import json

import requests

store_as = "youtube_1"


def load_web(web_site="https://www.youtube.com/"):
    web_data = requests.get(web_site)

    print(web_data.text)

    open(f"data/{store_as}.html", "w").write(web_data.text)


def scrap_rich_item_renderer(rich_item_renderer):
    title_list = []
    contents_video_renderer = rich_item_renderer["content"]["videoRenderer"]
    contents = contents_video_renderer["title"]["runs"]
    for content in contents:
        try:
            video_info = {
                "title": content["text"],
                "videoId": contents_video_renderer["videoId"],
                "viewCountText": None,
            }
            if "runs" in contents_video_renderer["viewCountText"]:
                video_info["viewCountText"] = "".join([z["text"] for z in contents_video_renderer[
                    "viewCountText"]["runs"]])
            elif "simpleText" in contents_video_renderer["viewCountText"]:
                video_info["viewCountText"] = contents_video_renderer["viewCountText"]["simpleText"]

            title_list.append(video_info)
        except Exception as e:
            print(e)
            print(content["text"], contents_video_renderer)

    return title_list


def scrap_web_from_html():
    lt_text = []

    web_data = open(f"data/{store_as}.html", "r").read()
    web_data = web_data.split("</script>")
    print(len(web_data))
    for x in web_data:
        try:
            x = x.lstrip('<script nonce="P5DjENHJc06CPI-4OKyDBw">var ytInitialData = ')
            x = x.rstrip(";")
            x = json.loads(x)
            contents_tabs = x["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
            for tabs in contents_tabs:
                contents_rich_grid_renderer = tabs["tabRenderer"]["content"]["richGridRenderer"]["contents"]
                for rich_grid_renderer in contents_rich_grid_renderer:
                    if "richItemRenderer" in rich_grid_renderer:
                        lt_text.extend(scrap_rich_item_renderer(rich_grid_renderer["richItemRenderer"]))
        except Exception as e:
            print(e)

    return lt_text


if __name__ == "__main__":
    load_web()
    output = scrap_web_from_html()
    open(f"data/{store_as}_final_output.json", "w").write(json.dumps(output, indent=4))