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

#Funkction to process data and send it to the API
def process_data(data):
    try:
        json_data = json.loads(data.decode())
        response = requests.post(api_address, data=json_data, headers=headersArray)
        if response.status_code == 200:
            return "Data sent successfully"
        else:
            print("Error sending data to API")

    except Exception as e:
        print("Error processing data")
        print()

#Function for UDP receivers to receive data, for different ports
def receive_data():
    ports = [10100, 10101]
    threads = []

    for port in ports:
        thread = threading.Thread(target=receive_data_thread, args=(port,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
if __name__ == "__main__":
    receive_data()