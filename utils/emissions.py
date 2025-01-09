import requests
def calculate_emissions(distance_km):
    car_emission_factor = 0.2  # kg CO2 per km for a car
    truck_emission_factor = 0.8  # kg CO2 per km for a truck

    car_emissions = round(distance_km * car_emission_factor, 2)
    truck_emissions = round(distance_km * truck_emission_factor, 2)

    return {"car": car_emissions, "truck": truck_emissions}

