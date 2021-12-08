<template>
  <tr v-if="question" class="question">
    <td class="sub-question">{{ question[lang] }}</td>
    <td>
      <the-checkbox
        :chart-control="'arr'"
        :selection-id="selectionId"
        :selected-arr="selectedArr"
        @new-chart-setting="emitSetting"
      ></the-checkbox>
    </td>
    <td>
      <the-checkbox
        :chart-control="'ord'"
        :selection-id="selectionId"
        :selected-ord="selectedOrd"
        @new-chart-setting="emitSetting"
      ></the-checkbox>
    </td>
  </tr>
</template>

<script>
import TheCheckbox from "./TheCheckbox.vue";

export default {
  components: {
    TheCheckbox,
  },
  emits: ["new-chart-setting"],
  props: ["selection-id", "lang", "question", "selected-arr", "selected-ord"],
  methods: {
    emitSetting(newSetting) {
      this.$emit("new-chart-setting", newSetting);
    },
  },
};
</script>

<style scoped>
.sub-question {
  padding-left: 1rem;
}
tr > td {
  border-top: dashed 1px rgb(68, 68, 68);
}
td {
  vertical-align: top;
}
.question:hover {
  background-color: rgb(233, 233, 233);
}
</style>
