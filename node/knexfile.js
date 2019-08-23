// Update with your config settings.

module.exports = {

  development: {
    client: 'pg',
    connection: {
      database: 'korean_words',
      username: "john",
      password: "password"
    },
    migrations : {
        tableName : "migrations",
    }
  }

};
