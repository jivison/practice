const express = require("express");
const morgan = require("morgan");
const cookieParser = require("cookie-parser");
const path = require("path");

const createBackend = require("./helpers/backend.js");
const createWord = require("./backend/classes/word");
const createDBWrite = require("./backend/classes/DBWrite");

const client = require("./backend/client");
const backend = createBackend([client]);
const dbWrite = createDBWrite([client]);

const app = express();

app.use(express.static(path.join(__dirname, "public")));
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(morgan("dev"));

app.use((req, res, next) => {
    res.locals.word = req.cookies.word;
    res.locals.promptLang = req.cookies.promptLang;
    res.locals.answerLang = req.cookies.answerLang;
    res.locals.ammended = req.cookies.ammended;
    next();
});

app.set("view engine", "jade");

app.get("/", (req, res) => {
    res.render("welcome");
});

app.get("/new", (req, res) => {
    backend.selectFromDB(backend.SQL_selectOnDifficulty).then(word => {
        let ask = word.questionRand;

        res.cookie("word", word);
        res.cookie("promptLang", word.promptLang);
        res.cookie("answerLang", word.answerLang);

        let ammend = res.locals.ammended;
        res.clearCookie("ammended");

        res.render(
            "homepage",
            Object.assign(ask, {
                hints: [],
                ammended: ammend,
                wordId: word.id
            })
        );
    });
});

app.post("/answer", (req, res) => {
    let word = createWord({
        id: res.locals.word.id,
        korean: res.locals.word.korean,
        english: res.locals.word.english,
        classification: Object.values(res.locals.word.hintsUnmodified[0])[0],
        notes: Object.values(res.locals.word.hintsUnmodified[1])[0],
        speech_part: Object.values(res.locals.word.hintsUnmodified[2])[0],
        score_history_csv: res.locals.word.scoreHistory.join(",")
    });
    word.promptLang = res.locals.word.promptLang;
    word.answerLang = res.locals.word.answerLang;

    if (req.body.answer === word[res.locals.answerLang]) {
        // Handle correct DB-wise
        word.save(true, true);
    }

    dbWrite.save(
        word,
        () => {
            if (req.body.answer === ".hint") {
                res.render(
                    "homepage",
                    Object.assign(
                        word,
                        word.question(word.promptLang, word.answerLang),
                        {
                            hints: word.hints,
                            wordId: word.id,
                        }
                    )
                );
            } else {
                res.render(
                    "postState",
                    Object.assign(
                        word,
                        word.question(word.promptLang, word.answerLang),
                        {
                            hints: word.hints,
                            answerState:
                                req.body.answer === word[res.locals.answerLang]
                                    ? "correct"
                                    : "incorrect",
                            next:
                                req.body.answer === word[res.locals.answerLang]
                        }
                    )
                );
            }
        },
        []
    );
});

app.post("/ammend", (req, res) => {
    let word = createWord({
        id: res.locals.word.id,
        korean: res.locals.word.korean,
        english: res.locals.word.english,
        classification: Object.values(res.locals.word.hintsUnmodified[0])[0],
        notes: Object.values(res.locals.word.hintsUnmodified[1])[0],
        speech_part: Object.values(res.locals.word.hintsUnmodified[2])[0],
        score_history_csv: res.locals.word.scoreHistory.join(",")
    });

    if (req.body.answer === "c" || req.body.answer === "ㅊ") {
        word.save(true, true);
        res.cookie("ammended", true);
    } else {
        word.save(false, true);
    }
    dbWrite.save(
        word,
        args => {
            res.redirect("/new");
        },
        []
    );
});

const PORT = 4545;
const ADDRESS = "localhost";

app.listen(PORT, ADDRESS, () => {
    console.log(`Express server started on ${ADDRESS} and ${PORT}`);
});
