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

re_ascii_alpha = re.compile(r"^[a-zA-Z]+$", re.V1)

@dc.dataclass(init=True)
class LyricsWindow:

    root: tk.Tk = dc.field(init=False, default=None)

    lyrics: str = dc.field(init=True)
    title: str = dc.field(init=True)

    def __post_init__ (self) -> None:
        self.root = tk.Tk()

        self.root.title(self.title)
        self.root.resizable(width=True, height=True)

        T = tk.Text(self.root, bg="#333")

        T.pack(expand=True, fill=tk.BOTH)
        T.tag_config("lyrics", foreground="#999")
        T.insert(tk.END, self.lyrics, "lyrics")

        T.config(state=tk.DISABLED)

        self.root.mainloop()

def load_song():

    if len(sys.argv) == 2:
        music, artist = sys.argv[1].split("|")

        artist = artist[ : artist.find(",") ]

        artist = unidecode(artist)
        music = unidecode(music)

    else:
        artist = sys.argv[1]
        music = sys.argv[2]

    key = os.environ["APPKEY"]

    url = f"https://api.vagalume.com.br/search.php?art={artist}&mus={music}&apikey={key}"
    resp = requests.post(url)

    resp_j = json.loads(resp.text)

    return resp_j["mus"][0]["text"], artist + " " + music

if __name__ == "__main__":

    lyrics, title = load_song()

    window = LyricsWindow(lyrics, title)
