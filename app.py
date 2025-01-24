import os
import folium
from flask import Flask, render_template, request, jsonify
from utils.routing import get_google_route
from utils.traffic import get_tomtom_traffic
from utils.weather import get_air_quality
from utils.weather import get_weather_and_rain
from utils.emissions import calculate_emissions
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

API_KEYS = {
    "google_maps": "KEY",
    "tomtom": "KEY",
    "aqicn": "KEY",
    "openweather":"KEY",
}

# Ensure the 'static' directory exists
if not os.path.exists('static'):
    os.makedirs('static')


# NEW FEATURE: Geocoding API to convert place names to coordinates
def geocode_place(api_key, place_name):
    """
    Fetch latitude and longitude for a given place name using Google Geocoding API.
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": place_name, "key": api_key}
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        if data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            return None, None  # No results found
    else:
        return None, None  # Handle API failure

def fetch_weather_data(location):
    api_key = "cc9d6173cb1b3ce8bfbed6683c850a67"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        raise Exception("Weather data unavailable")

    weather_description = response["weather"][0]["description"]
    rain = response.get("rain", {}).get("1h", 0)  # Rainfall in mm
    return {"description": weather_description, "rain": rain}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    origin = request.form['origin'].strip()
    destination = request.form['destination'].strip()

    # Geocode origin and destination
    try:
        origin_lat, origin_lon = geocode_place(API_KEYS['google_maps'], origin)
        if origin_lat is None:
            return render_template("error.html", error=f"Could not find location: {origin}")
        destination_lat, destination_lon = geocode_place(API_KEYS['google_maps'], destination)
        if destination_lat is None:
            return render_template("error.html", error=f"Could not find location: {destination}")
    except Exception as e:
        return render_template("error.html", error=f"Error geocoding locations: {e}")

    # Fetch Google Maps Route
    try:
        route_data = get_google_route(
            API_KEYS['google_maps'],
            f"{origin_lat},{origin_lon}",
            f"{destination_lat},{destination_lon}"
        )
        distance_km = route_data['routes'][0]['legs'][0]['distance']['value'] / 1000
        travel_duration_secs =route_data['routes'][0]['legs'][0]['duration']['value']
    except Exception as e:
        return render_template("error.html", error=f"Error fetching route: {e}")

    # Traffic Data
    traffic_level, traffic_description = "Not Available", "Not Available"
    try:
        traffic_data = get_tomtom_traffic(API_KEYS['tomtom'], origin_lat, origin_lon)
        traffic_level = traffic_data.get('flowSegmentData', {}).get('currentSpeed', traffic_level)
        traffic_description = traffic_data.get('flowSegmentData', {}).get('currentTravelTime', traffic_description) / 60
        traffic_description = f"{round(traffic_description, 2)}"

    except Exception as e:
        print(f"Error fetching traffic data: {e}")


    # Air Quality
    aqi, pm10, pm25 = "N/A", "N/A", "N/A"
    try:
        air_quality = get_air_quality(API_KEYS['aqicn'], origin_lat, origin_lon)
        aqi = air_quality['data']['aqi']
        pm10 = air_quality['data']['iaqi'].get('pm10', {}).get('v', "N/A")
        pm25 = air_quality['data']['iaqi'].get('pm25', {}).get('v', "N/A")
    except Exception:
        pass

    # Get current time and calculate arrival time
    current_time = datetime.now()
    travel_duration = timedelta(seconds=travel_duration_secs)
    approximate_arrival_time = current_time + travel_duration

    # Format times
    current_time_formatted = current_time.strftime("%d-%m-%Y   %H:%M:%S")
    approximate_arrival_time_formatted = approximate_arrival_time.strftime("%d-%m-%Y   %H:%M:%S")

    # Weather and Rain
    rain_info, weather_description = "N/A", "N/A"
    try:
        weather_data = get_weather_and_rain(API_KEYS['openweather'], destination_lat, destination_lon)
        rain_info = weather_data.get("rain", rain_info)
        weather_description = weather_data.get("weather", weather_description)
    except Exception:
        pass

    # Emissions
    car_emissions, truck_emissions = "N/A", "N/A"
    try:
        emissions = calculate_emissions(distance_km)
        car_emissions = emissions.get("car", car_emissions)
        truck_emissions = emissions.get("truck", truck_emissions)
    except Exception:
        pass

    # Map and Polyline
    try:
        polyline = route_data['routes'][0]['overview_polyline']['points']
        decoded_polyline = decode_polyline(polyline)
        folium_map = folium.Map(location=[origin_lat, origin_lon], zoom_start=12)
        folium.PolyLine(locations=decoded_polyline, color="blue", weight=5).add_to(folium_map)
        folium.Marker([origin_lat, origin_lon], popup="Origin", icon=folium.Icon(color="green")).add_to(folium_map)
        folium.Marker([destination_lat, destination_lon], popup="Destination", icon=folium.Icon(color="red")).add_to(folium_map)
        map_html = "static/route_map.html"
        folium_map.save(map_html)
    except Exception as e:
        return render_template("error.html", error=f"Error creating map: {e}")

    return render_template(
        'result.html',
        route=route_data,
        traffic={"level": traffic_level, "description": traffic_description},
        air_quality={"aqi": aqi, "pm10": pm10, "pm25": pm25},
        emissions={"car": car_emissions, "truck": truck_emissions},
        weather={"description": weather_description, "rain": rain_info},
        current_time=current_time_formatted,
        approximate_arrival_time=approximate_arrival_time_formatted,
        map_html=map_html
    )


def decode_polyline(polyline):
    # Decodes an encoded polyline to a list of lat, lon coordinates
    index, lat, lng = 0, 0, 0
    coordinates = []
    while index < len(polyline):
        shift, result = 0, 0
        while True:
            byte = ord(polyline[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break
        dlat = (result & 1) and ~(result >> 1) or (result >> 1)
        lat += dlat
        shift, result = 0, 0
        while True:
            byte = ord(polyline[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break
        dlng = (result & 1) and ~(result >> 1) or (result >> 1)
        lng += dlng
        coordinates.append([lat / 1e5, lng / 1e5])
    return coordinates


if __name__ == '__main__':
    app.run(debug=True)
