import requests
from fake_useragent import UserAgent

USER_AGENT = UserAgent()
print(USER_AGENT.random)

def search_lyrics(lyrics):
    