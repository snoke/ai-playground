<template>
  <div class="">
    <div class="log">
      <div class="log_entry" v-for="message of this.messages">
        <p :class="message.role">{{ message.content }}</p>
      </div>
    </div>

      <div style="position: relative; width: 100%;">

        <!-- Textarea -->
        <input type="text"
            ref="input"
            v-model="inputText"
            placeholder="Text"></input>
        <button @click="onInputChange" >send</button>
      </div>





  </div>
</template>
<script>

import axios from 'axios';
import Dropdown from './components/Dropdown.vue';
import languages from './language_mapping.json';
import voices from './voices.json';
import {iso6393} from 'iso-639-3';
export default {
  name: 'Chat',
  components: {},
  data() {
    return {
      messages: [
        { role: 'system', content: 'you are a helpful Assistant.'}
      ],
      inputText: '',
      outputText: '',
      debounceTimeout: null,
      isGenerating: false,     // Status der Audio-Wiedergabe
    };
  },
  created() {
    },
  mounted() {
  },
  methods: {

    async onInputChange() {
      this.messages.push(
          { role: 'user', content:this.inputText.trim()}
      )
        if (this.inputText.trim()) {
          try {
            this.isGenerating = true;
            const response = await axios.post(
                'http://localhost:8000/chat/',
                {
                  messages: this.messages,
                },
                {
                  headers: {
                    'Content-Type': 'application/json',  // Content-Type korrekt setzen
                  },
                }
            );
            console.log(response.data)
            this.messages.push(response.data)
            this.outputText =  response.data.content;
          } catch (error) {
            console.error('Error during translation:', error);
            this.outputText = 'Error during translation';
          }
          this.isGenerating = false;
        } else {
          this.outputText = ''; // Textfeld leeren, wenn keine Eingabe
        }
    },

  },
};
</script>
<style scoped>
.grid-item {
  width:100%;
  text-align:center;
}
.grid-container {
  width: 100vw;                         /* Nimmt die gesamte Breite des Viewports ein */

  display: grid;
  grid-template-columns: 1fr 100px 1fr;  /* Drei Spalten */
  grid-template-rows: auto auto auto;   /* Drei Zeilen */
  gap: 10px;                            /* Abstand zwischen den Grid-Elementen */
}

textarea {
  width: 100%;
  height: 150px;
}

select, input[type="button"] {
  width: 100%;
}
/* CSS-Animation bleibt hier lokal */
.rotate {
  animation: spin 1s linear infinite;
}
@keyframes spin {
   0% {
     transform: rotate(0deg);
   }
   100% {
     transform: rotate(360deg);
   }
 }
/* Spinner Styling */
.spinner {
  font-size: 2rem;      /* Größe des Spinners */
  margin-left: -1rem;margin-top: -1rem;
  top:50%;
  left:50%;
  position: absolute;   /* Absolut positioniert */
  transform: translate(-50%, -50%); /* Zentrieren */
  z-index: 10;          /* Über der Textarea */
  color: gray;          /* Farbe des Spinners */
}

/* Textarea Styling */
.textarea-with-spinner {
  position: relative;   /* Textarea bleibt im Layoutfluss */
  width: 100%;
  z-index: 1;           /* Hinter dem Spinner */
  opacity: 0.5;         /* Halbtransparent, um den Spinner hervorzuheben */
  pointer-events: none; /* Keine Interaktion möglich während des Ladens */
}
.assistant {
  color: green;
}
.user {
  color: blue;
}
</style>