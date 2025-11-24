import requests
import json

def check_hea():
    # Happily Ever After ID
    hea_id = "22b78ed9-a692-47cb-b6a4-6d1224ff67e3"
    url = f"https://api.themeparks.wiki/v1/entity/{hea_id}/schedule"
    
    try:
        print(f"Fetching schedule for HEA ({hea_id})...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print(json.dumps(data, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_hea()
