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
      :selected-arr="arrangement"
      :selected-ord="order"
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
  props: ["lang", "selections", "arrangement", "order"],
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
        this.$emit("set-arrangement", newSetting);
      } else {
        this.$emit("set-order", newSetting);
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
