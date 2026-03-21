import requests
import yaml
import os
from bs4 import BeautifulSoup


def save_html(url: str, filename: str):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    with open(filename, "w", encoding="utf-8") as file:
        file.write(r.text)
        
    print(f"Pomyślnie zapisano do pliku {filename}")

def load_html_from_file(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    return soup

save_html("https://perfumehub.pl/french-avenue-platine-blanc-ekstrakt-perfum-unisex?all=true", "platineblanc.html")
soup = load_html_from_file("platineblanc.html")
