<template>
  <div>{{ pollMetadata }}</div>
  <div>---</div>
  <div v-if="pollData">{{ pollData[0] }}</div>
  <div v-else>Loading...</div>
  <div>---</div>
  <div v-if="pollArrangements">{{ pollArrangements }}</div>
  <div v-else>Loading...</div>
  <div>---</div>
  <div v-if="pollSelections">{{ pollSelections }}</div>
  <div v-else>Loading...</div>
</template>

<script>
import Polls from "../data/polls.json";

export default {
  props: ["id", "lang"],
  data() {
    return {
      pollData: null,
      pollArrangements: null,
      pollSelections: null,
    };
  },
  computed: {
    pollMetadata() {
      return Polls.find((poll) => poll.id.toString() === this.id);
    }
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

    const pollSelections = await this.tryCatchData("arrangements");
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
  },
};
</script>
