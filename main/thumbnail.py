import requests

def fetch_thumbnail_response(video_id):
    """Fetches the max resolution YouTube thumbnail and returns the response object."""
    thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
    try:
        response = requests.get(thumbnail_url)
        response.raise_for_status() # Check if the download was successful
        return response 

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the thumbnail: {e}")
        return None
    
 