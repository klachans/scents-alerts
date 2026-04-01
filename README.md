# scents-alerts
Python scraper that monitors fragrance prices on [perfumehub.pl](https://perfumehub.pl/) and
sends a Discord alert when they drop below your target price.

## What is does
* Script scrapes data for each fragrance and volume
* Lets you define your own watchlist (YAML)
* If fragrance with specific volume drops below your price threshold, sends Discord webhook notification
* Runs:
  * locally (your own `watchlist.yaml`)
  * automatically via GitHub Actions (daily at 8:01am UTC by default, but can be adjusted)

## Setup (local)
1. Clone repo, install dependencies
```
git clone https://github.com/klachans/scents-alerts.git
cd scents-alerts
pip install -r requirements.txt
```
2. Create `.env`
```
DISCORD_WEBHOOK_URL=your_webhook
```
Intro to weebhooks: https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

3. Edit your watchlist `cfg/watchlist.yaml`
Example:
```
brands:
  - brand: "Tom Ford"
    fragrances:
      - name: "Neroli Portofino"
        url: "https://perfumehub.pl/..."
        volumes:
          100: 750
          50: 500
```
`url` - url to fragrance on perfumehub (check all variants option!)

`volumes` - `volume[ml]: price_threshold[pln]` format

4. Run
```
python src/main.py
```
---
## GitHub Actions (auto mode)
Runs daily at 8:01am UTC via cron:
```
cron: '1 8 * * *'
```
If you prefer to run on different schedule, edit `.github\workflows\daily-scents-alerts.yaml`

__Required secrets:__
* `DISCORD_WEBHOOK_URL`
* `MY_WATCHLIST` - your full YAML config (same as `watchlist.yaml`)

The workflow:
* overwrites `cfg/watchlist.yaml` with your secret
* runs scraper
* sends alerts if `found price ≤ threshold price`
