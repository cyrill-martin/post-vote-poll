<template>
  <tr :class="isSuperQuestion ? 'superQuestion' : 'question'">
    <td>{{ question[lang] }}</td>
    <td v-if="!question.selections">
      <the-checkbox
        :chart-control="'arr'"
        :selection-id="selectionId"
        :selected-arr="selectedArr"
        @new-chart-setting="emitSetting"
      ></the-checkbox>
    </td>
    <td v-else></td>
    <td v-if="!question.selections">
      <the-checkbox
        :chart-control="'ord'"
        :selection-id="selectionId"
        :selected-ord="selectedOrd"
        @new-chart-setting="emitSetting"
      ></the-checkbox>
    </td>
    <td v-else></td>
  </tr>
  <the-poll-table-sub-row
    v-for="key in subSelectionKeys"
    :key="key"
    :selection-id="key"
    :lang="lang"
    :question="question.selections[key]"
    :selected-arr="selectedArr"
    :selected-ord="selectedOrd"
    @new-chart-setting="emitSetting"
  ></the-poll-table-sub-row>
</template>

<script>
import TheCheckbox from "./TheCheckbox.vue";
import ThePollTableSubRow from "./ThePollTableSubRow.vue";

export default {
  components: {
    TheCheckbox,
    ThePollTableSubRow,
  },
  emits: ["new-chart-setting"],
  props: ["lang", "selection-id", "question", "selected-arr", "selected-ord"],
  computed: {
    isSuperQuestion() {
      return this.question.selections;
    },
    subSelectionKeys() {
      return this.question.selections
        ? Object.keys(this.question.selections)
        : [];
    },
  },
  methods: {
    emitSetting(newSetting) {
      this.$emit("new-chart-setting", newSetting)
    }
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-spacing: 0;
}
td {
  vertical-align: top;
}
.superQuestion {
  background-color: lightgrey;
}
tr.question > td {
  border-top: solid 1px rgb(68, 68, 68);
}
.question:hover {
  background-color: rgb(233, 233, 233);
}
</style>
