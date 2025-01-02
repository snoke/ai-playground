<script>
export default {
  name: 'Dropdown',
  data() {
    return {
      visible: false,
      selected: null,
      filterTerm: ''
    }
  },
  props: {
    options: {
      type: Object, // Korrigiert: options sollte ein Objekt sein
      default: () => ({}),
    },
  },
  computed: {
    filteredOptions() {
      return Object.entries(this.options)
          .filter(([key, value]) =>
              value.toLowerCase().startsWith(this.filterTerm.toLowerCase())
          )
          .reduce((obj, [key, value]) => {
            obj[key] = value;
            return obj;
          }, {});
    },
  },
  methods: {
    hide() {
      this.visible = false;
    },
    show() {
      this.visible = true;
    },
    apply(key) {
      this.selected = key;
      this.$emit('change', key); // Ruft ein `change`-Event auf
      this.$emit('update:modelValue', key); // Für v-model Unterstützung
      this.hide(); // Dropdown schließen, nachdem eine Auswahl getroffen wurde
    },
  }
}
</script>

<template>
  <div>
    <input
        type="hidden"
        v-model="this.selected"
    />
    <input
        type="text"
        v-model="this.filterTerm"
        @focus="show"
        @input="show"
        @blur="hide"
    />
    <ul
        v-show="visible"
        @mousedown.prevent
    >
      <li
          v-for="(value, key) in filteredOptions"
          :key="key"
      >
        <button
            :value="key"
            @click="apply(key)"
        >
          {{ value }}
        </button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

* {
  width: 100%;
}
</style>