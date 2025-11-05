import requests
import json
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("MY_API_KEY")

CHANNEL_HANDLE = "MrBeast"
maxResults = 50

# this function returns the playlist ID of the channel uploads.
def get_playlistid():
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        channel_playlistid = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        print(channel_playlistid)
        return channel_playlistid
    
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching the playlist ID.")  
        raise e

# this function returns the video IDs for the above returned playlist ID.
def get_videoIDs(playlistid):

    #create the base URL for fetching playlist items using above obtained playlist ID.
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistid}&key={API_KEY}"  

    video_ids = []
    pageToken = None
    
    try:            
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            for item in data['items']:
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            
            pageToken = data.get('nextPageToken')
            if not pageToken:
                break
        
        print(video_ids)
        return video_ids
    
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching video IDs.")  
        raise e

# this function returns the video stats/ detailed data for the above returned video IDs.
def extract_video_data(video_ids):
    extract_data = []
    
    def batch_list(video_id_list, batch_size):
        for video_id in range(0, len(video_id_list), batch_size):
            yield video_id_list[video_id : video_id + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
                        
                video_data = {
                    "video_id": video_id,
                    "title": snippet.get("title"),
                    "publishedAt": snippet.get("publishedAt"),
                    "duration": contentDetails.get("duration"),
                    "viewCount": statistics.get("viewCount", None),
                    "likeCount": statistics.get("likeCount", None),
                    "commentCount": statistics.get("commentCount", None)
                }
        
                extract_data.append(video_data)

        return extract_data
    
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching video data.")  
        raise e

# save the extracted data to a JSON file.
def save_to_json(extracted_data):
    file_path = f"./data/yt_data_{date.today().isoformat()}.json"
    with open(file_path, "w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # Call the function to get the playlist ID and save it to a variable.
    playlistid = get_playlistid()
    video_ids = get_videoIDs(playlistid)
    video_data = extract_video_data(video_ids)
    save_to_json(video_data)

