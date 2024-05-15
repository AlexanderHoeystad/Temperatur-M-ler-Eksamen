from socket import *
import requests
from time import sleep
import json
import datetime

serverPort = 10100
serverSocket = socket(AF_INET, SOCK_DGRAM)

api_key = "29501236f4854c099e1104709240405"  # API KEY from WeatherAPI
location = "Roskilde"  # Location name

serverAddress = ('', serverPort)

api_address = "https://heatwaveprojekt.azurewebsites.net/api/Temp"
headersArray = {'Content-Type': 'application/json'}

serverSocket.bind(serverAddress)
print("The server is ready")

def fetch_weather(api_key, location):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": location, "aqi": "no"}
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    weatherData = fetch_weather(api_key, location)
    
    # Extract indoor temperature from the received JSON message
    indoor_temperature = json.loads(message.decode())["Temperature"]
    
    # Generate a new timestamp for each entry
    current_time = datetime.datetime.now()
    # formatted_date = current_time.strftime('%Y-%m-%dT%H:%M:%S')

    combinedData = {
        "id": "0",
        "outDoorTemperature": weatherData['current']['temp_c'],
        "inDoorTemperature": indoor_temperature,
        "date": current_time.strftime('%Y-%m-%dT%H:%M:%S')
        # "date": "2023-01-05T02:12:11"
    }
    
    json_data = json.dumps(combinedData)
    print("Received inDoorTemperature: " + message.decode())
    print("Received outDoorTemperature: " + str(weatherData['current']['temp_c']))
    response = requests.post(api_address, data=json_data, headers=headersArray)
    print(response.status_code)
    print(response.text)
    sleep(5)
    print("Data sent: " + json_data)
