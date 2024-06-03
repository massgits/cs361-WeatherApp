from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/wind', methods=['GET'])
def get_wind_speed():
    location = request.args.get('location')
    api_key = "4e135e42b0a995fd414528319169b4b7"
    # free weather API - OpenWeather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        wind_speed = data['wind']['speed']
        return jsonify({"Wind Speed": wind_speed})
    else:
        return jsonify({"error": "Failed to fetch wind speed data"})

if __name__ == '__main__':
    app.run(port=6790)