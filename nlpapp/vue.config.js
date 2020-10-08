module.exports = {
  "publicPath": process.env.NODE_ENV === 'production'
    ? '/nlpapp/'
    : '/',
  "transpileDependencies": [
    "vuetify"
  ]
}