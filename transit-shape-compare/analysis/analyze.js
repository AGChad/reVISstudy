import { readFileSync } from "fs";

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

    const shapes = ["rect", "circle", "triangle", "plus", "diamonde", "badge", "crescent"];
    const modes = ["walk", "bicycle", "car", "train", "plane", "bus", "boat"];

    for (const result of results) {
        if (result.trialId == "participantTags") continue;

        const question = parseInt(result.trialId.substring(19));
        result.shape = shapes[Math.floor(question / 7)];
        result.mode = modes[question % 7];
    }

    return results;
}

console.log(analyze());