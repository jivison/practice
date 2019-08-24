const Papa = require("papaparse")
const fs = require("fs");

function generatePool() {
    let csvData = Papa.parse(fs.readFileSync("/home/john/practice/node/backend/wordPool.csv").toString());

    return csvData.data.slice(1).reduce((acc, val) => {
        acc.push({
            korean: val[0],
            english: val[1],
            speech_part: val[2],
            classification: val[3],
            notes: val[4],
            score_history_csv: "0,0,0",
            difficulty_sum: 0
        });
        return acc
    }, []);

}

exports.seed = function(knex) {
    // Deletes ALL existing entries
    return knex("words")
        .del()
        .then(function() {
            // Inserts seed entries
            return knex("words").insert(generatePool());
        });
};
