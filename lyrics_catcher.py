import dotenv
import json
import os
import requests
import sys

import dataclasses as dc
import regex as re
import tkinter as tk

from pathlib import Path
from unidecode import unidecode

base_path = Path(__file__).resolve().parent
dotenv.load_dotenv(base_path / ".env", override=False)

@dc.dataclass(init=True)
class LyricsWindow:

    root: tk.Tk = dc.field(init=False, default=None)

    lyrics: str = dc.field(init=True)
    title: str = dc.field(init=True)

    def __post_init__ (self) -> None:
        self.root = tk.Tk()

        self.root.title(self.title)
        self.root.resizable(width=True, height=True)

        T = tk.Text(self.root, bg="#333", padx=25, pady=25, font=("Linux Biolinum", 12))

        T.pack(expand=True, fill=tk.BOTH)

        T.tag_config("lyrics", foreground="#999")
        T.tag_config("title", foreground="#999", font=("Linux Biolinum", 16, "bold"))

        T.insert(tk.END, self.title + '\n', "title")
        T.insert(tk.END, self.lyrics, "lyrics")

        T.config(state=tk.DISABLED)

        self.root.mainloop()

def load_song():

    if len(sys.argv) == 2:
        music, artists = sys.argv[1].split("|")

        artists = [ unidecode(artist.strip()) for artist in artists.split(",") ]
        music = unidecode(music)
    else:
        artists = [ sys.argv[1] ]
        music = sys.argv[2]

    key = os.environ["APPKEY"]

    for artist in artists:

        url = f"https://api.vagalume.com.br/search.php?art={artist}&mus={music}&apikey={key}"
        resp = requests.post(url)
        try:
            resp_json = json.loads(resp.content)
            if resp_json["type"] != "song_not_found":
                return resp_json["mus"][0]["text"], artist + " - " + music
        except:
            if resp.status_code != 200:
                print("Error with connection with Vagalume API")
                return None
            continue

    return None

if __name__ == "__main__":

    try:
        lyrics, title = load_song()

        window = LyricsWindow(lyrics, title)
    except:
        print("Song not Found")
