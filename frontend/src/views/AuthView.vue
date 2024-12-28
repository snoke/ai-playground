<template>
  <div class="auth">
    <h1>Google Auth</h1>
    <div id="google-sign-in" style="overflow:hidden;"></div>
  </div>
</template>

<script>
export default {
  name: 'GoogleAuth',
  props: {
    oauthClientId: {
      type: String,
      required: true,
    },
    oauthRedirectUri: {
      type: String,
      required: true,
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
        // Falls das Skript bereits geladen ist
        this.initializeGoogleSignIn();
      }
    },
    initializeGoogleSignIn() {
      google.accounts.id.initialize({
        client_id: '325144873900-s2eib0vh981tol0ukm5u1q7pscl8qmsh.apps.googleusercontent.com',
        callback: (response) => {
          window.location.href = `http://localhost:8001/auth/google?token=${response.credential}`;
        },
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
  },
};
</script>

<style scoped>
/* Deine CSS-Anpassungen hier */
</style>