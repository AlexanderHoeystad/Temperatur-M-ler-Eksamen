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
    # Loop til at sende temperaturdata
    while True:
        # Get temperaturen fra Sense HAT
        temperature = get_temperature()

        # Sender temperaturdata i JSON format
        temperatureData = {
            "Temperature": temperature,
        }
        
        # Konverterer data til JSON
        jsonData = json.dumps(temperatureData)

        # Sender JSON data over til UDP broadcast
        clientSocket.sendto(jsonData.encode(), (serverName, serverPort))

        # Hvor lang tid den venter med at sende next broadcast
        sleep(60)

finally:
    clientSocket.close()
    print("Socket closed.")
