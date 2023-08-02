import requests

response = requests.get("https://www.facebook.com/marketplace/112356482109204/search/?sortBy=creation_time_descend&query=property&exact=false")
print(response.text)