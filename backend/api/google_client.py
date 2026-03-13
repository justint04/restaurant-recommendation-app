import requests
import os
from dotenv import load_dotenv

load_dotenv()
def get_place_info(address, api_key) :
    #Base URL
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

    #these are the parameters we want to retrieve from a place info call
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

    #return the results of our place_info call 
    return {
        "name": place["name"],
        "address": place["formatted_address"],
        "place_id":place["place_id"]
    }

#core part of our project, user should be able to type a query like "indian food in brooklyn"
#this will help us achieve that
def search_restaurants_by_location(query, api_key): 
    base_url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-key": api_key,
        "X-Goog-Field-Mask": "places.id,places.displayName,places.formattedAddress, places.rating"  
    }

    body = {
        "textQuery": query,
        "includedType": "restaurant",
        "maxResultCount": 5
    }

    response = requests.post(base_url, headers=headers, json=body)
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}")
        return []
    
    data = response.json()
    results = []

    for place in data.get("places", []):
        results.append({
            "name": place.get("displayName", {}).get("text"),
            "address": place.get("formattedAddress"),
            "place_id": place.get("id"),
            "rating": place.get("rating"),
        })
    return results

PRICE_MAP = {
    "PRICE_LEVEL_FREE": 0,
    "PRICE_LEVEL_INEXPENSIVE": 1,
    "PRICE_LEVEL_MODERATE": 2,
    "PRICE_LEVEL_EXPENSIVE": 3,
    "PRICE_LEVEL_VERY_EXPENSIVE": 4
}

def get_place_details(place_id, api_key) :
    #place details url from google places documentation
    base_url = f"https://places.googleapis.com/v1/places/{place_id}"

    headers = {
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "id,displayName,formattedAddress,businessStatus,editorialSummary,priceLevel,rating,reviews,regularOpeningHours,websiteUri,servesVegetarianFood"
    }

    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}")
        return None
    
    place = response.json()
    #return the result of our place_detail call 
    return {
        "business_status": place.get("businessStatus"),
        "formatted_address": place.get("formattedAddress"),
        "name": place.get("displayName", {}).get("text"),
        "editorial_summary": place.get("editorialSummary", {}).get("text"),
        "price_level": place.get("priceLevel"),
        "rating": place.get("rating"),
        "reviews": place.get("reviews", []),
        "url": place.get("googleMapsUri"),
        "serves_vegetarian_food": place.get("servesVegetarianFood")
    }
