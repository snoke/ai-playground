<template>
  <ul>
    <li>
      <RouterLink to="/chat">chat</RouterLink>
      <RouterLink to="/translate">translate</RouterLink>
    </li>
  </ul>
    <RouterView />
</template>
<script>


export default {
  name: 'App',
  components: {},
  data() {
    return {
    };
  },
  created() {
  },
  mounted() {
  },
  methods: {
  },
};
</script>
<style scoped>
</style>