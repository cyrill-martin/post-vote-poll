<template>
  <div class="container">
    <div class="row col-12 poll-info">
      <h1>{{ pollMetadata[lang] }} - {{ pollMetadata.date }}</h1>
    </div>
    <div class="row col-12" id="table-header">
      <table>
        <tr>
          <th class="poll-question">{{ question[lang] }}</th>
          <th class="poll-arrangement poll-icon" id="arr-icon" @click="scrollToLine('arr')">
            <img src="../assets/images/drag_indicator_black_24dp.svg" alt="Poll arrangement icon" />
          </th>
          <th class="poll-order poll-icon" id="ord-icon" @click="scrollToLine('ord')">
            <img src="../assets/images/south_black_24dp.svg" alt="Poll order icon" />
          </th>
        </tr>
      </table>
    </div>
    <div class="row" id="poll-questions">
      <div v-if="pollSelections" class="col-12">
        <the-poll-table
          :lang="lang"
          :selections="pollSelections"
          :arrangement="arrangement"
          :order="order"
          @set-arrangement="setArrangement"
          @set-order="setOrder"
        ></the-poll-table>
      </div>
      <div v-else class="col-12">Loading...</div>
    </div>
    <div class="row">
      <div v-if="pollData" class="col-9" id="poll-chart">
        <span v-if="arrangement">{{ selectionText(arrangement) }}</span>
        <span v-else></span>
        by
        <span v-if="order">{{ selectionText(order) }}</span>
        <span v-else></span>
      </div>
      <div class="col-3" id="poll-legend">Legend</div>
    </div>
  </div>
</template>

<script>
import Polls from "../data/polls.json";
import ThePollTable from "../components/ThePollTable.vue";

export default {
  components: {
    ThePollTable,
  },
  props: ["id", "lang"],
  data() {
    return {
      pollData: null,
      pollArrangements: null,
      pollSelections: null,
      arrangement: false,
      order: false,
      question: {
        de: "Frage",
        fr: "Question",
        it: "Questione",
      },
    };
  },
  computed: {
    pollMetadata() {
      return Polls.find((poll) => poll.id.toString() === this.id);
    },
    selectionKeys() {
      if (this.pollSelections) {
        return Object.keys(this.pollSelections);
      } else {
        return [];
      }
    },
  },
  async mounted() {
    const pollData = await this.tryCatchData("data");
    if (pollData) {
      this.pollData = pollData;
    }

    const pollArrangements = await this.tryCatchData("arrangements");
    if (pollArrangements) {
      this.pollArrangements = pollArrangements;
    }

    const pollSelections = await this.tryCatchData("selections");
    if (pollSelections) {
      this.pollSelections = pollSelections;
    }
  },
  methods: {
    async fetchData(file) {
      const pollData = `${process.env.VUE_APP_BASEURL}/data/${this.id}/${this.id}_${file}.json`;
      const response = await fetch(pollData);
      const responseData = await response.json();
      if (!response.ok) {
        const error = new Error(
          response.message || `Failed to request "${file}" for poll ${this.id}`
        );
        throw error;
      }
      return responseData;
    },
    async tryCatchData(file) {
      try {
        // await this.fetchData(file).then((response) => {
        //   responseData = response;
        // });
        const responseData = await this.fetchData(file);
        return responseData;
      } catch (error) {
        console.log(`Error: "${file}" for poll ${this.id} not found!`);
        console.log(error);
      }
    },
    setArrangement(arr) {
      // [ "arr", "BIRTHYEARR", true ]
      if (this.arrangement === arr[1]) {
        this.arrangement = false;
      } else {
        this.arrangement = arr[1];
      }
    },
    setOrder(ord) {
      if (this.order === ord[1]) {
        this.order = false;
      } else {
        this.order = ord[1];
      }
    },
    selectionText(key) {
      if (this.pollSelections[key]) {
        return this.pollSelections[key][this.lang];
      } else {
        const superKey = key.split("_");
        return this.pollSelections[superKey[0]].selections[key][this.lang];
      }
    },
    scrollToLine(column) {
      if (column === "arr") {
        document.getElementById(`arr--${this.arrangement}`).scrollIntoView();
      } else {
        document.getElementById(`ord--${this.order}`).scrollIntoView();
      }
    }
  },
};
</script>

<style scoped>
/* #table-header {
  padding-bottom: 0;
} */
#poll-questions {
  padding-top: 0;
  height: 30vh;
  border-bottom: solid 1px black;
  overflow-y: scroll;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* Internet Explorer 10+ */
}
#poll-questions::-webkit-scrollbar {
  /* WebKit */
  width: 0;
  height: 0;
}
table {
  width: 100%;
  border-spacing: 0;
}
tr {
  background-color: lightgrey;
}
th {
  text-align: left;
}
.poll-icon {
  cursor: pointer;
}
</style>
