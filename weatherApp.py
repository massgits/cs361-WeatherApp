import tkinter as tk
from tkinter import ttk
import requests
import threading
import re


class WeatherDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Dashboard")
        self.minsize(460, 320)
        self.center_window()

        # ttk theme + styles
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("Field.TLabel", font=("Helvetica", 11))
        style.configure("Value.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("TButton", padding=6)

        # root grid config
        self.columnconfigure(0, weight=1)

        # main container
        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)

        # header
        ttk.Label(container, text="Weather Dashboard", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )

        # search row
        search_row = ttk.Frame(container)
        search_row.grid(row=1, column=0, pady=(12, 6), sticky="ew")
        search_row.columnconfigure(0, weight=1)

        # --- Entry with placeholder behavior ---
        self.location_var = tk.StringVar()
        self.placeholder_text = "ex. Seattle or [Zipcode]"
        self._placeholder_active = True

        # Use tk.Entry so we can set fg color for placeholder
        self.entry = tk.Entry(search_row, textvariable=self.location_var, fg="#777777")
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.location_var.set(self.placeholder_text)

        # Bind focus events to manage placeholder
        self.entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.entry.bind("<FocusOut>", self._on_entry_focus_out)

        self.search_btn = ttk.Button(search_row, text="Get Weather", command=self.fetch_weather)
        self.search_btn.grid(row=0, column=1)

        # spinner (hidden until fetching)
        self.spinner = ttk.Progressbar(search_row, mode="indeterminate", length=120)
        self.spinner.grid(row=0, column=2, padx=(8, 0))
        self.spinner.grid_remove()

        # Enter key triggers search
        self.bind("<Return>", lambda e: self.fetch_weather())

        # status line
        self.status_var = tk.StringVar(value="")
        ttk.Label(container, textvariable=self.status_var, style="Field.TLabel").grid(
            row=2, column=0, sticky="w"
        )

        # results card
        result = ttk.Frame(container, padding=12)
        result.grid(row=3, column=0, pady=(12, 0), sticky="ew")
        result.columnconfigure(1, weight=1)

        ttk.Label(result, text="Temperature:", style="Field.TLabel").grid(
            row=0, column=0, sticky="w", pady=2
        )
        self.temp_var = tk.StringVar(value="—")
        ttk.Label(result, textvariable=self.temp_var, style="Value.TLabel").grid(
            row=0, column=1, sticky="w", pady=2
        )

        ttk.Label(result, text="Description:", style="Field.TLabel").grid(
            row=1, column=0, sticky="w", pady=2
        )
        self.desc_var = tk.StringVar(value="—")
        ttk.Label(result, textvariable=self.desc_var, style="Value.TLabel").grid(
            row=1, column=1, sticky="w", pady=2
        )

        ttk.Label(result, text="Humidity:", style="Field.TLabel").grid(
            row=2, column=0, sticky="w", pady=2
        )
        self.hum_var = tk.StringVar(value="—")
        ttk.Label(result, textvariable=self.hum_var, style="Value.TLabel").grid(
            row=2, column=1, sticky="w", pady=2
        )

        ttk.Label(result, text="Wind:", style="Field.TLabel").grid(
            row=3, column=0, sticky="w", pady=2
        )
        self.wind_var = tk.StringVar(value="—")
        ttk.Label(result, textvariable=self.wind_var, style="Value.TLabel").grid(
            row=3, column=1, sticky="w", pady=2
        )

        # Front-end validation regex (matches backend rule)
        self._allowed_re = re.compile(r"[A-Za-z0-9\s\-.,']{1,80}$")

    def center_window(self):
        self.update_idletasks()
        w, h = 460, 320
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ---------- placeholder helpers ----------
    def _on_entry_focus_in(self, _event):
        if self._placeholder_active:
            self.location_var.set("")
            self.entry.config(fg="#000000")
            self._placeholder_active = False

    def _on_entry_focus_out(self, _event):
        if not self.location_var.get().strip():
            self.location_var.set(self.placeholder_text)
            self.entry.config(fg="#777777")
            self._placeholder_active = True

    # ---------- loading helpers ----------
    def start_loading(self, msg="Fetching…"):
        self.search_btn.state(["disabled"])
        self.status_var.set(msg)
        self.spinner.grid()         # show
        self.spinner.start(12)      # animate

    def end_loading(self):
        self.spinner.stop()
        self.spinner.grid_remove()  # hide
        self.search_btn.state(["!disabled"])

    # ---------- UI actions ----------
    def fetch_weather(self):
        city = self.location_var.get().strip()

        # Treat placeholder as empty
        if self._placeholder_active or not city:
            self.status_var.set("Enter a location like: Seattle,WA,US(or ZIP code)")
            return

        # Front-end input validation (same as backend)
        if not self._allowed_re.fullmatch(city):
            self.status_var.set(
                "Please use only letters, numbers, spaces, commas, periods, apostrophes, and dashes (1–80 chars)."
            )
            return

        self.start_loading()

        # Run network requests in a background thread so UI stays responsive
        thread = threading.Thread(target=self._fetch_worker, args=(city,), daemon=True)
        thread.start()

    # Worker thread: do the HTTP calls here
    def _fetch_worker(self, city):
        result = {"temp": "—", "desc": "—", "hum": "—", "wind": "—", "error": ""}

        try:
            t = requests.get("http://127.0.0.1:6787/weather", params={"location": city}, timeout=5).json()
            d = requests.get("http://127.0.0.1:6788/description", params={"location": city}, timeout=5).json()
            h = requests.get("http://127.0.0.1:6789/humidity", params={"location": city}, timeout=5).json()
            w = requests.get("http://127.0.0.1:6790/wind", params={"location": city}, timeout=5).json()

            result["temp"] = t.get("Temperature", "—")
            result["desc"] = d.get("Description", "—")
            result["hum"]  = h.get("Humidity", "—")
            result["wind"] = w.get("Wind Speed", "—")
        except requests.Timeout:
            result["error"] = "Request timed out. Try again."
        except Exception:
            result["error"] = "Something went wrong. Try again."

        # Back to the UI thread to update widgets
        self.after(0, lambda r=result: self._apply_results(r))

    def _apply_results(self, r):
        if r["error"]:
            self.status_var.set(r["error"])
        else:
            self.temp_var.set(r["temp"])
            self.desc_var.set(r["desc"])
            self.hum_var.set(r["hum"])
            self.wind_var.set(r["wind"])
            self.status_var.set("")
        self.end_loading()


if __name__ == "__main__":
    app = WeatherDashboard()
    app.mainloop()