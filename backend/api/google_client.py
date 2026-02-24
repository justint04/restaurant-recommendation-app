import requests
def get_place_info(address, api_key) :
    #Base URL
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=<address_input>&inputtype=textquery&fields=formatted_address%2Cname%2Cbusiness_status%2Cplace_id&key=<api_key>"
    params = {
        "input": address,
        "inputtype": "textquery", 
        "fields": "formatted_address, name, business_status, place_id",
        "key": api_key, 
    }
    #Send request and capture response
    response = requests.get(base_url, params=params)
    #Check if request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
api_key = 
address = "219 Mulberry Street, New York, NY 10012"
place_info = get_place_info(address, api_key)
if place_info is not None:
    print(place_info)
else:
    print("Failed to get a response from Google Places API")