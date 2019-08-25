class Count {
    constructor() {
        this.scoreObj = {
            correct: 0,
            total: 0
        }
    }

    save(outcome) {
        this.scoreObj.total += 1;
        this.scoreObj.correct += (outcome) ? 1 : 0;
    }

    get score() {
        return this.scoreObj
    }
}

module.exports = () => {
    return new Count();
};
