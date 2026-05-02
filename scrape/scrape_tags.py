from requests import get
from json import dumps
import re
from bs4 import BeautifulSoup

html_url = "https://store.steampowered.com/app/2121980"

headers = headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i"
}

def q_get_tags():
    # get html
    response = get(html_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    tags = [tag.get_text(strip=True) for tag in soup.select(".glance_tags a.app_tag")]
    return tags

if __name__ == "__main__":
    with open("test.txt", "w") as f:
        for tag in q_get_tags():
            f.write(tag + "\n")
