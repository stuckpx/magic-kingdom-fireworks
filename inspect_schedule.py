import requests
import json
from datetime import datetime

def check_schedule():
    # Magic Kingdom ID
    mk_id = "e957da41-3552-4cf6-b636-5babc5cbc4e5"
    url = f"https://api.themeparks.wiki/v1/entity/{mk_id}/schedule"
    
    try:
        print(f"Fetching schedule from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Save to file for inspection
        with open("mk_schedule.json", "w") as f:
            json.dump(data, f, indent=2)
            
        print("Schedule saved to mk_schedule.json")
        
        # Print first few items to see structure
        print("\nSample Schedule Items:")
        schedule = data.get('schedule', [])
        for item in schedule[:5]:
            print(json.dumps(item, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_schedule()
