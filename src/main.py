import requests
import yaml
import os
from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv
import notificators

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

def scrap(url: str) -> BeautifulSoup:
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return BeautifulSoup(r.text, 'html.parser')

def get_watchlist() -> dict:
    with open(os.path.join(os.pardir, 'cfg', 'watchlist.yaml')) as f:
        return yaml.safe_load(f)

def find_fragrances_below_price(tracked: dict):
    for brand in tracked['brands']:
        for fragrance in brand['fragrances']:
            current_prices = get_lowest_prices(
                scrap(url=fragrance['url']),
                fragrance['volumes'].keys()
            )
            thresholds = dict(
                sorted(
                    fragrance['volumes'].items(),
                    key=lambda x: x[0],
                    reverse=True
                )
            )
            for volume, price_threshold in thresholds.items():
                current_price = current_prices.get(str(volume))
                if current_price:
                    if current_price<=price_threshold:
                        notificators.discord(
                            brand=brand['brand'],
                            fragrance=fragrance['name'],
                            volume=volume,
                            current_price=current_price,
                            url=fragrance['url']
                        )

def main():
    load_dotenv()
    find_fragrances_below_price(get_watchlist())

if __name__=='__main__':
    main()
