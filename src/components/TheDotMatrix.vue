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
      maxDotsPerRow: 100,
      xScaleOuter: null,
      xScaleInner: null,
      yScale: null,
      duration: 2000,
      linearColors: null,
      orderKeys: null,
      // colorScheme: d3.schemeTableau10,
      colorScheme: ["797d62","9b9b7a","baa587","d9ae94","f1dca7","ffcb69","e8ac65","d08c60","b58463","997b66"],
    };
  },
  watch: {
    selectedArrangement() {
      this.arrangement = this.selectedArrangement;
      const order = this.order || this.defaultOrd;
      // Update D3
      this.updateColors(order);
      this.callUpdateArrangement(this.arrangement, order);
    },
    selectedOrder() {
      this.order = this.selectedOrder;
      // Update D3
      this.updateColors(this.order);
      this.callUpdateArrangement(this.arrangement, this.order);
    },
    pollLang() {
      this.language = this.pollLang;
    },
  },
  methods: {
    updateColors(order) {
      if (!this.pollArrangements[order]) {
        this.linearColors = this.getColorScale(order);
      } else {
        this.linearColors = null;
        this.orderKeys = Object.keys(this.pollArrangements[order]);
      }
    },
    getOuterXDomain(arrangement) {
      // Outer x-Scale - depends on the arrangement
      let xOuterDomain;
      if (this.pollArrangements[arrangement]) {
        const xOuterItems = Object.keys(this.pollArrangements[arrangement]);
        xOuterDomain = xOuterItems.map(
          (item) => this.pollArrangements[arrangement][item][this.language]
        );
        return xOuterDomain;
      } else {
        // It's numerical
        // Get the max
        const max = parseInt(d3.max(this.pollData, (human) => human[arrangement]));
        // Get the min
        const min = parseInt(d3.min(this.pollData, (human) => human[arrangement]));
        console.log(min, max);
        xOuterDomain = Array.from({ length: max - min + 1 }, (_, i) => i + min);
        console.log(xOuterDomain);
      }
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
    getColorScale(order) {
      let colorScale;
      // It's numerical

      // Get the max
      const max = d3.max(this.pollData, (human) => human[order]);

      // Get the min
      const min = d3.min(this.pollData, (human) => human[order]);

      colorScale = d3
        .scaleLinear()
        .domain([min, max])
        .range(["lightgrey", "black"]);
      return colorScale;
    },
    colorGenerator(index) {
      return d3.schemePaired[index % 10];
    },
    drawDotMatrix() {
      d3.select("svg").remove();

      // Set dimensions
      const dimensions = {
        width: 1000,
        height: 800,
        margins: {
          top: 15,
          right: 10,
          bottom: 500,
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
      // const tooltip = d3.select("#tooltip");
      // console.log(tooltip);

      const drawArrangement = (
        arrangement,
        order,
        outerXDomain,
        innerXDomain,
        yDomain
      ) => {
        // Create the actual outer x-scale
        this.xScaleOuter = d3
          .scaleBand()
          .domain(outerXDomain)
          .range([0, dimensions.ctrWidth])
          .paddingInner(0.1) // Space between groups of x-axis items
          .paddingOuter(0.1)
          .align(0.5);

        // Create the actual inner x-scale
        this.xScaleInner = d3
          .scaleBand()
          .domain(innerXDomain)
          .range([0, this.xScaleOuter.bandwidth()])
          .paddingInner(0.1);

        // Create the actual y-scale
        this.yScale = d3
          .scaleBand()
          .domain(yDomain)
          .range([0, dimensions.ctrHeight])
          .paddingInner(0.1);

        const dotsGroup = ctr.append("g").attr("class", "dots");

        // colors
        this.updateColors(order);

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
          .attr("fill", (d) => {
            if (this.linearColors) {
              return this.linearColors(d[order]);
            } else {
              return `#${
                this.colorScheme[
                  this.orderKeys.indexOf(d[order]) % this.colorScheme.length
                ]
              }`;
            }
          });

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

        // Rotate axis tick labels
        xAxisLine
          .selectAll("text")
          .style("text-anchor", "end")
          .attr("dy", 10)
          .attr("dx", -10)
          // .attr("dy", "-1rem")
          // .attr("dx", "-1rem")
          .attr("transform", "rotate(-90)");

        // Remove the horizontal x-axis line
        xAxisLine.call((axis) => axis.select(".domain").remove());
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
      drawArrangement(
        this.defaultArr,
        this.defaultOrd,
        outerXDomain,
        innerXDomain,
        yDomain
      );
    },
    updateArrangement(
      newArrangement,
      newOrder,
      newXOuter,
      newXInner,
      newYDomain
    ) {
      console.log("newArrangement", newArrangement);
      console.log("newOrder", newOrder);

      this.xScaleOuter.domain(newXOuter);

      this.xScaleInner
        .domain(newXInner)
        .range([0, this.xScaleOuter.bandwidth()]);

      this.yScale.domain(newYDomain);

      const x = d3.select("#x-axis");
      x.transition()
        .duration(this.duration / 2)
        .call(d3.axisBottom(this.xScaleOuter).tickSize(0).tickSizeOuter(0));

      // Rotate axis tick labels
      x.selectAll("text")
        .style("text-anchor", "end")
        .attr("dy", -1)
        .attr("dx", -15)
        // .attr("dy", "-1rem")
        // .attr("dx", "-1rem")
        .attr("transform", "rotate(-90)");

      // Remove the horizontal x-axis line
      x.call((axis) => axis.select(".domain").remove());

      // Update the position of the dots
      d3.selectAll(".dot")
        .transition()
        .duration(this.duration)
        .attr("transform", (d) => {
          if (this.pollArrangements[newArrangement]) {
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
            } else {
              // Deal with positioning missing (" ") values
            }
          } else {
            return `translate(${+this.xScaleOuter(parseInt(d[newArrangement]))}, 0)`;
          }
        }); // Position along the main x-axis

      d3.selectAll(".human")
        .transition()
        .duration(this.duration)
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
        .attr("fill", (d) => {
          if (this.linearColors) {
            return this.linearColors(d[this.order]);
          } else {
            return `#${
              this.colorScheme[
                this.orderKeys.indexOf(d[this.order]) % this.colorScheme.length
              ]
            }`;
          }
        });
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
