import requests
import pandas as pd
import os

API_KEY = "4939008a97msh16b09b1f9f4e72dp1e5930jsn5c960d50051d"

def get_comments(video_id):
    url = "https://youtube138.p.rapidapi.com/video/comments/"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "youtube138.p.rapidapi.com"
    }
    
    params = {"id": video_id, "hl": "en", "gl": "US"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    comments = []
    for item in data.get("comments", []):
        comments.append({
            "text": item.get("content", ""),
            "likes": item.get("votes", {}).get("simpleText", "0"),
            "date": item.get("publishedTimeText", "")
        })
    
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(comments)
    df.to_csv("data/comments.csv", index=False)
    print(f"Saved {len(df)} comments!")
    return df

# Test with a YouTube video
video_id = "dQw4w9WgXcQ"
get_comments(video_id)