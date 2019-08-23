exports.up = function(knex) {
    return knex.schema.createTable("words", table => {
        table.bigIncrements("id");
        table.string("korean");
        table.string("english");
        table.string("speech_part");
        table.string("classification");
        table.text("notes");
        table.string("score_history_csv");
        table.integer("difficulty_sum");
    });
};

exports.down = function(knex) {
    return knex.schema.dropTable("words");
};
