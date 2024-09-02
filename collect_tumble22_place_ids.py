import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def load_locations():
    locations_raw = os.getenv('RESTAURANT_LOCATIONS')
    print(f"Raw RESTAURANT_LOCATIONS: {locations_raw}")  # Debug print
    
    # Remove any newline characters and extra whitespace
    locations_clean = locations_raw.replace('\n', '').strip()

    try:
        # Attempt to parse as JSON
        locations = json.loads(locations_raw)
        
        if isinstance(locations, list):
            print(f"Parsed {len(locations)} locations")  # Debug print
            return locations
        else:
            print("RESTAURANT_LOCATIONS is not a list")  # Debug print
            return [locations_raw]
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")  # Debug print
        return []

def get_place_id(api_key, location):
    base_url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress"
    }
    data = {
        "textQuery": f"Tumble 22 {location}"
    }
    response = requests.post(base_url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if 'places' in result and result['places']:
            place = result['places'][0]
            return {
                "name": place.get('displayName', {}).get('text', ''),
                "address": place.get('formattedAddress', ''),
                "place_id": place.get('id', '')
            }
    print(f"Error for {location}: {response.text}")
    return None

def update_env_file(place_ids):
    with open('.env', 'r') as file:
        lines = file.readlines()
    
    with open('.env', 'w') as file:
        place_ids_updated = False
        for line in lines:
            if line.startswith('PLACE_IDS='):
                file.write(f'PLACE_IDS={json.dumps(place_ids)}\n')
                place_ids_updated = True
            else:
                file.write(line)
        
        if not place_ids_updated:
            file.write(f'PLACE_IDS={json.dumps(place_ids)}\n')

def main():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("API key not found. Please check your .env file.")
        return

    locations = load_locations()
    if not locations:
        print("No Tumble 22 locations found. Please check your .env file.")
        return

    print(f"Loaded locations: {locations}")  # Debug print
    print("Fetching Place IDs for Tumble 22 locations...")
    place_ids = []

    for location in locations:
        print(location)
        print("\n")
        print(f"\nProcessing: {location}")
        result = get_place_id(api_key, location)
        if result:
            place_ids.append(result)
            print(f"Found: {result['name']}")
            print(f"Address: {result['address']}")
            print(f"Place ID: {result['place_id']}")
        else:
            print(f"No result found for {location}")

    if place_ids:
        update_env_file(place_ids)
        print("\nPlace IDs for Tumble 22 locations have been updated in the .env file.")
    else:
        print("\nNo Place IDs were found.")

if __name__ == "__main__":
    main()