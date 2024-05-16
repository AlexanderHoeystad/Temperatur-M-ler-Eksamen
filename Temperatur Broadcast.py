from sense_hat import SenseHat
import json
from socket import *
from time import sleep, time

sense = SenseHat()

# Funktion til at hente temperaturen fra Sense HAT
def get_temperature():
    temperature = sense.get_temperature()
    return round(temperature, 1)

# Broadcaster konfiguration
serverName = '255.255.255.255'
serverPort = 10100
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

try:
    while True:
        # Get temperature from Sense HAT
        temperature = get_temperature()

        # Send temperature data in JSON format
        temperatureData = {
            "Temperature": temperature,
        }
        
        # Convert data to JSON
        jsonData = json.dumps(temperatureData)

        # Send JSON data over UDP broadcast
        clientSocket.sendto(jsonData.encode(), (serverName, serverPort))

        # Wait before sending the next broadcast
        sleep(60)

except KeyboardInterrupt:
    pass