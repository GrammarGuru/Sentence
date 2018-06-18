const express = require('express');
const bodyParser = require('body-parser');
const parseText = require('./src/parseText');
const getNews = require('./src/getNews');
const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/parse', parseText);
app.get('/getNews', getNews);

// Listen to the App Engine-specified port, or 8080 otherwise
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});