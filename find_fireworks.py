import requests
import json

def find_fireworks_entity():
    # Magic Kingdom Park ID (from previous output)
    mk_park_id = "75ea578a-adc8-4116-a54d-dccb60765ef9"
    url = f"https://api.themeparks.wiki/v1/entity/{mk_park_id}/children"
    
    try:
        print(f"Fetching children from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        children = data.get('children', [])
        print(f"Found {len(children)} children.")
        
        fireworks = []
        for child in children:
            name = child.get('name', '').lower()
            entity_type = child.get('entityType', '')
            if 'fireworks' in name or 'happily ever after' in name or 'enchantment' in name or 'wishes' in name:
                fireworks.append(child)
                print(f"Found candidate: {child['name']} ({child['id']}) - {entity_type}")
        
        if not fireworks:
            print("No obvious fireworks shows found. Dumping all 'SHOW' types:")
            for child in children:
                if child.get('entityType') == 'SHOW':
                    print(f"Show: {child['name']} ({child['id']})")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_fireworks_entity()
