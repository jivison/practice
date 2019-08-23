class DBWrite {
    constructor(client) {
        this.client = client;
    }

    save(word, nextFn, nextParams) {
        this.client("words")
            .where("id", "=", word.id)
            .update(word.dbCompatible)
            .then(() => {
                nextFn(...nextParams);
            });
    }
}

module.exports = params => {
    return new DBWrite(...params);
};
