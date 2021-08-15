import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs4
import webbrowser
import speech_recognition as sr
import time


USER_AGENT = UserAgent()
HTML_PARSER = "html.parser"
SPEECH_RECOGNIZER = sr.Recognizer()


def listen_to_lyrics():
    with sr.Microphone() as source:
        print("Listening..")
        lyrics_audio = SPEECH_RECOGNIZER.listen(source)
        print("Processing..")

        try:
            lyrics_audio_string = SPEECH_RECOGNIZER.recognize_google(
                lyrics_audio)
            print("Lyrics: " + lyrics_audio_string)
            return lyrics_audio_string
        except:
            print("Sorry, I did not get that")
            lyrics_string = input("Lyrics: ")
            return lyrics_string


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
        soup = bs4(request.content, HTML_PARSER)

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

    user_song_url = f"https://songsear.ch{user_song_url_raw}"

    return user_song_url


def get_complete_lyrics(lyrics_url):
    headers = {
        "User-Agent": USER_AGENT.random,
    }

    request = requests.get(lyrics_url, headers=headers)

    if request.status_code == 200:
        soup = bs4(request.content, HTML_PARSER)

    song_link = request.url
    info_song_link = song_link.split("/")
    song_artist = info_song_link[4].replace("-", " ")
    song_name = info_song_link[5].replace("-", " ")

    lyrics_blockquote = soup.find("blockquote")
    lyrics_blockquote_string = str(lyrics_blockquote)
    negatives = ["<blockquote>", "</blockquote>", "<br/>"]
    for negative in negatives:
        lyrics_blockquote_string = lyrics_blockquote_string.replace(
            negative, "\n")

    lyrics = lyrics_blockquote_string

    # write lyrics to file!
    with open(f"{song_name.upper()} - {song_artist}.txt", "wb") as file:
        file.write(lyrics.encode("utf-8"))

    verses = lyrics.split("\n")
    for verse in verses:
        print(verse)
        time.sleep(0.5)


def play_on_youtube(song_link):
    info_song_link = song_link.split("/")
    song_artist = info_song_link[4].replace("-", " ")
    song_name = info_song_link[5].replace("-", " ")
    webbrowser.open_new(
        f"https://www.youtube.com/results?search_query={song_name}+by+{song_artist}")


def main():
    user_lyrics = listen_to_lyrics()
    song_links = song_info_from_lyrics(user_lyrics)
    user_choosed_song = user_song_of_choice(song_links)
    get_complete_lyrics(user_choosed_song)
    play_on_youtube(user_choosed_song)


if __name__ == '__main__':
    main()
