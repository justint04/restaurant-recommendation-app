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
        
def get_place_details(place_id, api_key) :
    #place details url from google places documentation
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"

    #these are the parameters we want to retrieve from a place details call
    params = {
        "place_id": place_id,
        "fields": "business_status,formatted_address,name,editorial_summary,photos,price_level,rating,reviews,url,serves_vegetarian_food",
        "key": api_key
    }
    #call the api with place details and our listed params
    response = requests.get(base_url, params=params)

    #200 means good, anything else is usually an error
    if response.status_code != 200:
        return None
    
    #google places returns api calls with a json file
    data = response.json()

    if data["status"] != 'OK':
        return None
    
    #store data in place variable
    place = data["result"]


    #return the result of our place_detail call 
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

    