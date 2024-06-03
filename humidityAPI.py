from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/humidity', methods=['GET'])
def get_weather_description():
    location = request.args.get('location')
    api_key = "4e135e42b0a995fd414528319169b4b7"
    # free weather API - OpenWeather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        humidity_data = data['main']['humidity']
        
        return jsonify({"Humidity": humidity_data})
    else:
        return jsonify({"error": "Failed to fetch humidity data"})

if __name__ == '__main__':
    app.run(port=6789)