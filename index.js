const fs = require('fs');
const news = require('./news');

//every minute, check if news.json exists

news.getData();
setInterval(() => {
    news.getData();
}, 60000);