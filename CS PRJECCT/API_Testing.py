import requests
import json

def get_random_cat_picture():
    try:
        
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        
        data = response.json()
        
        if data and 'url' in data[0]:
            return data[0]['url']
        else:
            return None
    except Exception as e:
        print(f"Error fetching cat picture: {e}")
        return None


cat_picture_url = get_random_cat_picture()
if cat_picture_url:
    print(f"Here's your random cat picture: {cat_picture_url}")


else:
    print("Failed to fetch cat picture.")
