import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("MY_API_KEY")

CHANNEL_HANDLE = "MrBeast"


def get_playlist_id():

    try:

        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        channel_items = data['items'][0]
        channel_plalist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']

        print(channel_plalist_id)
        return channel_plalist_id
    
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching the playlist ID.")  
        raise e
    


if __name__ == "__main__":
    #print("get_playlist_id() will be executed")
    get_playlist_id()


""" 
else:
    print( "the function won't be executed from anything other than __name__ == '__main__'" ) 
"""
