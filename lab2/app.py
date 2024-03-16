import os
import base64
import asyncio
import requests
import statistics
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

from io import BytesIO
from labellines import labelLines
from matplotlib.ticker import AutoLocator, AutoMinorLocator

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI()


def get_data_from(url: str, headers: dict = {}):
    try:
        response = requests.get(url, headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def process_weather_info(weather_info: dict):
    if "hourly" not in weather_info:
        return None
    if any(p not in weather_info["hourly"] for p in ("time", "temperature_2m", "rain")):
        return None
    time = weather_info["hourly"]["time"]
    temp = weather_info["hourly"]["temperature_2m"]
    rain = weather_info["hourly"]["rain"]

    avg_temp = statistics.mean(temp)
    max_temp = max(temp)
    min_temp = min(temp)

    fig, ax1 = plt.subplots()

    ax1.plot(time, temp, color="r")
    x_lim = ax1.get_xlim()
    ax1.set_xlim(*x_lim)

    ax1.axhline(avg_temp, xmin=0, xmax=x_lim[1], color="r", lw=0.8, ls="--", label=f"Avg = {avg_temp:.1f} °C")
    ax1.axhline(min_temp, xmin=0, xmax=x_lim[1], color="r", lw=0.8, ls="--", label=f"Min = {min_temp:.1f} °C")
    ax1.axhline(max_temp, xmin=0, xmax=x_lim[1], color="r", lw=0.8, ls="--", label=f"Max = {max_temp:.1f} °C")

    labelLines(ax1.get_lines()[-3:], drop_label=True)

    ax1.set_ylabel("Temperature [°C]", color="r")
    ax1.set_xticks(time, time, rotation=-30, ha="left")

    ax1.xaxis.set_major_locator(AutoLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())

    ax2 = ax1.twinx()
    ax2.set_ylabel("Rain [mm]", color="blue")
    ax2.bar(time, rain, color="blue", alpha=0.5)

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format="png", bbox_inches="tight")
    encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")

    return f"<img src='data:image/png;base64,{encoded}'>"


@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <html>
        <head>
            <title>Simple Weather Forecasty</title>
        </head>
        <body>
            <h2>Simple Weather Forecast</h2>
            <form action="/result" method="post">
                <label for="city">City:</label><br>
                <input type="text" id="city" name="city"><br>
                <label for="forecast">Forecast days:</label><br>
                <input type="number" min="1" max="16" id="forecast" name="forecast"><br>
                <button type="submit">Send</button>
            </form>
        </body>
    </html>
    """


html_log_error = (
    lambda e: f"""
        <html>
            <head>
                <title>Simple Weather Forecast</title>
            </head>
            <body>
                <h2>Simple Weather Forecast</h2>
                <p>{e}</p>
            </body>
        </html>
        """
)


@app.post("/result", response_class=HTMLResponse)
async def process_request(city: str = Form(None), forecast: int = Form(None)):
    if None in (city, forecast):
        return html_log_error("Not all parameters were provided!")

    # Request latitude, longitude from 1st API
    geocoding = await asyncio.to_thread(
        get_data_from, f"https://api.api-ninjas.com/v1/geocoding?city={city}", {"X-Api-Key": API_KEY}
    )

    if geocoding is None or len(geocoding) < 1:
        return html_log_error(f"Error retrieving geocoding of the city: {city}!")
    geocoding = geocoding[0]

    if any(p not in geocoding for p in ("latitude", "longitude", "country")):
        return html_log_error(f"Geocoding does not contain necessary parameters!")

    lat, lon, country = geocoding["latitude"], geocoding["longitude"], geocoding["country"]

    # Request weather forecast from 2nd API
    weather_info = await asyncio.to_thread(
        get_data_from,
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,rain&forecast_days={forecast}",
    )

    if weather_info is None:
        return html_log_error("Error retrieving weather forecasts!")

    # Process weather forecast
    weather_info = process_weather_info(weather_info)

    if weather_info is None:
        return html_log_error("Error processing weather forecasts!")

    return f"""
    <html>
        <head>
            <title>Simple Weather Forecast</title>
        </head>
        <body>
            <h2>Simple Weather Forecast</h2>
            <p>{city}, {country}, ({lat:.2f}, {lon:.2f})</p>
            <p>{weather_info}</p>
        </body>
    </html>
    """
