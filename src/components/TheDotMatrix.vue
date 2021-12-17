<template>
  <div id="tooltip"></div>
</template>

<script>
import * as d3 from "d3";

export default {
  props: [
    "pollData",
    "pollArrangements",
    "pollSelections",
    "selectedArrangement",
    "selectedOrder",
    "pollLang",
  ],
  inject: ["defaultArr", "defaultOrd"],
  mounted() {
    this.drawDotMatrix();
    this.language = this.pollLang;
  },
  data() {
    return {
      arrangement: false,
      order: false,
      language: "de",
      maxDotsPerRow: 80,
      xScaleOuter: null,
      xScaleInner: null,
      yScale: null,
    };
  },
  watch: {
    selectedArrangement() {
      this.arrangement = this.selectedArrangement;
      // Update D3
      this.callUpdateArrangement(this.arrangement, this.order);
    },
    selectedOrder() {
      this.order = this.selectedOrder;
      // Update D3
      this.callUpdateArrangement(this.arrangement, this.order);
    },
    pollLang() {
      this.language = this.pollLang;
    },
  },
  methods: {
    getOuterXDomain(arrangement) {
      // Outer x-Scale - depends on the arrangement
      console.log("pollArrangement", this.pollArrangements);
      console.log("arrangement", arrangement);
      const xOuterItems = Object.keys(this.pollArrangements[arrangement]);
      const xOuterDomain = xOuterItems.map(
        (item) => this.pollArrangements[arrangement][item][this.language]
      );
      return xOuterDomain;
    },
    getInnerXDomain(nrOfOuterGroups) {
      // The inner scale is given by the maxSeatsPerRow divided by number of outer groups
      const xInnerDomain = Array.from(
        Array(Math.ceil(this.maxDotsPerRow / nrOfOuterGroups)).keys()
      );
      return xInnerDomain;
    },
    getYDomain(arrangement, order, nrOfInnerGroups) {
      // y-Scale - depends on largest group: Number of members / xInnerDomain

      // Group the this.dataset by the selected arrangement
      const groupedData = d3.groups(this.pollData, (d) => d[arrangement]);
      // E.g. this.dataset = [
      //   [ "1", [...] ],
      //   [ "2", [...] ],
      //   ...
      // ]

      groupedData.forEach((group) => {
        // Sort group according to order
        group[1].sort((a, b) => {
          return d3.ascending(a[order], b[order]);
        });

        // Add innerIdx to get positioning right later
        group[1].forEach((item, index) => {
          const datasetItem = this.pollData.find(
            ({ CODERESP }) => CODERESP === item.CODERESP
          );
          datasetItem.innerIdx = index;
        });
      });

      // Get the number of dots of the largest group
      const largestGroup = d3.max(groupedData, (group) => {
        return group[1].length;
      });

      // Set the y-scale domain
      // It's the number of dot rows of the largest group
      const yScaleDomain = Array.from(
        Array(Math.ceil(largestGroup / nrOfInnerGroups)).keys()
      );
      return yScaleDomain;
    },
    drawDotMatrix() {
      d3.select("svg").remove();

      // Set dimensions
      const dimensions = {
        width: 1000,
        height: 300,
        margins: {
          top: 15,
          right: 10,
          bottom: 15,
          left: 10,
        },
        ctrWidth: null,
        ctrHeight: null,
      };

      // Create and set inner container width
      dimensions.ctrWidth =
        dimensions.width - (dimensions.margins.left + dimensions.margins.right);
      // Create and set inner container height
      dimensions.ctrHeight =
        dimensions.height -
        (dimensions.margins.top + dimensions.margins.bottom);

      // Create SVG element
      const svg = d3
        .select("#poll-chart")
        .append("svg")
        .attr("preserveAspectRatio", "xMinYMin")
        .attr("viewBox", `0 0 ${dimensions.width} ${dimensions.height}`);

      // Add inner container to SVG
      const ctr = svg
        .append("g")
        .attr(
          "transform",
          `translate(${dimensions.margins.left}, ${dimensions.margins.top})`
        );

      // Get tooltip element from DOM
      const tooltip = d3.select("#tooltip");
      console.log(ctr, tooltip);

      const drawArrangement = (
        arrangement,
        outerXDomain,
        innerXDomain,
        yDomain
      ) => {
        // Create the actual outer x-scale
        this.xScaleOuter = d3
          .scaleBand()
          .domain(outerXDomain)
          .range([0, dimensions.ctrWidth])
          .paddingInner(0.05) // Space between groups of x-axis items
          .paddingOuter(0.05)
          .align(0.5);

        // Create the actual inner x-scale
        this.xScaleInner = d3
          .scaleBand()
          .domain(innerXDomain)
          .range([0, this.xScaleOuter.bandwidth()])
          .paddingInner(0.05);

        // Create the actual y-scale
        this.yScale = d3
          .scaleBand()
          .domain(yDomain)
          .range([0, dimensions.ctrHeight])
          .paddingInner(0.1);

        // Create x-axis
        const xAxis = d3
          .axisBottom(this.xScaleOuter)
          .tickSize(0)
          .tickSizeOuter(0);

        // Draw x-axis
        const xAxisLine = ctr
          .append("g")
          .attr("id", "x-axis")
          .attr("transform", `translate(0, ${dimensions.ctrHeight})`)
          .call(xAxis);

        // Remove the horizontal x-axis line
        xAxisLine.call((axis) => axis.select(".domain").remove());

        const dotsGroup = ctr.append("g").attr("class", "dots");

        dotsGroup
          .selectAll("g")
          .data(this.pollData)
          .join("g")
          .attr("class", "dot")
          .attr("transform", (d) => {
            return `translate(${+this.xScaleOuter(
              this.pollArrangements[arrangement][d[arrangement]][this.language]
            )}, 0)`;
          }) // Position along the main x-axis
          // .attr("id", (d) => d.id)
          .append("circle")
          .attr("class", "human")
          .attr("cx", (d) => {
            // Get index of inner Scale
            const iIdx = d.innerIdx % innerXDomain.length;
            return this.xScaleInner(iIdx) + this.xScaleInner.bandwidth() / 2;
          })
          .attr("cy", (d) => {
            const yIdx = Math.floor(d.innerIdx / innerXDomain.length);
            return this.yScale(yIdx);
          })
          .attr("r", () => {
            let r = this.xScaleInner.bandwidth() / 2;
            if (this.yScale.bandwidth() / 2 < r) {
              r = this.yScale.bandwidth() / 2;
            }
            return r;
          })
          .attr("fill", "black");

        // Update function
      };

      // Calculating drawArrangement parameters
      const outerXDomain = this.getOuterXDomain(this.defaultArr);
      const innerXDomain = this.getInnerXDomain(outerXDomain.length);
      const yDomain = this.getYDomain(
        this.defaultArr,
        this.defaultOrd,
        innerXDomain.length
      );

      // Calling drawArrangement()
      drawArrangement(this.defaultArr, outerXDomain, innerXDomain, yDomain);
    },
    updateArrangement(
      newArrangement,
      newOrder,
      newXOuter,
      newXInner,
      newYDomain
    ) {
      console.log(newOrder);

      // const newOuterXScale = this.xScaleOuter.domain(newXOuter);
      this.xScaleOuter.domain(newXOuter);

      // const newInnerXScale = this.xScaleInner
      this.xScaleInner
        .domain(newXInner)
        //.range([0, newOuterXScale.bandwidth()]);
        .range([0, this.xScaleOuter.bandwidth()]);

      // const newYScale = this.yScale.domain(newYDomain);
      this.yScale.domain(newYDomain);

      const x = d3.select("#x-axis");
      x.transition()
        .duration(1000)
        .call(d3.axisBottom(this.xScaleOuter).tickSize(0).tickSizeOuter(0));
      // Remove the horizontal x-axis line
      x.call((axis) => axis.select(".domain").remove());

      // Update the position of the dots
      d3.selectAll(".dot")
        .transition()
        .duration(2000)
        .attr("transform", (d) => {
          if (
            d[newArrangement] !== " " &&
            this.pollArrangements[newArrangement][d[newArrangement]][
              this.language
            ]
          ) {
            return `translate(${+this.xScaleOuter(
              this.pollArrangements[newArrangement][d[newArrangement]][
                this.language
              ]
            )}, 0)`;
          }
        }); // Position along the main x-axis

      d3.selectAll(".human")
        .transition()
        .duration(2000)
        .attr("cx", (d) => {
          // Get index of inner Scale
          const iIdx = d.innerIdx % newXInner.length;
          return this.xScaleInner(iIdx) + this.xScaleInner.bandwidth() / 2;
        })
        .attr("cy", (d) => {
          const yIdx = Math.floor(d.innerIdx / newXInner.length);
          return this.yScale(yIdx);
        })
        .attr("r", () => {
          let r = this.xScaleInner.bandwidth() / 2;
          if (this.yScale.bandwidth() / 2 < r) {
            r = this.yScale.bandwidth() / 2;
          }
          return r;
        })
        .attr("fill", "black");
    },
    callUpdateArrangement(arrangement, order) {
      const newXOuter = this.getOuterXDomain(arrangement);
      const newXInner = this.getInnerXDomain(newXOuter.length);
      const newYDomain = this.getYDomain(arrangement, order, newXInner.length);
      this.updateArrangement(
        arrangement,
        order,
        newXOuter,
        newXInner,
        newYDomain
      );
    },
  },
};
</script>
