import requests
import yaml
import os
from bs4 import BeautifulSoup, Tag

PROTOTYPE=True

def get_lowest_prices(soup: BeautifulSoup, volumes: list[str]) -> dict[str, float]:
    volumes_ml = [str(volume)+' ml' for volume in volumes]

    def is_target_volume(tag: Tag) -> bool:
        if tag.name == 'a' and 'variant-tile' in tag.get('class', []):
            volume_tag = tag.find('div', class_='variant-tile-title')
            if volume_tag:
                volume = volume_tag.text.strip()
                return volume in volumes_ml
        return False

    target_volumes = soup.find_all(is_target_volume)
    lowest_prices = {}
    for volume in target_volumes:
        title = volume.find('div', class_='variant-tile-title').text.strip()
        price = volume.find('div', class_='variant-tile-subtitle price').text.strip()
        lowest_prices[title.rstrip('ml').strip()] = float(price.lstrip('od').rstrip('zł').strip())
    return lowest_prices

def scrap(url: str, htmlpath: str):
    if PROTOTYPE:
        with open(htmlpath, "r", encoding="utf-8") as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")
    else:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
    return soup

def get_fragrance_list() -> dict:
    with open(os.path.join(os.pardir, 'cfg', 'fragrances.yaml')) as f:
        return yaml.safe_load(f)
    
def main():
    frags = get_fragrance_list()

    for brand in frags['brands']:
        for fragrance in brand['fragrances']:
            lowest_prices = get_lowest_prices(
                scrap(None, fragrance['tmp_p']),
                fragrance['volumes'].keys()
            )
            print(lowest_prices)
            print(fragrance['volumes'])

if __name__=='__main__':
    main()