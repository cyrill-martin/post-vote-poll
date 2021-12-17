<template>
  <input
    type="checkbox"
    :id="inputId"
    v-model="checked"
    @click.stop="emitSetting"
  />
</template>

<script>
export default {
  emits: ["new-chart-setting"],
  props: ["chart-control", "selection-id", "selected-arr", "selected-ord"],
  inject: ["defaultArr", "defaultOrd"],
  mounted() {
    if (this.selectionId === this.defaultArr && this.chartControl === "arr") {
      this.emitSetting();
    }
    if (this.selectionId === this.defaultOrd && this.chartControl === "ord") {
      this.emitSetting();
    }
  },
  data() {
    return {
      checked: false,
    };
  },
  watch: {
    selectedArr() {
      if (this.chartControl === "arr") {
        this.checked = this.isChecked();
      }
    },
    selectedOrd() {
      if (this.chartControl === "ord") {
        this.checked = this.isChecked();
      }
    },
  },
  computed: {
    inputId() {
      return `${this.chartControl}--${this.selectionId}`;
    },
  },
  methods: {
    emitSetting() {
      this.$emit("new-chart-setting", {
        id: this.inputId,
        state: this.isChecked(),
      });
    },
    isChecked() {
      if (this.chartControl === "arr") {
        return this.selectionId === this.selectedArr;
      } else {
        return this.selectionId === this.selectedOrd;
      }
    },
  },
};
</script>

<style scoped>
input {
  cursor: pointer;
}
</style>
