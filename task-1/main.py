#!/usr/bin/python3
from flask import Flask, jsonify, request
from requests import get
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
env = getenv("FLASK_ENV", "development")
app.config.from_object(f"config.{env.capitalize()}Config")

weather_key = getenv("WEATHER_API_KEY")
ip_token = getenv("IP_INFO_TOKEN")


@app.route("/api/hello", methods=["GET"], strict_slashes=True)
def hello():
    """
    A simple Flask api endpoint.

    Returns:
        json: {
            "client_ip": str,
            "greeting": str,
            "location": str,
          }
    """
    visitor = request.args.get("visitor_name")
    if not visitor:
        return jsonify({"error": 'missing parameter "visitor_name"'}, 404)

    requester_ip = request.remote_addr
    try:
        local = get(f"https://ipinfo.io/{requester_ip}?token={ip_token}")
        location = local.json()
        city = location.get("city")

        if local.ok:
            coord = get(
                f"https://api.weatherapi.com/v1/current.json",
                params={"key": weather_key, "q": city},
            )
            coords = coord.json()
            temp = int(coords.get("current").get("temp_c"))

            return jsonify(
                {
                    "client_ip": requester_ip,
                    "greeting": f"Hello, {visitor}!, the temperature is {temp} degrees Celcius in {city}",
                    "location": city,
                }
            )
    except:
        return jsonify({"error": "unexpected error"}, 500)


if __name__ == "__main__":
    # Run the Flask application if this script is executed directly.
    app.run()
