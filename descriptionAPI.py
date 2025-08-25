from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import re

REQUEST_TIMEOUT = 5  # seconds

# helper for city input validation
_ALLOWED = re.compile(r"[A-Za-z0-9\s\-.,']+$")


def clean_location(raw: str):
    if not raw:
        return None
    s = raw.strip()
    # length guard: avoids abuse and weird upstream behavior
    if not (1 <= len(s) <= 80):
        return None
    # allow common city formats like "San José, CA"
    if not _ALLOWED.match(s):
        return None
    # collapse multiple spaces
    s = re.sub(r"\s{2,}", " ", s)
    return s


load_dotenv()

app = Flask(__name__)

@app.route('/description', methods=['GET'])
def get_weather_description():
    raw_location = request.args.get('location')
    location = clean_location(raw_location)
    if not location:
        return jsonify({"error": "Invalid 'location'"}), 400
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return jsonify({"error": "API key not configured"}), 500
    
    # free weather API - OpenWeather
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": location, "appid": api_key}
    
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    except requests.Timeout:
        return jsonify({"error": "Upstream timeout"}), 504
    except requests.RequestException:
        return jsonify({"error": "Upstream request failed"}), 502
    
    if response.status_code == 200:
        data = response.json()
        
        weather_description = data['list'][0]['weather'][0]['description']
        
        return jsonify({"Description": weather_description})
    else:
        return jsonify({"error": "Failed to fetch forecast data"})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=6788)
