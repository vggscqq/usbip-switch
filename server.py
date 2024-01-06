import socket
import subprocess
import time


# Server configuration
host = '10.19.0.1'
port = 12345

while True:

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))
    # Listen for incoming connections
    server_socket.listen(1)


    print(f"Server listening on {host}:{port}")

    # Accept a connection from the client
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')

    # Check if the received message is the special message
    if data.strip() == "attach":
        print("Attach demand recieved.")
        
        subprocess.run(["sudo usbip bind -b 3-1.3.2.1.2"], shell=True)
        subprocess.run(["sudo usbip bind -b 3-1.3.2.1.1"], shell=True)
        
    elif data.strip() == "detach":
        print("Detach demand recieved.")

        subprocess.run(["sudo usbip unbind -b 3-1.3.2.1.2"], shell=True)
        subprocess.run(["sudo usbip unbind -b 3-1.3.2.1.1"], shell=True)

    else:
        print("Invalid message received. No action taken.")

    # Close the connection
    client_socket.close()
    server_socket.close()

    time.sleep(5)