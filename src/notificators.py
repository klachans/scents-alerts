import os
import requests

def discord(brand, fragrance, volume, current_price, url):
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    if not webhook_url:
        print('Error: Discord Webhook URL missing from .env file.')
        return

    discord_payload = {
        'embeds': [
            {
                'title': f'🚨 PRICE DROP: {brand} {fragrance}',
                'description': (
                    f'**Volume:** {volume} ml\n'
                    f'**Current Price:** {current_price:.2f} PLN\n'
                    f'🛒 **[Click here to go to the price comparison]({url})**'
                ),
                'color': 5763719
            }
        ]
    }

    try:
        print(f'Attempting to send Discord alert for {brand} {fragrance}...')
        response = requests.post(webhook_url, json=discord_payload)
        response.raise_for_status() 
        print('Discord notification sent successfully!')
        
    except requests.exceptions.RequestException as e:
        print(f'Failed to send Discord alert. Error: {e}')
