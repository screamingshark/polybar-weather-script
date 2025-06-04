import argparse
import os

import requests
from requests.adapters import HTTPAdapter

URL = "https://api.openweathermap.org/data/2.5/weather"
# Get your API KEY here https://openweathermap.org/api,
# and set an environment variable for OPENWEATHER_API_KEY with your API KEY.
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "b2b6a57838c33b664a6390edc9b9871f")
HEADER = {"User-agent": "Mozilla/5.0"}


def get_city() -> str:
    try:
        r = requests.get("https://ipapi.co/json", headers=HEADER)
        return r.json()["city"]
    except requests.exceptions.ConnectionError:
        print("E: couldn't get city name")
        return "london"


def unit_suffix(unit: str) -> str:
    match unit:
        case "metric":
            unit = "ºC"
        case "imperial":
            unit = "ºF"
        case _:
            unit = " K"

    return unit

def get_icons(weather_code):

    match weather_code:
        case "01d":
            return "🌞"
        case "01n":
            return "🌙"
        case "02d":
            return "🌤"
        case "03d":
            return "🌥"
        case "03n" | "04d" | "04n":
            return "☁"
        case "09d" | "09n":
            return "🌧"
        case "10d" | "10n":
            return "🌦️"
        case "11d" | "11n":
            return "⛈"
        case "13d" | "13n":
            return "❄️"
        case "50d" | "50n":
            return "🌫️"
        case _:
            return "❓"  # 默认情况

def get_weather(city: str, lang: str, unit: str, api_key: str) -> dict[str, str] | None:

    try:
        s = requests.Session()
        s.mount("https://", HTTPAdapter(max_retries=5))
        r = s.get(
            f"{URL}?q={city}&lang={lang}&units={unit}&appid={api_key}",
            headers=HEADER,
            timeout=10,
        )
        data = r.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        icon = data["weather"][0]["icon"]
        unit = unit_suffix(unit)

        return {
            "temp": f"{int(temp)}{unit}",
            "desc": desc.title(),
            "icon": get_icons(icon),
        }

    except requests.exceptions.ConnectionError:
        print("E: failed to establish connection with the API")
        raise

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display information about the weather.",
    )
    parser.add_argument(
        "-c",
        metavar="CITY",
        dest="city",
        type=str,
        nargs="+",
        help="city name",
    )
    parser.add_argument(
        "-l",
        metavar="LANG",
        dest="lang",
        type=str,
        nargs=1,
        help="language (en, es, fr, ja, pt, pt_br, ru, zh_cn)",
    )
    parser.add_argument(
        "-u",
        metavar="metric/imperial",
        choices=("metric", "imperial"),
        dest="unit",
        type=str,
        nargs=1,
        help="unit of temperature (default: kelvin)",
    )
    parser.add_argument(
        "-a",
        metavar="API_KEY",
        dest="api_key",
        nargs=1,
        help="API Key",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="verbose mode",
    )

    args = parser.parse_args()

    api_key = args.api_key[0] if args.api_key else API_KEY
    city = args.city[0] if args.city else get_city()
    lang = args.lang[0] if args.lang else "en"
    unit = args.unit[0] if args.unit else "standard"

    weather = get_weather(city, lang, unit, api_key)
    if weather:
        temp, desc ,icon = weather.values()
        if args.verbose:
            print(f"{icon} {temp} {desc}")
        else:
            print(f"{temp}")


if __name__ == "__main__":
    main()
