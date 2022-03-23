//This file is based off news.py
const fs = require('fs');
const news = require('./news');
const fetch = require('node-fetch');

var newsJSON = {}

async function getJSONfile() {
    newsJSON = require('./news.json');
}

async function getData() {
    await getJSONfile();
    var url = `https://push.api.bbci.co.uk/batch?t=%2Fdata%2Fbbc-morph-lx-commentary-data-paged%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-${newsJSON.news_url}%2FisUk%2Ffalse%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F1%2FserviceName%2Fnews%2Fversion%2F1.5.6?timeout=5`;
    //console.log(url)
    var response = await fetch(url);
    response.json().then(data => {
        var latest = data.payload[0].body.results[0]
        if (latest["assetId"] == newsJSON.assetId) {
            console.log("No new news")
            return;
        }
        newsJSON.assetId = latest["assetId"];

        var title = latest["title"];
        var content = []
        var imageUrl = ""
        var isBreaking = latest["options"]["isBreakingNews"];
        var post_locator = latest["locator"];
        var updated = latest["lastUpdated"];

        try {
            for (imageKey in latest["media"]["images"]["body"]) {
                imageUrl = latest["media"]["images"]["body"][imageKey]["href"]
                break
            }
        } catch (e) {
            console.log("No image")
        }

        console.log(latest)
        for (item in latest["body"]) {
            item = latest["body"][item]

            if (item.name == "paragraph") {
                console.log("paragraph")

                for (child in item.children) {
                    child = item.children[child]
                    console.log("Child:")
                    console.log(child)

                    if (child.name == "text") {
                        console.log("Text:")
                        console.log(child.text)
                        content.push(child.text)
                    } else if (child.name == "link") {
                        console.log("link")
                        text = child.children[0].children[0].text;
                        text_url = child.children[2].attributes[1].value;
                        console.log(text_url)
                        if (text_url.startsWith("https://www.bbc.com/news/live/world-europe-") || text_url.startsWith("https://www.bbc.com/news/world-europe-")) {
                            newsJSON.news_url = text_url.split("-")[2];
                            console.log(`Changing news url to ${newsJSON.news_url}`);
                            break
                        }
                        content.push(`[${text}](${text_url})`);
                    } else if (child.name == "bold") {
                        console.log("bold")
                        content.push("**" + child.children[0].text.trim() + "**");
                    }
                }
                content.push("\n\n")
            } else if (item.name == "list") {

                for (child in item.children) {
                    child = item.children[child]
                    content.push(" . ")
                    for (subChild in child.children) {
                        subChild = child.children[subChild]
                        if (subChild.name == "text") {
                            content.push(subChild.text.trim() + " ")
                        } else if (subChild.name == "link") {
                            text = subChild.children[0].children[0].text;
                            text_url = subChild.children[2].attributes[1].value;
                            if (text_url.startsWith("https://www.bbc.co.uk/news/live/world-europe-") || text_url.startsWith("https://www.bbc.co.uk/news/world-europe-")) {
                                newsJSON.news_url = text_url.split("-")[5];
                                console.log(`Changing news url to ${newsJSON.news_url}`);
                                break
                            }
                            content.push(`[${text}](${text_url})`)

                        } else if (subChild.name == "bold") {
                            content.push("**" + subChild.children[0].text.trim() + "**")
                        }
                    }

                }
                content.push("\n\n")
            } else if (item.name == "link") {
                text = item.children[0].children[0].text;
                text_url = item.children[2].attributes[1].value;
                if (text_url.startsWith("https://www.bbc.co.uk/news/live/world-europe-") || text_url.startsWith("https://www.bbc.co.uk/news/world-europe-")) {
                    newsJSON.news_url = text_url.split("-")[5];
                    console.log(`Changing news url to ${newsJSON.news_url}`);
                    break
                }
                content.push(`[${text}](${text_url})`)
            } else if (item.name == "video") {
                content.push("*There is a video, but the bot cannot display it. Please click on the link above to view it.*\n\n")
            } else if (item.name == "quote") {
                if (item.children[0].name == "quoteText") {
                    content.push("\"" + item.children[0].children[0].text.replace("\"", "") + "\"\n\n")
                }
            } else if (item.name == "embed"){
                try {
                    if (item.children[0].children[0].text == "twitter"){
                        tUrl = item.children[1].children[0].text
                        content.push(`[Twitter](${tUrl})\n\n`)
                    }
                } catch (e) {
                    console.log("No twitter embed")
                }
            }
        }

        console.log(`New news: ${title}`);
        //convert the Array to a string
        content.forEach(function (item, index, array) {
            array[index].trim()
        });
        content = content.join(" ");
        console.log(content);
        console.log(`${imageUrl}`);
        console.log(`${isBreaking}`);
        console.log(`https://www.bbc.co.uk/news/live/world-europe-${newsJSON.news_url}?pinned_post_locator=${post_locator}`);
        console.log(`${updated}`);

        //save to file
        fs.writeFile('./news.json', JSON.stringify(newsJSON), (err) => {
            if (err) throw err;
            console.log('News saved to file');
        });
    });
}

module.exports = {
    getData
}