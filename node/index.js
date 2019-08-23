const client = require("./client");
const createPractice = require("./classes/practice");

const practice = createPractice([client]);

practice.start();
