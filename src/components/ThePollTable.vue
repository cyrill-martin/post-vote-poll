<template>
  <table>
    <tr>
      <th class="poll-question"></th>
      <th class="poll-arrangement"></th>
      <th class="poll-feature"></th>
    </tr>
    <the-poll-table-row
      v-for="key in selectionKeys"
      :key="key"
      :selection-id="key"
      :lang="lang"
      :question="selections[key]"
      :selected-arr="selectedArr"
      :selected-ord="selectedOrd"
      @new-chart-setting="setSetting"
    ></the-poll-table-row>
  </table>
</template>

<script>
import ThePollTableRow from "./ThePollTableRow.vue";

export default {
  components: {
    ThePollTableRow,
  },
  props: ["lang", "selections"],
  data() {
    return {
      selectedArr: false,
      selectedOrd: false,
    }
  },
  computed: {
    selectionKeys() {
      return Object.keys(this.selections);
    },
  },
  methods: {
    setSetting(newChartSetting) {
      // Received by TheCheckbox (e.g.): { id: "arr_BIRTHYEARR", state: true }
      const newSetting = newChartSetting.id.split("--");
      newSetting.push(newChartSetting.state)
      // [ "arr", "BIRTHYEARR", true ]
      if (newSetting[0] === "arr") {
        if (newSetting[2]) {
          this.selectedArr = newSetting[1];
        }
      } else {
        if (newSetting[2]) {
          this.selectedOrd = newSetting[1];
        }
      }
    }
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-spacing: 0;
}
</style>
