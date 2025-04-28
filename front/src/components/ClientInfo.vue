  <template>
      <v-container>
        <div v-if="client">
            <h3 class="client-title">Client informations :</h3>
            
            <!-- Client informations -->
            <div class="client-details">
                <p><strong>Name : </strong>{{ client.name }}</p>
                <p><strong>First Name : </strong>{{ client.first_name }}</p>
                <p><strong>Email : </strong>{{ client.email }}</p>
                <p><strong>Adress : </strong>{{ client.address }}</p>
                <p><strong>Job : </strong>{{ client.job }}</p>
            </div>
        </div>
      </v-container>
  </template>
  
  <script setup lang="ts">
    import { Client } from '@/types/client';

    const client : Client = null
  </script>
  
  <style scoped>

  /* Put the title on the left */
  .client-title {
    position: relative;
    text-align: left;
    font-size: 2em;
    margin-bottom: 10px;
    margin-left: 0;
  }
  
  .client-details {
    position: absolute;
    text-align: left;  
    margin-left: 30px;  /* Shift the details a little bit on the right */
  }

  </style>