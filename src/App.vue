<template>
  <div class="container page">
    <header class="row">
      <the-header @change-language="changeLanguage" :lang=lang></the-header>
    </header>
    <main class="row">
      <div class="col-12">
        <router-view :lang="lang"></router-view>
      </div>
    </main>
    <footer class="row">
      <the-footer></the-footer>
    </footer>
  </div>
</template>

<script>
import TheHeader from "./components/layouts/TheHeader.vue";
import TheFooter from "./components/layouts/TheFooter.vue";

export default {
  components: {
    TheHeader,
    TheFooter,
  },
  data() {
    return {
      lang: "de",
    };
  },
  methods: {
    changeLanguage(lang) {
      this.lang = lang;
    }
  }
};
</script>

<style scoped>
.page {
  position: relative;
  min-height: 100vh;
}

header {
  height: 4rem;
  padding-top: 1rem;
}

footer {
  text-align: center;
  height: 3rem;
}

@media only screen and (max-width: 65em) {
  header {
    padding-top: 0;
  }

  .page {
    padding: 0;
  }
}
</style>
