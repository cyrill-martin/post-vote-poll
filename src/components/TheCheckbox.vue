<template>
  <input type="checkbox" :id="inputId" v-model="checked" />
</template>

<script>
export default {
  emits: ["new-chart-setting"],
  props: ["chart-control", "selection-id", "selected-arr", "selected-ord"],
  data() {
    return {
      checked: this.ischecked(),
    }
  },
  watch: {
    checked(newValue) {
      this.$emit("new-chart-setting", { id: this.inputId, state: newValue });
    },
    selectedArr() {
      this.checked = this.ischecked();
    }, 
    selectedOrd() {
      this.checked = this.ischecked();
    }
  },
  computed: {
    inputId() {
      return `${this.chartControl}--${this.selectionId}`;
    },
  },
  methods: {
    ischecked() {
      if (this.chartControl === "arr") {
        return this.selectionId === this.selectedArr;
      } else {
        return this.selectionId === this.selectedOrd;
      } 
    }
  }
};
</script>

<style scoped>
input {
  cursor: pointer;
}
</style>
