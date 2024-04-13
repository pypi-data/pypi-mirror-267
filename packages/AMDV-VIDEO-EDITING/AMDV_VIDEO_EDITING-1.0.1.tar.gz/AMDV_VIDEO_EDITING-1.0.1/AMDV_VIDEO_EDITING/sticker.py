import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

def stickers_packs(limit=100, offset=0):
    api_key = os.getenv("GIPHY_API_KEY")
    if not api_key:
        raise ValueError("GIPHY_API_KEY not found in .env file")

    url = f"https://api.giphy.com/v1/stickers/packs/3138/stickers"
    params = {
        "api_key": api_key,
        "limit": limit,
        "offset": offset
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch stickers. Status code: {response.status_code}")
        return None

    data = response.json()
    return data

# Example usage:
# stickers_data = fetch_stickers(limit=100, offset=0)
# print(stickers_data)
