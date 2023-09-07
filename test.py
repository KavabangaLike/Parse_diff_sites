import requests

url = "https://scrape.smartproxy.com/v1/tasks"

payload = {
    "target": "universal",
    "headless": "html",
    "url": "https://www.facebook.com/marketplace/112356482109204/search?sortBy=creation_time_descend&query=house for rent &exact=false&latitude=-8.5181&longitude=115.2637&radius=10"
}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Basic VTAwMDAxMTk0ODY6UCRXMWUyNDdhNDU2MzA2MWYyZTc0MDc5Mzc5MmNiM2YwY2Nl"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)