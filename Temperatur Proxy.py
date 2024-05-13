from socket import *
import requests

serverPort = 10100
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverAddress = ('', serverPort)

api_address = "https://heatwaveprojekt.azurewebsites.net/api/Temp"
headersArray = {'Content-Type': 'application/json'}

serverSocket.bind(serverAddress)
print("The server is ready")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print("Received message:" + message.decode())
    requests.post(api_address, data=message, headers=headersArray)
