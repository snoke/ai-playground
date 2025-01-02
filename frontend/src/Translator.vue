<template>
  <div class="grid-container">
    <div class="grid-item">
      <select v-model="fromLanguage" @input="onInputChange">
        <optgroup v-for="(k,v) of this.languages" :key="k" :label="getLanguage(v).name">
          <option v-for="o of k">{{o}}</option>
        </optgroup>
      </select>

      <div style="position: relative; width: 100%;">
        <!-- Spinner -->
        <div
            :hidden="!isUploading"
        >
        <font-awesome-icon
            :icon="['fas', 'spinner']"
            class="spinner rotate"
        /></div>

        <!-- Textarea -->
        <textarea
            ref="input"
            v-model="inputText"
            @input="onInputChange" placeholder="Text to translate"></textarea>
      </div>

      <button
          :disabled="isRecording"
          :hidden="isRecording"
          style="width:100%;"
          @click="this.startRecording()" ><font-awesome-icon :icon="['fas', 'microphone']" /></button>

      <button
          :disabled="!isRecording"
          :hidden="!isRecording"
          style="width:100%; color:blue;"
          @click="this.stopRecording()" ><font-awesome-icon :icon="['fas', 'microphone']" /></button>

    </div>
    <div class="grid-item">
      <button
          style="width:100%;"
          @click="this.switch()" ><font-awesome-icon :icon="['fas', 'rotate']" /></button>
      <div
          style="width:100%;"
          :hidden="!isTranslating"
      ><font-awesome-icon :icon="['fas', 'spinner']" class="rotate"/></div>
    </div>
    <div class="grid-item">


      <select v-model="toLanguage" @input="onInputChange">
        <optgroup v-for="(k,v) of this.languages" :key="k" :label="getLanguage(v).name">
          <option v-for="o of k">{{o}}</option>
        </optgroup>
      </select>

      <div style="position: relative; width: 100%;">
        <!-- Spinner -->
        <font-awesome-icon
            :icon="['fas', 'spinner']"
            class="spinner rotate"
            :hidden="!isTranslating"
            :opacity="!isTranslating?0:1"
        />

        <!-- Textarea -->
        <textarea
            ref="output"
            v-model="outputText"
            placeholder="Translation will appear here"
            readonly
            class="textarea-with-spinner"
        ></textarea>
      </div>

      <button
          :disabled="isPlayback"
          :hidden="isPlayback"
          style="width:100%;"
          @click="this.startPlayback()" ><font-awesome-icon :icon="['fas', 'volume-high']" /></button>

      <button
          :disabled="!isPlayback"
          :hidden="!isPlayback"
          style="width:100%; color:blue;"
          @click="this.stopPlayback()" ><font-awesome-icon :icon="['fas', 'volume-high']" /></button>

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
  name: 'Translator',
  components: {Dropdown},
  data() {
    return {
      languages: [],
      lang: {},
      voices: [],
      fromLanguage: 'auto',  // Standardwert: Automatic
      toLanguage: 'ger',      // Standardwert: Deutsch
      voice:'',
      inputText: '',
      outputText: '',
      debounceTimeout: null,
      isTranslating: false,     // Status der Audio-Wiedergabe
      isUploading: false,     // Status der Audio-Wiedergabe
      isRecording: false,    // Status der Audioaufnahme
      isPlayback: false,     // Status der Audio-Wiedergabe
      mediaRecorder: null,   // MediaRecorder-Instanz
      audioChunks: [],
      audioBlob: null,
      audioUrl: '',          // URL für die Audio-Wiedergabe
    };
  },
  created() {
    this.languages = languages;
    },
  mounted() {
  },
  methods: {
    getLanguage(alpha3Code) {
      const language = iso6393.find(lang => lang.iso6393 === alpha3Code.substring(0,3));

      return language;
    },
    // Start Recording (bleibt unverändert)
    async startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(stream);
        this.mediaRecorder.ondataavailable = (event) => {
          this.audioChunks.push(event.data);
        };
        this.mediaRecorder.start();
        this.isRecording = true;
        console.log('Recording started!');
      } catch (err) {
        this.isRecording = false;
        console.error('Error accessing microphone:', err);
      }
    },

    // Stop Recording (bleibt unverändert)
    stopRecording() {
      if (this.mediaRecorder) {
        this.mediaRecorder.stop();
        this.isRecording = false;
        console.log('Recording stopped!');
        this.mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
          this.audioChunks = [];
          this.audioBlob = audioBlob;
          const mp3Blob = await this.convertToMp3(audioBlob);
          await this.uploadAudio(mp3Blob);
        };
      }
    },

    // Optional: MP3-Konvertierung (bleibt unverändert)
    async convertToMp3(blob) {
      return blob;
    },

    // Audio hochladen und die URL der Audiodatei empfangen
    async uploadAudio(audioBlob) {
      console.log(this.getLanguage(this.fromLanguage))
      this.isUploading = true
      const formData = new FormData();
      formData.append('file', audioBlob, 'audio.mp3');
      formData.append('language', this.getLanguage(this.fromLanguage).iso6391);

      try {
        const response = await axios.post('http://localhost:8000/transcribe/', formData, {

          headers: {'Content-Type': 'multipart/form-data'},
        });

        this.isUploading = false
        console.log(response.data.transcription)
        this.inputText = response.data.transcription  || ''; // Zeige die Transkription im Textfeld
        await this.onInputChange();
      } catch (error) {
        this.isUploading = false
        console.error('Error uploading audio:', error);
      }
    },

    // Debounce-Funktion für Text-Übersetzungen (bleibt unverändert)
    switch() {
      [this.toLanguage, this.fromLanguage] = [this.fromLanguage, this.toLanguage];
      [this.inputText, this.outputText] = [this.outputText, this.inputText];
       this.onInputChange();
    },
    async onInputChange() {
      if (this.debounceTimeout) {
        clearTimeout(this.debounceTimeout);
      }
      this.debounceTimeout = setTimeout(async () => {
        if (this.inputText.trim()) {
          try {
            this.isTranslating = true;
            const response = await axios.post(
                'http://localhost:8000/translate/',
                {
                  text: this.inputText,
                  from_language: this.fromLanguage,
                  to_language: this.toLanguage,
                },
                {
                  headers: {
                    'Content-Type': 'application/json',  // Content-Type korrekt setzen
                  },
                }
            );
            console.log(response.data.translation)

            this.fromLanguage = response.data.translation.from
            this.toLanguage = response.data.translation.to
            this.outputText = response.data.translation.message;
          } catch (error) {
            console.error('Error during translation:', error);
            this.outputText = 'Error during translation';
          }
          this.isTranslating = false;
        } else {
          this.outputText = ''; // Textfeld leeren, wenn keine Eingabe
        }
      }, 1500);
    },

    // Text an das Backend senden, um Audio zu generieren
    async startPlayback() {
      this.isPlayback = true;
      try {
        // Sende den Text an das Backend, um das Audio zu generieren
        const response = await axios.post('http://localhost:8001/playback-transcription', {
          text: this.outputText,
          language: this.toLanguage,
        }, {
          responseType: 'blob' // Erwarten von Binärdaten (Audio)
        });

        const audioUrl = URL.createObjectURL(response.data);

        const audio = new Audio(audioUrl);

        // Event: Audio zu Ende
        audio.onended = () => {
          this.isPlayback = false;
          console.log('Playback finished!');
        };

        audio.play();

        console.log('Playback started!');
      } catch (error) {
        this.isPlayback = false;
        console.error('Error during audio playback:', error);
      }
    },

    test() {
      alert("hi")
    },
    // Stop Wiedergabe (bleibt unverändert)
    stopPlayback() {
      const audio = new Audio(this.audioUrl);
      audio.pause();
      this.isPlayback = false;
      console.log('Playback stopped!');
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
</style>