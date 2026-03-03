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
        
def get_place_details(place_id, api_key) :
    
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "place_id": place_id,
        "fields": "business_status,formatted_address,name,editorial_summary,photos,price_level,rating,reviews,url,serves_vegetarian_food",
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        return None
    
    data = response.json()

    if data["status"] != 'OK':
        return None
    
    place = data["result"]

    #figure out how to add photos
    return {
        "business_status": place.get("business_status"),
        "formatted_address": place.get("formatted_address"),
        "name": place.get("name"),
        "editorial_summary": place.get("editorial_summary", {}).get("overview"),
        "price_level": place.get("price_level"),
        "rating": place.get("rating"),
        "reviews": place.get("reviews"),
        "url": place.get("url"),
        "serves_vegetarian_food": place.get("serves_vegetarian_food")
    }

    