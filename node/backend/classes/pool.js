const createWord = require("./word");
const readline = require("readline");
const clear = require("clear");
const chalk = require("chalk");

const sum = arr => arr.reduce((p, c) => p + c, 0);

const createDBWrite = require("./DBWrite");

class Pool {
    constructor(clientArg, practiceObj) {
        this.knexClient = clientArg;
        this.practiceObj = practiceObj;
        this.dbWrite = createDBWrite([this.knexClient]);

        this.rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

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

    selectFromDB(sql, nextFn, nextParams) {
        sql(this.knexClient.select("*").from("words")).then(data => {
            nextFn(this.createWord(data[0]), ...nextParams);
        });
    }

    createWord(rawWordData) {
        return createWord(rawWordData);
    }

    askQuestion(word, msgs = "", promptLang="rand", answerLang=undefined) {
        let ask;
        if (promptLang === 'rand') {
            ask = word.questionRand;
        } else {
            ask = word.question(promptLang, answerLang)
        }

        const headerString = chalk.bold("한국말\n");

        let messages = msgs;

        clear();

        this.rl.question(
            `${headerString}${messages}\nYour score is ${
                this.practiceObj.score.correct
            }/${this.practiceObj.score.total}\n(word ${word.id}@${Math.round(
                sum(word.scoreHistory)
            )}) ${ask.prompt}: `,
            answer => {
                if (answer.includes(".")) {
                    switch (answer) {
                        case ".므ㅠ":
                        case ".amb":
                            let currentHint = word.hint;
                            this.askQuestion(
                                word,
                                `${Object.keys(currentHint)[0]} • ${
                                    Object.values(currentHint)[0]
                                }`,
                                word.promptLang,
                                word.answerLang
                            );
                            break;
                        case ".벼샤":
                        case ".quit":
                        case ".q":
                        case ".ㅂ":
                            console.log("Goodbye!");
                            process.exit();
                        case ".help":
                        case ".되ㅔ":
                        case ".h":
                        case ".ㅗ":
                            this.askQuestion(
                                word,
                                `[.amb, .므ㅠ] • show a hint | [.quit, .q, .벼샤, .ㅂ] • quit | [.help, .h, .되ㅔ, .ㅗ] • help`,
                                word.promptLang, 
                                word.answerLang
                            );
                        default:
                            this.askQuestion(
                                word,
                                `Command '${answer}' not found.`,
                                word.promptLang,
                                word.answerLangs
                            );
                            break;
                    }
                } else {
                    this.rl.question(
                        word.score(answer, ask, false)
                            ? "Correct!\n"
                            : `Incorrect, expected answer '${ask.answer}'\n`,
                        ammend => {
                            if (ammend === "c" || ammend === "ㅊ") {
                                this.practiceObj.saveScore(
                                    word.score(ask.answer, ask, true)
                                );
                                console.log("Answer ammended.");
                            } else {
                                // Handle answer
                                this.practiceObj.saveScore(
                                    word.score(answer, ask, true)
                                );
                            }
                            this.dbWrite.save(word, this.home, [this]);
                        }
                    );
                }
            }
        );
    }

    home(pool) {
        pool.selectFromDB(pool.SQL_selectOnDifficulty, askQuestion, [pool]);
    }
}

function askQuestion(data, pool) {
    pool.askQuestion(data);
}

function createPool(args) {
    return new Pool(...args);
}

module.exports = createPool;

// const wordPool = new Pool(client);
// wordPool.selectFromDB(wordPool.SQL_selectAny, askQuestion, [wordPool]);
