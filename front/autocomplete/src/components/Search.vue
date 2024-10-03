<template>
  <div class="search-container">
    <!-- Icône de loupe -->
    <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 18a8 8 0 100-16 8 8 0 000 16zM21 21l-4.35-4.35" />
    </svg>

    <!-- Barre de recherche -->
    <input 
      v-model="query" 
      @input="fetchSuggestions" 
      @keydown="handleKeyDown"
      placeholder="Rechercher un nom ou prénom" 
    />

    <!-- Liste des suggestions -->
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

</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      suggestions: [],
      selectedIndex: -1,  // Indice de l'élément actuellement surligné
    };
  },
  methods: {
    // Fonction pour récupérer les suggestions basées sur la saisie
    fetchSuggestions() {
      this.selectedIndex =  -1
      if (this.query.length > 2) {
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

    // Séléction des suggestions avec le clavier
    handleKeyDown(event) {
      if (event.key === 'ArrowDown') {
        // Naviguer vers le bas dans la liste des suggestions
        if (this.selectedIndex < this.suggestions.length - 1) {
          this.selectedIndex++;
          this.scrollToView(this.selectedIndex); // Faire défiler jusqu'à l'élément surligné
        }
      } else if (event.key === 'ArrowUp') {
        // Naviguer vers le haut dans la liste des suggestions
        if (this.selectedIndex > 0) {
          this.selectedIndex--;
          this.scrollToView(this.selectedIndex); // Faire défiler jusqu'à l'élément surligné
        }
      } else if (event.key === 'Enter') {
        // Sélectionner l'élément actuellement surligné avec la touche Entrée
        if (this.selectedIndex >= 0) {
          this.selectSuggestion(this.suggestions[this.selectedIndex]);
        }
      }
    },

    scrollToView(index) {
      // Récupérer l'élément correspondant à l'index et faire défiler jusqu'à lui
      const element = this.$refs.suggestionItems[index];
      if (element) {
        element.scrollIntoView({
          block: 'nearest',  // Le mode 'nearest' s'assure que l'élément est entièrement visible
          behavior: 'smooth'  // Animation de défilement douce
        });
      }
    },

    // Sélection d'une suggestion et récupération des infos du client
    selectSuggestion(suggestion) {
      axios.get(`/api/clients/_doc/${suggestion._id}`)
        .then(response => {
          const client = response.data._source;  // Récupère les données du client
          // Emet un événement avec le client sélectionné
          this.$emit('client-selected', client);
          this.suggestions = [];
          this.query = `${ response.data._source.first_name } ${ response.data._source.name}`
          this.selectedIndex =  -1
        })
        .catch(error => {
          console.error('Erreur lors de la récupération des informations du client :', error);
        });
    }
  }
};
</script>

<style scoped>

.search-container {
  position: relative;
  width: 100%;  /* Prend toute la largeur du wrapper */
  max-width: 600px;  /* Limite la largeur maximale */
  margin-top: 20px;  /* Marge avec le haut */

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

input {
  padding-left: 40px;  /* Espace pour l'icône */
  padding-right: 10px;
  padding-top: 10px;
  padding-bottom: 10px;
  width: 100%;  /* Prend toute la largeur du conteneur parent */
  border: none;
  border-bottom: 2px solid #ccc;
  outline: none;
  font-size: 16px;
}

input:focus {
  border-bottom: 2px solid #5a5a5a;
}

.suggestions-list {
  position: absolute;  /* Position absolue pour placer la liste sous l'input */
  top: 100%;
  left: 0;
  width: 100%;  /* Prend toute la largeur du conteneur parent (search-container) */
  background-color: white;
  border: 1px solid #ccc;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  padding: 0;
  margin: 5px 0 0 0;
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
