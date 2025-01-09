import requests
def get_google_route(api_key, origin, destination, waypoints=[]):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "waypoints": "|".join(waypoints),
        "key": api_key,
        "traffic_model": "best_guess",
        "departure_time": "now",
        "mode": "driving"
    }
    response = requests.get(url, params=params)
    return response.json()
