import '@mdi/font/css/materialdesignicons.css';
import { createVuetify } from 'vuetify';
import { aliases, mdi } from 'vuetify/iconsets/mdi'; // Import material design icons
import 'vuetify/styles'; // Vuetify styles


const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'light', // Default theme
    themes: {
      light: {
        colors: {
          primary: '#1976D2', // Blue
          secondary: '#424242', // Grey
          background: '#FFFFFF', // White
        },
      },
      dark: {
        colors: {
          primary: '#BB86FC', // Purple
          secondary: '#03DAC6', // Teal
          background: '#121212', // Dark background
        },
      },
    },
  },
})

export default vuetify