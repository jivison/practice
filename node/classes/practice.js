const createPool = require("./pool");


class Practice {
    constructor(dbClient) {
        this.score = {
            correct: 0,
            total: 0
        };

        this.pool = createPool([dbClient, this]);
    }

    start() {
        this.pool.home(this.pool);
    }

    saveScore(outcome) {
        this.score.total += 1;
        this.score.correct += outcome ? 1 : 0;
    }
}

function createPractice(args) {
    return new Practice(...args);
}

module.exports = createPractice;


