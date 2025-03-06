//import { readFileSync } from "fs";
import d3 from "https://d3js.org/d3.v7.js";

const shapes = ["rect", "circle", "triangle", "plus", "diamonde", "badge", "crescent"];
const modes = ["walk", "bicycle", "car", "train", "plane", "bus", "boat"];

function process() {
    const data = readFileSync("./results.csv", "utf-8");
    const lines = data.split("\n");
    const results = [];
    const headers = lines.shift().split(",");
    for (const line of lines) {
        const values = line.split(",");
        const result = {};
        for (let i = 0; i < values.length; i++) {
            const value = JSON.parse(values[i]);
            const numberForm = parseInt(value);
            if (!isNaN(numberForm)) result[headers[i]] = numberForm;
            else result[headers[i]] = value;
        }
        results.push(result);
    }
    return results;
}

function analyze() {
    const results = process();

    for (const result of results) {
        if (result.trialId == "participantTags") continue;

        const question = parseInt(result.trialId.substring(19));
        result.shape = shapes[Math.floor(question / 7)];
        result.mode = modes[question % 7];
    }

    return results;
}

var data = analyze();

const margin = {top: 30, right: 30, bottom: 30, left: 30},
    width = 450 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;

const svg = d3.select("#dataviz")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

const x = d3.scaleBand()
    .range([ 0, width ])
    .domain(shapes)
    .padding(0.01);
    svg.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x))

const y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(modes)
    .padding(0.01);
    svg.append("g")
    .call(d3.axisLeft(y));

const myColor = d3.scaleLinear()
    .range(["white", "#69b3a2"])
    .domain([1,10])

svg.selectAll()
    .data(data, function(d) {return d.shape+':'+d.mode;})
    .join("rect")
    .attr("x", function(d) { return x(d.shape) })
    .attr("y", function(d) { return y(d.mode) })
    .attr("width", x.bandwidth() )
    .attr("height", y.bandwidth() )
    .style("fill", function(d) { return myColor(d.answer)} )
