import requests
import random
from bs4 import BeautifulSoup as bs
def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # получаем ответ HTTP и создаем объект soup
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies
free_proxies = get_free_proxies()
print(f'Обнаружено бесплатных прокси - {len(free_proxies)}:')
for i in range(len(free_proxies)):
    print(f"{i+1}) {free_proxies[i]}")