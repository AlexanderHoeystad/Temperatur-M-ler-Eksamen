from socket import *
import requests
from time import sleep
import json
import datetime

# Socket Configuration
serverPort = 10100
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverAddress = ('', serverPort)

# API Information fra WeatherAPI
api_key = "29501236f4854c099e1104709240405"
location = "Roskilde"
api_address = "https://heatwaveprojekt.azurewebsites.net/api/Temp"
headersArray = {'Content-Type': 'application/json'}

# Binder Server Address til Server Socket
serverSocket.bind(serverAddress)
print("The server is ready")

# Funktion til at hente vejrdata fra WeatherAPI
def fetch_weather(api_key, location):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": location, "aqi": "no"}
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

# Loop til at modtage data fra UDP broadcast
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    weatherData = fetch_weather(api_key, location)
    
    # Extract indoor temperature from the received JSON message
    indoor_temperature = json.loads(message.decode())["Temperature"]
    
    # Generate a new timestamp for each entry
    current_time = datetime.datetime.now()

    # Kombinerer data fra WeatherAPI og UDP broadcast
    combinedData = {
        "id": "0",
        "outDoorTemperature": weatherData['current']['temp_c'],
        "inDoorTemperature": indoor_temperature,
        "date": current_time.strftime('%Y-%m-%dT%H:%M:%S')
    }
    
    # Konverterer data til JSON
    json_data = json.dumps(combinedData)
    
    # Modtager data og printer fra UDP broadcast og WeatherAPI
    print("Received inDoorTemperature: " + message.decode())
    print("Received outDoorTemperature: " + str(weatherData['current']['temp_c']))
    
    # Sender data til API
    response = requests.post(api_address, data=json_data, headers=headersArray)
    
    # Tjekker om data er sendt korrekt
    print(response.status_code)
    print(response.text)
    
    # Printer data der er sendt
    print("Data sent: " + json_data)
