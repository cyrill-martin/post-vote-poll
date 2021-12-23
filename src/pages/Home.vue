<template>
  <div class="container">
    <div class="row col-12">
      <h1 v-html="introSentence(lang)"></h1>
    </div>
    <div class="col-12">
      {{ explanationSentence(lang) }}
    </div>
    <div class="row col-12">
      <table>
        <tr>
          <th @click="sortColumn('date')">
            {{ tableColumns.date[lang] }}
            <span v-html="sortIndicator('date')"></span>
          </th>
          <th @click="sortColumn('vote')">
            {{ tableColumns.vote[lang] }}
            <span v-html="sortIndicator('vote')"></span>
          </th>
        </tr>
        <tr
          class="vote"
          v-for="poll in polls"
          :key="poll.id"
          :id="poll.id"
          @click="selectPoll(poll.id)"
        >
          <td class="vote-date">{{ poll.date }}</td>
          <td class="vote-vote">{{ poll[lang] }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import Polls from "../data/polls.json";

export default {
  mounted() {
    this.sortColumn("date");
  },
  props: ["lang"],
  data() {
    return {
      polls: Polls,
      tableColumns: {
        date: {
          clicks: 0,
          sortedDesc: false,
          de: "Datum",
          fr: "Date",
          it: "Data",
        },
        vote: {
          clicks: 0,
          sortedDesc: false,
          de: "Abstimmung",
          fr: "Votation",
          it: "Votazione",
        },
      },
    };
  },
  methods: {
    introSentence(lang) {
      const langs = {
        de: "Visualisierungen der <a href='https://swissvotes.ch' target='_blan'>swissvotes</a>-Datensätze der Nachbefragungen zu den eidgenössischen Volksabstimmungen",
        fr: "Visualisations des ensembles de données <a href='https://swissvotes.ch' target='_blan'>swissvotes</a> des enquêtes de suivi des référendums fédéraux",
        it: "Visualizzazioni dei set di dati <a href='https://swissvotes.ch' target='_blan'>swissvotes</a> dei sondaggi successivi ai referendum federali",
      };
      return langs[lang];
    },
    explanationSentence(lang) {
      const langs = {
        de: "Visualisiert werden die Aussagen von 1000 zufällig ausgewählten Personen.",
        fr: "Les déclarations de 1000 personnes sélectionnées au hasard sont visualisées.",
        it: "Vengono visualizzate le dichiarazioni di 1000 persone selezionate a caso.",
      };
      return langs[lang];
    },
    checkColumn(column) {
      if (column === "date") {
        return "id";
      } else {
        return this.lang;
      }
    },
    selectPoll(id) {
      this.$router.push({ path: `/poll/${id}` });
    },
    sortColumn(column) {
      if (column === "date") {
        this.tableColumns.vote.clicks = 0;
        this.tableColumns.vote.sortedDesc = false;
      } else {
        this.tableColumns.date.clicks = 0;
        this.tableColumns.date.sortedDesc = false;
      }

      this.tableColumns[column].clicks++;

      const mod = this.tableColumns[column].clicks % 3;

      if (mod !== 0) {
        this.tableColumns[column].sortedDesc =
          !this.tableColumns[column].sortedDesc;
      }

      if (this.tableColumns[column].sortedDesc) {
        column = this.checkColumn(column);
        this.polls.sort((a, b) => {
          return b[column] > a[column] ? 1 : -1;
        });
      } else {
        column = this.checkColumn(column);
        this.polls.sort((a, b) => {
          return b[column] < a[column] ? 1 : -1;
        });
      }
    },
    sortIndicator(column) {
      const mod = this.tableColumns[column].clicks % 3;
      if (mod === 0) {
        return "";
      } else if (mod === 1) {
        return "&#8595;";
      } else {
        return "&#8593;";
      }
    },
  },
};
</script>

<style scoped>
table {
  width: 100%;
  border-spacing: 0;
}
th {
  padding: 0.5rem;
  background-color: lightgrey;
  color: #3584e4;
  text-align: left;
  cursor: pointer;
}
span {
  color: #3584e4;
}
td {
  padding: 0.5rem;
  vertical-align: top;
  border-bottom: solid 1px rgb(68, 68, 68);
}
.vote {
  cursor: pointer;
}
.vote:hover {
  background-color: rgb(233, 233, 233);
}
.vote-date {
  width: 10%;
}
.vote-vote {
  width: 50%;
}
</style>
