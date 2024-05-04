from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    api_key = "4e135e42b0a995fd414528319169b4b7"
    # free weather API - OpenWeather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        temperature_kelvin = data['main']['temp']
        
        temperature_fahrenheit = round(temperature_kelvin - 273.15) * 9/5 + 32
        
        return jsonify({"Temperature": f"{temperature_fahrenheit}°F"})
    else:
        return jsonify({"error": "Failed to fetch weather data"})

if __name__ == '__main__':
    app.run(port=6787)