from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/description', methods=['GET'])
def get_weather_description():
    location = request.args.get('location')
    api_key = "4e135e42b0a995fd414528319169b4b7"
    # free weather API - OpenWeather
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        weather_description = data['list'][0]['weather'][0]['description']
        
        return jsonify({"Description": weather_description})
    else:
        return jsonify({"error": "Failed to fetch forecast data"})

if __name__ == '__main__':
    app.run(port=6788)