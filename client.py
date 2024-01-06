import socket
import argparse
import time
import subprocess

def attach(host, port, action):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, int(port)))

    # Send the special message to the server
    client_socket.send(action.encode('utf-8'))
    print(f"Message sent to server: {action}")

    # Close the connection
    client_socket.close()

    
    if action == "attach":
        time.sleep(1)
        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe attach -r {host} -b 3-1.3.2.1.2".format(host=host), shell=True)
        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe attach -r {host} -b 3-1.3.2.1.1".format(host=host), shell=True)

    else:
        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe detach -p 00", shell=True)
        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe detach -p 01", shell=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--action', required=True, choices=['attach', 'detach'])
    args = parser.parse_args()

    attach(args.host, args.port, args.action)


if __name__ == '__main__':
    main()