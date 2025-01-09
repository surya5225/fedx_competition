def get_tomtom_traffic(api_key, lat, lon):
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    params = {
        "key": api_key,
        "point": f"{lat},{lon}",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        try:
            return response.json()
        except Exception as e:
            print("Error parsing JSON:", response.text)
            raise e
    else:
        print(f"API Error: {response.status_code} - {response.text}")
        raise Exception("API Request Failed")
