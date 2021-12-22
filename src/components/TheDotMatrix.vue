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
  emits: ["nr-of-answers"],
  inject: ["defaultArr", "defaultOrd"],
  mounted() {
    this.drawDotMatrix();
    this.language = this.pollLang;
  },
  data() {
    return {
      arrangement: this.defaultArr,
      order: this.defaultOrd,
      language: "de",
      maxDotsPerRow: 100,
      xScaleOuter: null,
      xScaleInner: null,
      yScale: null,
      duration: 2000,
      linearColors: null,
      orderKeys: null,
      colorScheme: [
        "283d3b",
        "197278",
        "edddd4",
        "c44536",
        "772e25",
        "21585a",
        "83a8a6",
        "d99185",
        "9e3a2e",
        "4c4340",
      ],
    };
  },
  watch: {
    selectedArrangement() {
      this.arrangement = this.selectedArrangement;
      const order = this.order || this.defaultOrd;
      // Update D3
      this.callUpdateArrangement(this.arrangement, order);
    },
    selectedOrder() {
      this.order = this.selectedOrder;
      const arrangement = this.arrangement || this.defaultArr;
      // Update D3
      this.callUpdateArrangement(arrangement, this.order, true);
    },
    pollLang() {
      this.language = this.pollLang;
      this.drawDotMatrix();
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

        // Get rid of "MISSING" values
        xOuterDomain = xOuterDomain.filter((item) => item !== "MISSING");

        return xOuterDomain;
      } else {
        // It's numerical
        // Get the max
        const max = parseInt(
          d3.max(this.pollData, (human) => human[arrangement])
        );
        // Get the min
        const min = parseInt(
          d3.min(this.pollData, (human) => human[arrangement])
        );
        xOuterDomain = Array.from({ length: max - min + 1 }, (_, i) => i + min);
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

      let groupedData;

      let dataLength = this.pollData.length;

      // Get rid of "MISSING" values
      if (this.pollArrangements[arrangement]) {
        groupedData = this.pollData.filter((human) => {
          return this.existence(human, arrangement);
        });
        dataLength = groupedData.length;
      } else {
        groupedData = this.pollData;
      }

      // EMIT dataLength;
      this.$emit("nr-of-answers", dataLength);

      // Group the data by the selected arrangement
      groupedData = d3.groups(groupedData, (d) => d[arrangement]);
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

      this.orderKeys = Array.from({ length: max - min + 1 }, (_, i) => i + min);

      colorScale = d3
        .scaleLinear()
        .domain([min, max])
        .range(["lightgrey", "black"]);
      return colorScale;
    },
    existence(d, arrangement) {
      let existence = false;

      if (!this.pollArrangements[arrangement]) {
        existence = true;
      } else if (d[arrangement] !== " ") {
        if (
          this.pollArrangements[arrangement][d[arrangement]][this.language] !==
          "MISSING"
        ) {
          existence = true;
        }
      }
      return existence;
    },
    drawLegend(keys) {
      d3.select("#svg-legend").remove();

      const dimensions = {
        width: 200,
        height: 800,
        margins: {
          top: 0,
          right: 10,
          bottom: 500,
          left: 5,
        },
        ctrWidth: null,
        ctrHeight: null,
      };

      const spacingVertical = 15;
      const circleRadius = spacingVertical / 3;
      const spacingHorizontal = spacingVertical / 2;

      // Create SVG element
      const svg = d3
        .select("#poll-order")
        .append("svg")
        .attr("id", "svg-legend")
        .attr("preserveAspectRatio", "xMinYMin")
        .attr("viewBox", `0 0 ${dimensions.width} ${dimensions.height}`);

      // Add inner container to SVG
      const ctr = svg
        .append("g")
        .attr(
          "transform",
          `translate(${dimensions.margins.left}, ${dimensions.margins.top})`
        );

      // Add legend group
      const legendGroup = ctr
        .append("g")
        .attr("class", "legend")
        .style("font-size", "10px")
        .attr("transform", `translate(0, ${dimensions.margins.top})`);

      // Add <g> for each legend item
      const legendItems = legendGroup
        .selectAll(".legend-item")
        .data(keys)
        .join("g")
        .attr("class", "legend-item")
        .attr(
          "transform",
          (_, i) => `translate(0, ${spacingVertical + i * spacingVertical})`
        );

      // Draw the legend circles for selected legend keys
      legendItems
        .append("circle")
        .transition()
        .duration(1000)
        .attr("cx", 0)
        .attr("cy", 0.5)
        .attr("r", circleRadius)
        .attr("fill", (d) => {
          if (this.linearColors) {
            return this.linearColors(d);
          } else {
            return `#${
              this.colorScheme[
                this.orderKeys.indexOf(d) % this.colorScheme.length
              ]
            }`;
          }
        });
      const order = this.order || this.defaultOrd;
      // Write the legend keys next to the legend circles
      legendItems
        .append("text")
        .attr("opacity", 0)
        .transition()
        .duration(1000)
        .attr("opacity", 1)
        .attr("x", spacingHorizontal)
        .attr("y", circleRadius / 2 + 1)
        .text((d) => {
          if (this.linearColors) {
            return d;
          } else {
            return this.pollArrangements[order][d][this.language];
          }
        });
    },
    drawDotMatrix() {
      d3.select("#svg-chart").remove();

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
        .attr("id", "svg-chart")
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

        dotsGroup
          .selectAll("g")
          .data(this.pollData)
          .join("g")
          .attr("class", "dot")
          .attr("transform", (d) => {
            if (this.existence(d, arrangement)) {
              return `translate(${+this.xScaleOuter(
                this.pollArrangements[arrangement][d[arrangement]][
                  this.language
                ]
              )}, 0)`;
            }
          }) // Position along the main x-axis
          .append("circle")
          .attr("class", "human")
          .attr("cx", (d) => {
            if (this.existence(d, arrangement)) {
              // Get index of inner Scale
              const iIdx = d.innerIdx % innerXDomain.length;
              return this.xScaleInner(iIdx) + this.xScaleInner.bandwidth() / 2;
            }
          })
          .attr("cy", (d) => {
            if (this.existence(d, arrangement)) {
              const yIdx = Math.floor(d.innerIdx / innerXDomain.length);
              return this.yScale(yIdx);
            }
          })
          .attr("r", (d) => {
            if (this.existence(d, arrangement)) {
              let r = this.xScaleInner.bandwidth() / 2;
              if (this.yScale.bandwidth() / 2 < r) {
                r = this.yScale.bandwidth() / 2;
              }
              return r;
            }
          })
          .attr("fill", (d) => {
            if (this.existence(d, arrangement)) {
              if (this.linearColors) {
                return this.linearColors(d[order]);
              } else {
                return `#${
                  this.colorScheme[
                    this.orderKeys.indexOf(d[order]) % this.colorScheme.length
                  ]
                }`;
              }
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
          .attr("dy", -1)
          .attr("dx", -15)
          .attr("transform", "rotate(-90)");

        // Remove the horizontal x-axis line
        xAxisLine.call((axis) => axis.select(".domain").remove());
      };

      // Calculating drawArrangement parameters
      const arrangement = this.arrangement || this.defaultArr;
      const order = this.order || this.defaultOrd;

      const outerXDomain = this.getOuterXDomain(arrangement);
      const innerXDomain = this.getInnerXDomain(outerXDomain.length);
      const yDomain = this.getYDomain(arrangement, order, innerXDomain.length);

      // colors
      this.updateColors(order);
      this.drawLegend(this.orderKeys);

      // Calling drawArrangement()
      drawArrangement(arrangement, order, outerXDomain, innerXDomain, yDomain);
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
        .attr("transform", "rotate(-90)");

      // Remove the horizontal x-axis line
      x.call((axis) => axis.select(".domain").remove());

      // Update the position of the dots
      d3.selectAll(".dot")
        .transition()
        .duration(this.duration)
        .attr("transform", (d) => {
          if (this.existence(d, newArrangement)) {
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
              }
            } else {
              return `translate(${+this.xScaleOuter(
                parseInt(d[newArrangement])
              )}, 0)`;
            }
          }
        }); // Position along the main x-axis

      d3.selectAll(".human")
        .transition()
        .duration(this.duration)
        .attr("cx", (d) => {
          if (this.existence(d, newArrangement)) {
            // Get index of inner Scale
            const iIdx = d.innerIdx % newXInner.length;
            return this.xScaleInner(iIdx) + this.xScaleInner.bandwidth() / 2;
          }
        })
        .attr("cy", (d) => {
          if (this.existence(d, newArrangement)) {
            const yIdx = Math.floor(d.innerIdx / newXInner.length);
            return this.yScale(yIdx);
          }
        })
        .attr("r", (d) => {
          if (this.existence(d, newArrangement)) {
            let r = this.xScaleInner.bandwidth() / 2;
            if (this.yScale.bandwidth() / 2 < r) {
              r = this.yScale.bandwidth() / 2;
            }
            return r;
          }
        })
        .attr("fill", (d) => {
          if (this.existence(d, newArrangement)) {
            if (this.linearColors) {
              return this.linearColors(d[this.order]);
            } else {
              return `#${
                this.colorScheme[
                  this.orderKeys.indexOf(d[this.order]) %
                    this.colorScheme.length
                ]
              }`;
            }
          }
        });
    },
    callUpdateArrangement(arrangement, order, legend = false) {
      const newXOuter = this.getOuterXDomain(arrangement);
      const newXInner = this.getInnerXDomain(newXOuter.length);
      const newYDomain = this.getYDomain(arrangement, order, newXInner.length);

      // colors
      if (legend) {
        this.updateColors(order);
        this.drawLegend(this.orderKeys);
      }

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
