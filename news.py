import asyncio
import aiohttp
from console import Console
from datetime import datetime
from typing import Union

console = Console(True)

url = "https://push.api.bbci.co.uk/batch?t=%2Fdata%2Fbbc-morph-%7Blx-page-component-data%2F_mrrVersion%2F2.2.1%2FassetUri%2Fnews%252Flive%252Fworld-europe-60517447%2FisUk%2Ffalse%2FlayoutName%2Fdefault%2FpageNumber%2F1%2FserviceName%2Fnews%2Ftheme%2Fnews%2Fversion%2F15.6.0%2Clx-sign-in-data%2FassetUri%2Fnews%252Flive%252Fworld-europe-60517447%2Fversion%2F5.0.1%2Cfeature-toggle-manager%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FfeatureToggle%2Flx-live-guide-active-viewer%2Fproject%2Fbbc-live%2Fversion%2F1.0.3%2Cfeature-toggle-manager%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FfeatureToggle%2Flx-native-sign-in%2Fproject%2Fbbc-live%2Fversion%2F1.0.3%2Cfeature-toggle-manager%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FfeatureToggle%2Flx-related-sessions%2Fproject%2Fbbc-live%2Fversion%2F1.0.3%2Clx-heartbeat-count%2FassetId%2F60517447%2Fversion%2F2.1.2%2Cfeature-toggle-manager%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FfeatureToggle%2Flx-debate-banner%2Fproject%2Fbbc-live%2Fversion%2F1.0.3%2Clx-page-commentary-meta%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FisUk%2Ffalse%2Fversion%2F1.1.2%2Cfeature-toggle-manager%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FfeatureToggle%2Freactions-stream-v4%2Fproject%2Fbbc-live%2Fversion%2F1.0.3%2Cfeature-toggle-manager%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FfeatureToggle%2Fanimated-stream%2Fproject%2Fbbc-live%2Fversion%2F1.0.3%2Cfeature-toggle-manager%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FfeatureToggle%2Fmlfl-breaking-news%2Fproject%2Fbbc-live%2Fversion%2F1.0.3%2Clx-commentary-data-paged%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FisUk%2Ffalse%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F1%2FserviceName%2Fnews%2Fversion%2F1.5.6%2Clx-cps-more-from-data%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FisUk%2Ffalse%2Fversion%2F2.2.3%2Clx-commentary-data-paged%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FisUk%2Ffalse%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F2%2FserviceName%2Fnews%2Fversion%2F1.5.6%2Clx-commentary-data-paged%2FassetUri%2F%252Fnews%252Flive%252Fworld-europe-60517447%2FisUk%2Ffalse%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F8%2FserviceName%2Fnews%2Fversion%2F1.5.6%7D?timeout=5"

with open("latest", "r+") as f:
    latest_id = f.read()

async def get_data() -> Union[dict, None]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            global latest_id

            latest = data["payload"][11]["body"]["results"][0]

            # for i in data["payload"][11]["body"]["results"]:
            #     if i["assetId"] == "62197e41980bea49f4b7a024":
            #         latest = i

            if latest["assetId"] == latest_id:
                console.log("Latest update has already been posted.")
                return None

            latest_id = latest["assetId"]

            title = latest["title"]
            content = "" # Gotten later
            image_url = None
            is_breaking = latest["options"]["isBreakingNews"]
            post_locator = latest["locator"]
            updated = datetime.strptime(latest["lastUpdated"].rstrip(":"), "%Y-%m-%dT%H:%M:%S%z")

            # Image
            try:
                for image_key in latest["media"]["images"]["body"]:
                    image_url = latest["media"]["images"]["body"][image_key]["href"]
                    break
            except: image_url = None

            # Content
            for item in latest["body"]:

                if item["name"] == "paragraph":
                    if len(item["children"]) == 1:
                        content += item["children"][0]["text"] + "\n\n"

                    else:
                        for child in item["children"]:
                            if child["name"] == "text":
                                content += child["text"].replace("\n\n", " ")

                            if child["name"] == "link":
                                text = child["children"][0]["children"][0]["text"]
                                text_url = child["children"][2]["attributes"][1]["value"]

                                content += f"[{text}]({text_url}) "

                elif item["name"] == "list":
                    for list_item in item["children"]:
                        content += " - " + list_item["children"][0]["text"].strip() + "\n\n"

                elif item["name"] == "link":
                    text = item["children"][0]["children"][0]["text"]
                    text_url = item["children"][2]["attributes"][1]["value"]

                    content += f"[{text}]({text_url})\n\n"

                elif item["name"] == "video":
                    content += "*There is a video, but the bot cannot display it. Please click on the link above to view it.*\n\n"

                # TODO: Once the text is over 2000 chars long, replace the last 3 with ...
                if len(content) > 2000:
                    pass

            content = content.strip()

            with open("latest", "w+") as f:
                f.write(latest_id)

            return {
                "title": title,
                "content": content,
                "is_breaking": is_breaking,
                "image": image_url,
                "locator": post_locator,
                "updated": updated
            }

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_data())