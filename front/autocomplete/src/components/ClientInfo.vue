  <template>
      <div v-if="client">
          <!-- Titre aligné à gauche -->
          <h3 class="client-title">Informations du client :</h3>
          
          <!-- Informations du client avec un décalage à droite -->
          <div class="client-details">
              <p><strong>Nom : </strong>{{ client.name }}</p>
              <p><strong>Prénom : </strong>{{ client.first_name }}</p>
              <p><strong>Email : </strong>{{ client.email }}</p>
              <p><strong>Adresse : </strong>{{ client.address }}</p>
              <p><strong>Job : </strong>{{ client.job }}</p>
          </div>
      </div>
  </template>
  
  <script>
  export default {
    props: {
      client: {
        type: Object,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>

  /* Le titre reste aligné à gauche */
  .client-title {
    position: relative;
    text-align: left;
    font-size: 2em;
    margin-bottom: 10px;
    margin-left: 0;  /* Garde le titre aligné à gauche */
  }
  
  /* Les détails sont alignés à gauche mais légèrement décalés */
  .client-details {
    position: absolute;
    text-align: left;  /* Aligne tout à gauche */
    margin-left: 30px;  /* Décale les informations à droite */
  }

  </style>