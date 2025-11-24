import requests
import json

def check_live():
    mk_id = "75ea578a-adc8-4116-a54d-dccb60765ef9"
    url = f"https://api.themeparks.wiki/v1/entity/{mk_id}/live"
    
    try:
        print(f"Fetching live data from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Save to file
        with open("mk_live.json", "w") as f:
            json.dump(data, f, indent=2)
            
        print("Live data saved to mk_live.json")
        
        # Look for show times in live data
        live_data = data.get('liveData', [])
        for item in live_data:
            name = item.get('name', '')
            if 'Fireworks' in name or 'Happily' in name:
                print(f"Found in live: {name} - {item}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_live()
