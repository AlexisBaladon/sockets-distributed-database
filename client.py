from clientSocket import ClientSocket

PORT = 2022  # The port used by the server

MSG = 'GET 2022 \n' # Test message
def main():
    client = ClientSocket() # Gets socket
    client.connect(client.getHost(), PORT) # Establish conection
    client.send(MSG)
    data = client.receive()
    client.close()
    print(data)

main()