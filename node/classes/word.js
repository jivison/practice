const sum = arr => arr.reduce((p, c) => p + c, 0);

class Word {
    constructor(id, korean, english, hints, wordHistory) {
        this.id = id;
        this.korean = korean;
        this.english = english;
        this.hintsUnmodified = hints;
        this.hints = hints.reduce((acc, element) => {
            try {
                if (!Object.values(element).includes("")) {
                    acc.push(element);
                }
            } catch (err) {}
            return acc;
        }, []);
        this.hintIndex = 0;
        this.scoreHistory = wordHistory.split(",");
        this.scoreHistory = this.scoreHistory.map(element => {
            return parseInt(element);
        });
    }

    get dbCompatible() {
        return {
            id: this.id,
            notes: this.hints.reduce((acc, val) => {
                return (val.notes && acc === '') ? val.notes : acc; 
            }, ""),
            korean: this.korean,
            english: this.english,
            speech_part: this.hints.reduce((acc, val) => {
                return (val.speech_part && acc === '') ? val.speech_part : acc; 
            }, ""),
            classification: this.hints.reduce((acc, val) => {
                return (val.classification && acc === '') ? val.classification : acc; 
            }, ""),
            score_history_csv: this.scoreHistory.join(","),
            difficulty_sum: sum(this.scoreHistory)
        };
    }

    get hint() {
        let hint = this.hints[this.hintIndex % this.hints.length];
        this.hintIndex += 1;
        return hint;
    }

    coinFlip() {
        return Math.floor(Math.random() * 2) == 0;
    }

    get questionRand() {
        let order = this.coinFlip()
            ? [this.english, this.korean]
            : [this.korean, this.english];
        return {
            prompt: order[0],
            answer: order[1]
        };
    }

    save(score, realScore) {
        if (realScore) {
            this.scoreHistory = this.scoreHistory.slice(1, 3);
            this.scoreHistory.push(score ? 1 : 0);
        }
    }

    score(userAnswer, answerObj, realScore = true) {
        if (userAnswer.toLowerCase() === answerObj.answer.toLowerCase()) {
            this.save(true, realScore);
            return true;
        } else {
            this.save(false, realScore);
            return false;
        }
    }
}

// {
//     id: '255',
//     korean: '듣다',
//     english: 'to hear',
//     speech_part: 'verb',
//     classification: 'abstracts',
//     notes: '듣다 follows the ㄷ irregular',
//     score_history_csv: '0,0,0'
// }

function createWord(rawWordData) {
    return new Word(
        rawWordData.id,
        rawWordData.korean,
        rawWordData.english,
        [
            { classification: rawWordData.classification },
            { notes: rawWordData.notes },
            { speech_part: rawWordData.speech_part }
        ],
        rawWordData.score_history_csv
    );
}

module.exports = createWord;
