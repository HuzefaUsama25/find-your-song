import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs4

USER_AGENT = UserAgent()
print(USER_AGENT.random)


def song_info_from_lyrics(lyrics):
    headers = {
        "User-Agent": USER_AGENT.random,
    }
    song_links = list()
    lyrics = lyrics.replace(" ", "+")
    base_url = "https://songsear.ch/q/"
    search_url = f"{base_url}{lyrics}"

    request = requests.get(search_url, headers=headers)

    if request.status_code == 200:
        soup = bs4(request.content, 'html.parser')

    song_info_div_heads = soup.find_all(class_="head")

    for song_info_div_head in song_info_div_heads:
        song_link = song_info_div_head.find("a").get("href")
        song_links.append(song_link)

    return song_links


def list_songs(song_links):
    song_index = 0
    for song_link in song_links:

        info_song_link = song_link.split("/")

        # /song/Franz-Ferdinand/Auf-Achse/1027717

        song_artist = info_song_link[1]
        song_name = info_song_link[2]
        print(f"{song_index} - {song_artist} - {song_name}")

        song_index += 1
