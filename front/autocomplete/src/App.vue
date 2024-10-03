<script setup lang="ts">
import Search from './components/Search.vue'
import ClientInfo from './components/ClientInfo.vue'
import { ref } from 'vue'

const selectedClient = ref(null);

function onClientSelected(client) {
  // Assigne les informations du client à selectedClient.value
  selectedClient.value = client;
}

</script>

<template>
  <main>
    
    <!-- La barre de recherche -->
    <div class="search-wrapper">
      <Search @client-selected="onClientSelected" />
    </div>

    <!-- Composant pour afficher les résultats -->
     <div class="client-infos">
    <ClientInfo v-if="selectedClient" :client="selectedClient" />
    </div>
  </main>
</template>


<style scoped>

/* Assure que la barre de recherche reste en haut */
.search-wrapper {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 60px; /* Espace pour les résultats en dessous */
}

.client-infos {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
