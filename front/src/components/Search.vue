<template>
    <v-container>
      <div class="search-container">

        <!-- Search bar -->

          <v-text-field
          v-model="query" 
          @input="fetchSuggestions" 
          @keydown="handleKeyDown"
          clearable
          label="Client name"
          placeholder="Name or first name"
          prepend-inner-icon="mdi-magnify"
          hide-details
          variant="underlined"
          ></v-text-field>


        <!-- Suggestions list -->
        <ul v-if="suggestions.length" class="suggestions-list">
          <li 
            v-for="(suggestion, index) in suggestions" 
            :key="index"
            @click="selectSuggestion(suggestion)"
            :class="{ 'highlighted': index === selectedIndex }"
            ref="suggestionItems"
            style="cursor: pointer"
          >
            {{ suggestion._source.first_name }} {{ suggestion._source.name }}
          </li>
        </ul>

      </div>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      suggestions: [],
      selectedIndex: -1,  // Index of the current selected suggestion
    };
  },
  methods: {
    // Fonction to ges the list of suggestions based on the input
    fetchSuggestions() {
      this.selectedIndex =  -1
      if (this.query.length > 2) {
        // Use axios to query ElasticSearch
        axios
          .post(`/api/clients/_search`, {
            suggest: {
              'name-suggest': {
                prefix: this.query,
                completion: {
                  field: 'name',
                  fuzzy: {
                    fuzziness: 1
                  }
                }
              },
              'first-name-suggest': {
                prefix: this.query,
                completion: {
                  field: 'first_name',
                  fuzzy: {
                    fuzziness: 1
                  }
                }
              }
            }
          })
          .then((response) => {
            const nameSuggestions = response.data.suggest['name-suggest'][0].options;
            const firstNameSuggestions = response.data.suggest['first-name-suggest'][0].options;

            this.suggestions = [
              ...nameSuggestions,
              ...firstNameSuggestions
            ];
          })
          .catch((error) => {
            console.error(error);
          });
      } else {
        this.suggestions = [];
      }
    },

    // Navigate through suggestions throught the keyboard
    handleKeyDown(event) {
      if (event.key === 'ArrowDown') {
        // Go down in the suggestion list
        if (this.selectedIndex < this.suggestions.length - 1) {
          this.selectedIndex++;
          this.scrollToView(this.selectedIndex); // Scroll to reach the selected element
        }
      } else if (event.key === 'ArrowUp') {
        // Go up in the suggestion list
        if (this.selectedIndex > 0) {
          this.selectedIndex--;
          this.scrollToView(this.selectedIndex); // Scroll to reach the selected element
        }
      } else if (event.key === 'Enter') {
        // Select the element with the Enter key
        if (this.selectedIndex >= 0) {
          this.selectSuggestion(this.suggestions[this.selectedIndex]);
        }
      }
    },

    scrollToView(index) {
      // Get the element with the index and scroll to it
      const element = this.$refs.suggestionItems[index];
      if (element) {
        element.scrollIntoView({
          block: 'nearest',  // The mode 'nearest' assure that the element is completely visible
          behavior: 'smooth'  // Smooth animation
        });
      }
    },

    // Select a suggestion, and get client informations
    selectSuggestion(suggestion) {
      axios.get(`/api/clients/_doc/${suggestion._id}`)
        .then(response => {
          const client = response.data._source;  // Get client infos
          // Emit a "client-selected" event to pass it to the ClientInfo component
          this.$emit('client-selected', client);
          this.suggestions = [];
          this.query = `${ response.data._source.first_name } ${ response.data._source.name}`
          this.selectedIndex =  -1
        })
        .catch(error => {
          console.error('Error while getting client informations :', error);
        });
    }
  }
};
</script>

<style scoped>

.search-container {
  position: relative;
  width: 100%;
  max-width: 600px;
  margin-top: 20px;

}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #999;
}

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: white;
  border: 1px solid #ccc;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  padding: 0;
  margin: 0 0 0 0;
  list-style: none;
}

.suggestions-list li {
  padding: 10px;
  border-bottom: 1px solid #eee;
}
.suggestions-list li.highlighted {
  background-color: #e0e0e0;
}
.suggestions-list li:hover {
  background-color: #f0f0f0;
}

</style>
