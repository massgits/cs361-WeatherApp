# Weather Dashboard
A simple project demonstrating microservices architecture through a weather dashboard. The app separates concerns into distinct Flask services (temperature, description, humidity, wind), each independently exposing an endpoint, and integrates them into a Tkinter GUI. This structure showcases how lightweight services can work together to form a cohesive application.

# Objectives
The purpose of this project is to illustrate functional understanding of microservices:

-Build small, independent services for specific tasks.
-Orchestrate those services in a desktop GUI client.
-Handle user input, validation, service communication, and error recovery cleanly.
-While the domain (weather reporting) is simple, the design mirrors real-world distributed systems where independent components collaborate to provide a complete solution.

# Tech Stack
Languages: Python 3
Libraries/Frameworks: Flask, Requests, Tkinter, ttk (themed widgets), python-dotenv
APIs/Services: OpenWeather API (current weather + forecast)

# How to Run
**1) Create & activate a virtual environment**
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\Activate.ps1  # Windows PowerShell

**2) Install dependencies**
pip3 install flask requests python-dotenv

**3) Add your API key to .env (create file if not present)**
echo "OPENWEATHER_API_KEY=your_real_key_here" > .env

**4) Start each microservice in its own terminal**
python3 tempAPI.py         # http://127.0.0.1:6787/weather
python3 descriptionAPI.py  # http://127.0.0.1:6788/description
python3 humidityAPI.py     # http://127.0.0.1:6789/humidity
python3 windAPI.py         # http://127.0.0.1:6790/wind

**5) Launch the GUI app**
python3 weatherApp.py

**Features**
-Tkinter GUI with modern ttk styling
-Placeholder entry that clears on focus and restores if empty
-Input validation (letters, numbers, spaces, commas, periods, apostrophes, dashes; 1–80 chars)
-Spinner (loading animation) while fetching data
-Background thread for network requests (UI never freezes)

**Microservices:**
-Temperature (°F)
-Weather description (e.g., “clear sky”)
-Humidity (%)
-Wind speed

**Learning Takeaways**
This project was built to show practical understanding of microservices:

-Service isolation: each weather attribute runs as its own Flask service.
-Orchestration: a Tkinter GUI acts as a lightweight client to call multiple services.
-Resilience: input validation, error handling, and timeouts ensure the system fails gracefully.
-Security hygiene: API keys externalized, no secrets in code, and HTTPS enforced.
