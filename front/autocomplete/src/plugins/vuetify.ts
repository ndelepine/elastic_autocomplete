import 'vuetify/styles'  // Vuetify styles
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'  // Import des icônes Material Design
import '@mdi/font/css/materialdesignicons.css'  // Styles pour les icônes MDI


// Créer l'instance Vuetify avec l'icône MDI
const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})

export default vuetify