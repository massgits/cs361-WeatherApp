import tkinter as tk
import requests

class WeatherDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Dashboard")
        
        # information button
        self.info_button = tk.Button(self, text="i", command=self.show_info)
        self.info_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        # label for entry field
        self.location_label = tk.Label(self, text="Enter City Name:")
        self.location_label.grid(row=1, column=0, padx=10, pady=10, sticky = "w")

        # entry field
        self.location_entry = tk.Entry(self)
        self.location_entry.grid(row=1, column=1, padx=10, pady=10, sticky = "ew")

        # submit button
        self.fetch_button = tk.Button(self, text="Get Weather Info", command=self.get_weather)
        self.fetch_button.grid(row=2, column=1, padx=10, pady=5, sticky = "w")

        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=4, column=0, padx=5, pady=5, sticky = "")



    def get_weather(self):
        location = self.location_entry.get()
        if location:
            # fetch data from microservices
            weather_data = self.fetch_microservice_data("http://localhost:6787/weather", location)
            forecast_data = self.fetch_microservice_data("http://localhost:6788/description", location)

            current_temperature = weather_data.get("Temperature", "N/A")
            weather_description = forecast_data.get("Description", "N/A")

            # display data with labels
            self.result_label.config(text=f"Current Temperature: {current_temperature}\nWeather Description: {weather_description}")

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