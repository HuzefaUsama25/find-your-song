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


def user_song_of_choice(song_links):
    song_index = 0
    for song_link in song_links:

        info_song_link = song_link.split("/")
        song_artist = info_song_link[2].replace("-", " ")
        song_name = info_song_link[3].replace("-", " ")
        info_string = f"{song_index} - {song_artist} - {song_name}"

        if len(str(song_index)) == 1:
            print(f"0{info_string}")

        else:
            print(info_string)

        song_index += 1

    while True:
        try:
            user_choice_of_song = int(input("Song Index: "))
            user_song_url_raw = song_links[user_choice_of_song]
            break

        except Exception as e:
            print("\nenter the index of song you want to listen")
            continue

    user_song_url = f"https://songsear.ch/q{user_song_url_raw}"

    return user_song_url
