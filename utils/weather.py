import requests
def get_air_quality(api_key, lat, lon):
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"
    params = {"token": api_key}
    response = requests.get(url, params=params)
    return response.json()
def get_weather_and_rain(api_key, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        rain = data.get('rain', {}).get('1h', 0)  # Rainfall in the last hour
        return {"rain": rain, "weather": data.get('weather', [{}])[0].get('description', 'Not available')}
    else:
        raise ValueError(f"Failed to fetch weather data: {data.get('message', 'Unknown error')}")


