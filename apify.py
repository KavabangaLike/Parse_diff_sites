from apify_client import ApifyClient


def apify_request(url: str) -> str:
    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_Mf0M5vgPSxKHanwrKyIYvlpS1OBwd02Tz6V6")
    # print(url)
    # Prepare the Actor input
    run_input = {
        "startUrls": [{"url": url}],
        "priceMin": 0,
        "priceMax": 0,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("shmlkv/facebook-marketplace").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    return str([*client.dataset(run["defaultDatasetId"]).iterate_items()])
