
import requests
from urllib.parse import urlencode
import json
api_key = "AIzaSyAPOOnlu8YXdWsyM3uUkz3tU7AeDWgoQqA"


landmarks={}
with open('./cityLandmarks.json') as f:
  landmarks = json.load(f)
endpoint="https://maps.googleapis.com/maps/api/directions/json"
stops="|".join(landmarks["Hong Kong"][1:3])
params = {
    "key": api_key,
    "origin":"The Peninsula Hong Kong",
    "destination":"The Peninsula Hong Kong",
    "waypoints":"optimize:true|"+stops
}
url_params = urlencode(params)
url = f"{endpoint}?{url_params}"
r = requests.get(url)
print(json.dumps(r.json(),indent=4))

def extract_lat_lng(address_or_postalcode, data_type = 'json'):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": address_or_postalcode, "key": api_key}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200, 299): 
        return {}
    latlng = {}
    try:
        latlng = r.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlng.get("lat"), latlng.get("lng")


lat,lng = extract_lat_lng("Victoria Peak")

base_endpoint_places = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

params = {
    "key": api_key,
    "location":f"{lat},{lng}",
    "radius":"2000",
    "type":"restaurant",
    "rankby":"prominence"
    }
params_encoded = urlencode(params)
places_endpoint = f"{base_endpoint_places}?{params_encoded}"
r = requests.get(places_endpoint)
#print(r.json()["results"][0])