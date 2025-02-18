<template>
  <div class="container">
    <div class="row col-12 poll-info">
      <h1>{{ pollMetadata[lang] }} - {{ pollMetadata.date }} *</h1>
    </div>
    <div class="row col-12" id="table-header">
      <table>
        <tr>
          <th class="poll-question">{{ question[lang] }}</th>
          <th
            class="poll-arrangement poll-icon"
            id="arr-icon"
            @click="scrollToLine('arr')"
          >
            <img
              src="../assets/images/drag_indicator_black_24dp.svg"
              alt="Poll arrangement icon"
            />
          </th>
          <th
            class="poll-order poll-icon"
            id="ord-icon"
            @click="scrollToLine('ord')"
          >
            <img
              src="../assets/images/south_black_24dp.svg"
              alt="Poll order icon"
            />
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
      <div v-if="pollData && arrangement" class="col-10">
        <span v-html="introSentence(pollData.length, nrOfAnswers, lang)"></span
        >:
        <br />
        <span id="poll-arrangement" v-html="selectionText(arrangement)"></span>
      </div>
      <div v-else class="col-10"></div>
      <div class="col-2"></div>
    </div>
    <div class="row">
      <div v-if="pollData" class="col-10" id="poll-chart"></div>
      <the-dot-matrix
        v-if="pollSelections && pollArrangements && pollData"
        :poll-data="pollData"
        :poll-arrangements="pollArrangements"
        :poll-selections="pollSelections"
        :selected-arrangement="arrangement"
        :selected-order="order"
        :poll-lang="lang"
        @nr-of-answers="updateNrOfAnswers"
      ></the-dot-matrix>
      <!-- <div v-if="pollData && arrangement" class="col-2" id="poll-order"> -->
      <div class="col-2" id="poll-order">
        <span v-if="order" id="order-text" v-html="selectionText(order)"></span>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <p>
          * Für die Visualisierung werden maximal 1000 Teilnehmer:innen der
          Nachbefragung zur Abstimmung dargestellt. Die Auswahl basiert auf der
          Sortierung aller Teilnehmer:innen nach Sozialversicherungsnummer
          (aufsteigend) und der Verwendung der ersten 1000 Teilnehmer:inner einer
          Befragung. Transformierte und für diese Seite verwendete Daten sind
          verfügbar auf
          <a
            :href="`https://github.com/cyrill-martin/swisspolls/tree/main/public/data/${id}`"
            target="_blank"
            >https://github.com/cyrill-martin/swisspolls/tree/main/public/data/{{
              id
            }}</a
          >. Original-Codebuch und -Datensatz zur Nachbefragung sind verfügbar
          auf
          <a :href="`https://swissvotes.ch/vote/${id}.00`" target="_blank"
            >https://swissvotes.ch/vote/{{ id }}.00</a
          >.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import Polls from "../data/polls.json";
import ThePollTable from "../components/ThePollTable.vue";
import TheDotMatrix from "../components/TheDotMatrix.vue";

export default {
  components: {
    ThePollTable,
    TheDotMatrix,
  },
  props: ["id", "lang"],
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
  data() {
    return {
      pollData: null,
      nrOfAnswers: null,
      pollArrangements: null,
      pollSelections: null,
      arrangement: null,
      order: false,
      question: {
        de: "Frage",
        fr: "Question",
        it: "Questione",
      },
    };
  },
  provide() {
    return {
      // Default selections
      defaultArr: this.defaultArr,
      defaultOrd: this.defaultOrd,
    }
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
    defaultArr() {
      if (this.$route.query.arr) {
        return this.$route.query.arr;
      }
      return "PART"
    },
    defaultOrd() {
      if (this.$route.query.ord) {
        return this.$route.query.ord;
      }
      return "POLINT"
    }
  },
  methods: {
    introSentence(total, actual, lang) {
      const sentences = {
        de: `${total} Menschen wurden gefragt, <mark>${actual}</mark> haben geantwortet`,
        fr: `${total} personnes ont été interrogées, <mark>${actual}</mark> ont répondu`,
        it: `È stato chiesto a ${total} persone, <mark>${actual}</mark> hanno risposto`,
      };
      return sentences[lang];
    },
    updateNrOfAnswers(nr) {
      this.nrOfAnswers = nr;
    },
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
    updateUrl() {
      history.pushState(
        {},
        null,
        `${this.$route.path}?arr=${this.arrangement}&ord=${this.order}`
      );
    },
    setArrangement(arr) {
      // [ "arr", "BIRTHYEARR", true ]
      if (this.arrangement === arr[1]) {
        this.arrangement = false;
      } else {
        this.arrangement = arr[1];
        this.updateUrl();
      }
    },
    setOrder(ord) {
      if (this.order === ord[1]) {
        this.order = false;
      } else {
        this.order = ord[1];
        this.updateUrl();
      }
    },
    selectionText(key) {
      if (this.pollSelections[key]) {
        return this.pollSelections[key][this.lang];
      } else {
        const superKey = key.split("_");
        return `${this.pollSelections[superKey[0]][this.lang]}<br>- ${
          this.pollSelections[superKey[0]].selections[key][this.lang]
        }`;
      }
    },
    scrollToLine(column) {
      let col = this.arrangement;
      if (column === "ord") {
        col = this.order;
      }
      document
        .getElementById(`${column}--${col}`)
        .scrollIntoView({ behavior: "smooth" });
    },
  },
};
</script>

<style scoped>
#poll-questions {
  padding-top: 0;
  margin-bottom: 1rem;
  height: 25vh;
  border-bottom: solid 1px black;
  overflow-y: scroll;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
/* WebKit */
#poll-questions::-webkit-scrollbar {
  width: 0;
  height: 0;
}
#poll-arrangement {
  font-weight: bold;
  font-size: 1.2rem;
}
#order-text {
  font-weight: bold;
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
