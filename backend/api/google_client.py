import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_place_info(address, api_key) :
    #Base URL
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

    params = {
        "input": address,
        "inputtype": "textquery", 
        "fields": "formatted_address,name,business_status,place_id",
        "key": api_key, 
    }
    #Send request and capture response
    response = requests.get(base_url, params=params)
    #Check if request was successful
    if response.status_code != 200:
        return None
    
    data = response.json()

    if data["status"] != "OK" or not data["candidates"]:
        return None
    
    place = data["candidates"][0]

    return {
        "name": place["name"],
        "address": place["formatted_address"],
        "place_id":place["place_id"]
    }
        
    
api_key = os.getenv("GOOGLE_PLACES_API_KEY")
address = "Rubys Cafe SOHO"
place_info = get_place_info(address, api_key)


if place_info is not None:
    print(place_info)
else:
    print("Failed to get a response from Google Places API")