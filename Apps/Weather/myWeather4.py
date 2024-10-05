# -*- coding: utf-8 -*-

import requests
import time as t  # Renamed to 't' to avoid conflicts with time display
from datetime import datetime
from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.render import canvas
from luma.core.legacy import text, show_message  # Added show_message for scrolling text
from luma.core.legacy.font import TINY_FONT  # Use TINY_FONT from legacy fonts

# WMO weather codes with description
weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

# Step 1: Fetch temperature, weather code, and wind speed data from Open-Meteo
def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 53.578806,  # Replace with your location's latitude
        "longitude": -113.378106,  # Replace with your location's longitude
        "current_weather": True  # This requests the current weather
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        
        data = response.json()  # Parse the response as JSON
        
        # Fetch the current weather (temperature, weather code, and wind speed)
        current_weather = data.get('current_weather', {})
        current_temperature = current_weather.get('temperature', None)  # Fetch temperature
        weather_code = current_weather.get('weathercode', None)  # Fetch weather code
        wind_speed = current_weather.get('windspeed', None)  # Fetch wind speed (in km/h)
        
        if current_temperature is None or weather_code is None or wind_speed is None:
            print("Error: Could not retrieve temperature, weather code, or wind speed from response.")
            return None, None, None
        
        return current_temperature, weather_code, wind_speed
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Open-Meteo: {e}")
        return None, None, None

# Step 2: Setup the LED matrix
def setup_led_matrix():
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=12, block_orientation=-90, rotate=2, width=32, height=24)  # Adjust parameters as needed
    return device

# Step 3: Scroll temperature, weather description, and wind speed across the LED matrix
def scroll_weather_message(device, message):
    # Scroll the message across the LED matrix once
    show_message(device, message, fill="white", font=TINY_FONT, scroll_delay=0.05)  # Adjust scroll_delay for speed

# Step 4: Display current time for 5 seconds on the LED matrix
def display_time(device):
    now = datetime.now()
    current_time = now.strftime("%H:%M")  # Format the time as HH:MM
    with canvas(device) as draw:
        text(draw, (0, 2), current_time, fill="white", font=TINY_FONT)  # Display the current time
    t.sleep(5)  # Display time for 5 seconds

# Helper function to interpret weather code
def interpret_weather_code(code):
    return weather_codes.get(code, "Unknown weather")

# Main function to continuously refresh weather info every 30 minutes and loop display
def main():
    device = setup_led_matrix()  # Initialize LED matrix once
    last_update_time = t.time()  # Track the last time weather data was fetched (epoch time)
    update_interval = 1800  # Set update interval to 30 minutes (1800 seconds)
    
    # Initialize temperature, weather description, and wind speed for first display
    temperature, weather_code, wind_speed = get_weather_data()  # Initial fetch of weather data
    
    while True:  # Infinite loop to display and refresh
        # Step 1: Check if 30 minutes have passed since the last update
        if t.time() - last_update_time >= update_interval:
            temperature, weather_code, wind_speed = get_weather_data()  # Fetch new weather data
            last_update_time = t.time()  # Reset the last update time
        
        # Step 2: If valid temperature, weather, and wind speed, interpret the weather code
        if temperature is not None and weather_code is not None and wind_speed is not None:
            weather_description = interpret_weather_code(weather_code)
            message = f"Temp: {temperature:.1f}C, Wind: {wind_speed:.1f}km/h, {weather_description}"  # Create message
            
            # Step 3: Scroll the weather message once
            scroll_weather_message(device, message)
            
            # Step 4: Display the current time for 5 seconds
            display_time(device)
        
        else:
            print("Failed to get weather data.")
            display_time(device)  # Still display time if weather fetch fails

if __name__ == "__main__":
    main()
