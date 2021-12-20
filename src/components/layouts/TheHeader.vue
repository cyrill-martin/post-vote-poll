<template>
  <div class="col-12">
    <div class="logo">
      <router-link to="/">
        <img :src="logo" alt="The kmapper logo"
      /></router-link>
    </div>
    <div class="languages">
      <button
        :class="{ isSelected: language === 'de' }"
        @click="setLanguage('de')"
      >
        DE
      </button>
      <button
        :class="{ isSelected: language === 'fr' }"
        @click="setLanguage('fr')"
      >
        FR
      </button>
      <button
        :class="{ isSelected: language === 'it' }"
        @click="setLanguage('it')"
      >
        IT
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: ["lang"],
  mounted() {
    this.language = this.lang;
  },
  data() {
    return {
      language: null,
    };
  },
  computed: {
    logo() {
      return require("../../assets/images/kmapper_k_3b.png");
    },
  },
  methods: {
    setLanguage(lang) {
      this.language = lang;
      this.$emit("change-language", this.language);
    },
  },
};
</script>

<style scoped>
img {
  width: 120px;
}

.languages {
  font-size: 0.8rem;
  position: absolute;
  top: 0.8rem;
  right: 0.8rem;
  z-index: 10;
}

.languages button {
  margin-left: 0.25rem;
  cursor: pointer;
  border: none;
  background: none;
}

.isSelected {
  font-weight: bold;
}
</style>
