import tkinter as tk
from tkinter import font as tkfont
import requests

class WeatherDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Dashboard")
        self.geometry("400x300")
        self.center_window()

        self.default_font = tkfont.Font(family="Helvetica", size=12)
        self.bold_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

        # Frame for location entry
        self.location_frame = tk.Frame(self)
        self.location_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Information button
        self.info_button = tk.Button(self.location_frame, text="i", command=self.show_info)
        self.info_button.grid(row=0, column=2, padx=10, sticky="e")

        # Label for entry field
        self.location_label = tk.Label(self.location_frame, text="Enter City Name:", font=self.default_font)
        self.location_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Entry field
        self.location_entry = tk.Entry(self.location_frame, font=self.default_font)
        self.location_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.location_entry.bind("<Return>", self.get_weather)

        # Submit button
        self.fetch_button = tk.Button(self.location_frame, text="Get Weather Info", command=self.get_weather, font=self.bold_font)
        self.fetch_button.grid(row=1, column=1, padx=10, pady=5, sticky="e")

        # Frame for result display
        self.result_frame = tk.Frame(self)
        self.result_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.result_label = tk.Label(self.result_frame, text="", font=self.default_font, justify="left")
        self.result_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.location_frame.grid_columnconfigure(1, weight=1)
        self.result_frame.grid_columnconfigure(0, weight=1)

        # Set focus to the entry field
        self.location_entry.focus_set()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def get_weather(self, event=None):
        location = self.location_entry.get()
        if location:
            # Initialize variables to store results
            current_temperature = "N/A"
            weather_description = "N/A"
            humidity = "N/A"
            wind = "N/A"

            # Fetch data from each microservice, handling failures individually
            try:
                weather_data = self.fetch_microservice_data("http://localhost:6787/weather", location)
                current_temperature = weather_data.get("Temperature", "N/A")
            except Exception as e:
                print(f"Failed to fetch weather data: {e}")

            try:
                forecast_data = self.fetch_microservice_data("http://localhost:6788/description", location)
                weather_description = forecast_data.get("Description", "N/A")
            except Exception as e:
                print(f"Failed to fetch forecast data: {e}")

            try:
                humidity_data = self.fetch_microservice_data("http://localhost:6789/humidity", location)
                humidity = humidity_data.get("Humidity", "N/A")
            except Exception as e:
                print(f"Failed to fetch humidity data: {e}")

            try:
                wind_data = self.fetch_microservice_data("http://localhost:6790/wind", location)
                wind = wind_data.get("Wind Speed", "N/A")
            except Exception as e:
                print(f"Failed to fetch wind data: {e}")

            # Display data with labels
            self.result_label.config(
                text=f"Current Temperature: {current_temperature}\nWeather Description: {weather_description}\nHumidity: {humidity}\nWind Speed: {wind}")

    def fetch_microservice_data(self, url, location):
        response = requests.get(url, params={"location": location})
        if response.status_code == 200:
            return response.json()
        else:
            return "Failed to fetch data"

    def show_info(self):
        info_window = tk.Toplevel(self)
        info_window.title("About")
        info_window.geometry("600x300")

        info_label = tk.Label(info_window, text="Weather Dashboard App\n\nThis app allows you to get weather information such as Temperature and a brief weather description for a specific city.\n\nInstructions:\n1. Enter the city name in the text box. If your results show 'N/A', check your spelling and try again.\n2. Click 'Get Weather Info' to fetch the data.\n3. Repeat steps 1 and 2 if you'd like to search other cities.\n\nFor any queries, contact support@weatherappcs361.com", wraplength=500)
        info_label.pack(padx=10, pady=10)

def main():
    app = WeatherDashboard()
    app.mainloop()

if __name__ == "__main__":
    main()
