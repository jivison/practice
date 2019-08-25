const createWord = require("../backend/classes/word");
const createDBWrite = require("../backend/classes/DBWrite");


const sum = arr => arr.reduce((p, c) => p + c, 0);

class Pool {
    constructor(clientArg) {
        this.knexClient = clientArg;
        this.dbWrite = createDBWrite([this.knexClient]);

        // Selecting options
        this.SQL_selectAny = knex => {
            return knex.orderByRaw("RANDOM()").limit(1);
        };

        this.SQL_selectOnDifficulty = knex => {
            return knex
                .min({ minimum: "difficulty_sum" })
                .groupBy("id")
                .orderByRaw("minimum ASC, RANDOM()");
        };
    }

    async selectFromDB(sql) {
        return sql(this.knexClient.select("*").from("words")).then(data => {
            return this.createWord(data[0]);
        });
    }

    createWord(rawWordData) {
        return createWord(rawWordData);
    }


    askQuestion(word, msgs = "", promptLang = "rand", answerLang = undefined) {
        let ask;
        if (promptLang === "rand") {
            ask = word.questionRand;
        } else {
            ask = word.question(promptLang, answerLang);
        }

        
    }

    home(pool) {
        // pool.selectFromDB(pool.SQL_selectOnDifficulty, askQuestion, [pool]);
        pool.selectFromDB(pool.SQL_selectAny, askQuestion, [pool]);
    }
}


function createPool(args) {
    return new Pool(...args);
}

module.exports = createPool;
