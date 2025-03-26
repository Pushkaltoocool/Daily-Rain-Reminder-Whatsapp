import os
import requests
from twilio.rest import Client

# Get secrets from environment variables
API_KEY = os.getenv("API_KEY")
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

LATITUDE = 1.290270
LONGITUDE = 103.851959

parameters = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "cnt": 4,
    "appid": API_KEY
}

weather_codes = []
response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
weather_data = response.json()["list"]

for i in weather_data:
    weather_codes.append(i["weather"][0]["id"])

need_umbrella = any(int(code) < 700 for code in weather_codes)

if need_umbrella:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+{your twilio number}',
        body='It is going to rain today! Prepare an umbrella if you are going out ☂️',
        to='whatsapp:+{your own number}'
    )
    print(message.status)
