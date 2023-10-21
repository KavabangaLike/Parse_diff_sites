from apify_client import ApifyClient
import requests
import json


def apify_request(url: str) -> str:
    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_Mf0M5vgPSxKHanwrKyIYvlpS1OBwd02Tz6V6")
    # print(url)
    # Prepare the Actor input
    run_input = {
        "startUrls": [{"url": url}],
        "headers": {"Viewport-Width:": 3465345, "Content-Length": 124312},
        "priceMin": 0,
        "priceMax": 0,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("shmlkv/facebook-marketplace").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    return str([*client.dataset(run["defaultDatasetId"]).iterate_items()])


def smartproxy_request(url_: str) -> str:
    url = "https://scrape.smartproxy.com/v1/tasks"

    payload = {
        "target": "universal",
        "headless": "html",
        "url": f"{url_}"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Basic VTAwMDAxMjY5ODM6UCRXMWU5Y2U4ODljMTU2M2E5OTUyMTZmZGY0MWVmZWViYmIw"
        # "Authorization": "Basic VTAwMDAxMjM2NDY6UCRXMTU5NjUzNDE1MzE5NGEyYzdlYmNjZWIxNDIyMTUyZDNm"

    }

    re = requests.request("POST", url, json=payload, headers=headers).text
    return str(json.loads(re)['results'][0]['content'])
