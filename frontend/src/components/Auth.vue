<template>
  <div class="auth">
    <h1>Google Auth</h1>
    <div id="google-sign-in" style="overflow:hidden;"></div>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import claim from '@/storage/claim.js';
export default {
  name: 'GoogleAuth',
  props: {
    oauthClientId: {
      type: String,
      default: '325144873900-s2eib0vh981tol0ukm5u1q7pscl8qmsh.apps.googleusercontent.com',
    },
    theme: {
      type: String,
      default: 'outline',
    },
    width: {
      type: String,
      default: '270',
    },
    locale: {
      type: String,
      default: 'en_EN',
    },
    type: {
      type: String,
      default: 'standard',
    },
    size: {
      type: String,
      default: 'medium',
    },
    text: {
      type: String,
      default: 'signin_with',
    },
    shape: {
      type: String,
      default: 'rectangular',
    },
    logoAlignment: {
      type: String,
      default: 'left',
    },
  },
  data() {
    return {
      claim,
      message: '',
    };
  },
  mounted() {
    this.loadGoogleScript();
  },
  methods: {
    loadGoogleScript() {
      if (!document.getElementById('google-sign-in-script')) {
        const script = document.createElement('script');
        script.id = 'google-sign-in-script';
        script.src = 'https://accounts.google.com/gsi/client';
        script.async = true;
        script.defer = true;
        script.onload = this.initializeGoogleSignIn;
        document.head.appendChild(script);
      } else {
        this.initializeGoogleSignIn();
      }
    },
    initializeGoogleSignIn() {
      google.accounts.id.initialize({
        //client_id: this.oauthClientId,
        client_id: '325144873900-s2eib0vh981tol0ukm5u1q7pscl8qmsh.apps.googleusercontent.com',
        callback: this.handleCredentialResponse,
      });
      google.accounts.id.renderButton(
          document.getElementById('google-sign-in'),
          {
            theme: this.theme,
            width: `${this.width}px`,
            locale: this.locale,
            type: this.type,
            size: this.size,
            text: this.text,
            shape: this.shape,
            logo_alignment: this.logoAlignment,
          }
      );
    },
    async handleCredentialResponse(response) {

      try {
        const res = await fetch("http://localhost:8001/auth/google?token=" + response.credential, {
          method: 'GET',
        });

        if (!res.ok) {
          throw new Error('Fehler bei der Authentifizierung');
        }

        const data = await res.json();
        this.message = `Erfolgreich authentifiziert: ${data.message}`;
        this.claim.email = data.email
      } catch (error) {
        console.error(error);
        this.message = 'Fehler: Authentifizierung fehlgeschlagen.';
      }
    },
  },
};
</script>

<style scoped>
/* Deine CSS-Anpassungen hier */
</style>