import requests
import json

def check_minnie():
    # Minnie's Wonderful Christmastime Fireworks ID
    minnie_id = "bb28947d-a747-44f0-ac71-1fa8188f4cee"
    url = f"https://api.themeparks.wiki/v1/entity/{minnie_id}/schedule"
    
    try:
        print(f"Fetching schedule for Minnie's ({minnie_id})...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print(json.dumps(data, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_minnie()
