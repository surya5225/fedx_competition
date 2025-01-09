Route Optimization Project
This project is a web application designed to optimize routes between two locations and provide useful information such as traffic conditions, weather, air quality, and estimated emissions. The application is built using Flask, integrates with Google Maps API for location data, and uses simulated data for weather, traffic, and emissions.

Features
Route Optimization: Users can input an origin and destination to calculate the optimized route.
Displays details such as distance and travel time.
Traffic Information: Provides traffic congestion levels and descriptions.
Weather Information: Displays current weather conditions and rainfall data.
Air Quality Data: Shows AQI and particulate matter (PM10, PM2.5) levels.
Emissions Data: Estimates CO2 emissions for cars and trucks for the given route.
Interactive Map: Displays the route on a map using an embedded iframe.

Technologies Used
Frontend:HTML, CSS (basic styling inline), JavaScript (Google Places Autocomplete API integration)

Backend: Flask (Python web framework), Google Maps API (for location data)

Installation and Setup
Prerequisites:
Python 3.7 or higher
Flask (pip install flask)

Steps:
Clone the repository:
git clone https://github.com/surya5225/fedx_competition/edit/main
cd route-optimization
Install dependencies:
pip install -r requirements.txt
Obtain an API key for Google Maps:
Go to the Google Cloud Console.
Create a new project and enable the Maps JavaScript API and Places API.
Generate an API key and replace the placeholder in index.html:
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places"></script>

Run the application:
python app.py
Access the application in your browser at http://127.0.0.1:5000.

Usage
Open the application in your browser. Enter the origin and destination locations. Click "Optimize Route." View the results, including the optimized route, traffic, weather, air quality, and emissions data. Use the "Change Route" button to return to the input form.

Simulated Data
In the current version, traffic, weather, air quality, and emissions data are simulated. Replace these placeholders with real API integrations for production use:
Traffic Data: Use Google Maps Directions API for real-time traffic details.
Weather Data: Integrate with APIs like OpenWeatherMap or WeatherStack.
Air Quality Data: Use APIs such as AQICN or BreezoMeter.
Emissions Data: Develop a calculator or use third-party services for CO2 estimation.

Future Enhancements
API Integrations: Replace simulated data with real-time API calls.
User Authentication: Allow users to save their routes and preferences.
Responsive Design: Enhance UI/UX for mobile and tablet devices.
Additional Features: Integrate public transport options.Provide alternate routes and cost estimations.

Contact
For any queries or issues, feel free to reach out:
Email: jayasurya78088@gmail.com
