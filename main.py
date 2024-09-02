import os
import json
import requests
import csv
import time
from dotenv import load_dotenv

load_dotenv()

def get_place_ratings_reviews(api_key, place_id, max_reviews=100):
    base_url = "https://places.googleapis.com/v1/places"
    headers = {
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "id,displayName,formattedAddress,rating,userRatingCount,reviews"
    }
    
    url = f"{base_url}/{place_id}"
    all_reviews = []
    
    while len(all_reviews) < max_reviews:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            new_reviews = data.get('reviews', [])
            
            # Check for duplicate reviews
            new_unique_reviews = [review for review in new_reviews if review not in all_reviews]
            all_reviews.extend(new_unique_reviews)
            
            if not new_unique_reviews:
                # If no new unique reviews, we've probably got all available reviews
                break
            
            print(f"Fetched {len(all_reviews)} reviews so far")
            
            # Wait before making the next request to avoid rate limiting
            time.sleep(2)
        else:
            print(f"Error fetching details for place_id {place_id}: {response.text}")
            break
    
    return {
        "name": data.get('displayName', {}).get('text', ''),
        "address": data.get('formattedAddress', ''),
        "rating": data.get('rating', 'N/A'),
        "user_ratings_total": data.get('userRatingCount', 'N/A'),
        "reviews": all_reviews
    }

def load_place_ids():
    place_ids_json = os.getenv('PLACE_IDS', '[]')
    try:
        return json.loads(place_ids_json)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in PLACE_IDS environment variable")
        return []

def main():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("API key not found. Please check your .env file.")
        return

    place_ids = load_place_ids()
    if not place_ids:
        print("No Place IDs found. Please run the Place ID collection script first.")
        return

    print("Fetching ratings and reviews for Tumble 22 locations...")

    csv_file = 'tumble22_all_reviews.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'Location Name', 'Address', 'Overall Rating', 'Total Reviews',
            'Review Rating', 'Review Text', 'Review Time'
        ])
        writer.writeheader()

        for place in place_ids:
            place_id = place['place_id']
            print(f"\nProcessing: {place['name']}")
            details = get_place_ratings_reviews(api_key, place_id)
            
            if details:
                for review in details['reviews']:
                    writer.writerow({
                        'Location Name': details['name'],
                        'Address': details['address'],
                        'Overall Rating': details['rating'],
                        'Total Reviews': details['user_ratings_total'],
                        'Review Rating': review.get('rating', 'N/A'),
                        'Review Text': review.get('text', {}).get('text', 'No comment'),
                        'Review Time': review.get('relativePublishTimeDescription', 'N/A')
                    })
                print(f"Fetched {len(details['reviews'])} reviews for {details['name']}")
            else:
                print(f"No details found for {place['name']}")

    print(f"\nAll data exported to {csv_file}")

if __name__ == "__main__":
    main()