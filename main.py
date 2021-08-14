import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs4

USER_AGENT = UserAgent()
print(USER_AGENT.random)


def search_lyrics(lyrics):
    headers = {
        "User-Agent": USER_AGENT.random,
    }
    base_url = "https://songsear.ch/q/"
    lyrics = lyrics.replace(" ", "+")
    search_url = f"{base_url}{lyrics}"

    request = requests.get(search_url, headers=headers)

    if request.status_code == 200:
        soup = bs4(request.content, 'html.parser')
