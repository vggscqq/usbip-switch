import argparse
import time
import subprocess
import threading
import keyboard
import requests
from flask import Flask, redirect
import logging
import paramiko

PORT = 5000

server_usbIDs = ["3-1.3.2.1.2", "3-1.3.2.1.1"]
#server_usbIDs = ["3-1.3.2.1.1"]
client_usbIDs = []

for i in range(len(server_usbIDs)):
    if len(str(i)) == 1:
        client_usbIDs.append(f"0{i}")
    else:
        client_usbIDs.append(f"{i}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def release_keys():
    keyboard.release("ctrl")
    keyboard.release("alt")
    keyboard.release("1")
    keyboard.release("2")
    keyboard.release("3")
    time.sleep(1)
    keyboard.release("ctrl")
    keyboard.release("alt")
    keyboard.release("1")
    keyboard.release("2")
    keyboard.release("3")


def switcher_web():
    app = Flask(__name__)

    @app.route("/")
    def root():
        return """
    <a href="/to_server" style="font-size:130px;">Pass to server</a>
    <br>
    <a href="/to_client" style="font-size:130px;">Pass to client</a>
    """

    @app.route("/to_server")
    def to_server():
        #TODO
        #1. Announce demand to client
        for i in client_usbIDs:
            command = f"C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe detach -p {i}"
            print(command)
            requests.post(f"http://{args.rhost}:{PORT}/run", data=command)

        #2. Unbind locally

        for i in server_usbIDs:
            subprocess.run([f"sudo usbip unbind -b {i}"], shell=True)


        return redirect("/")
    
    @app.route("/to_client")
    def to_client():
        #TODO
        #1. Bind usbip device
        for i in server_usbIDs:
            subprocess.run([f"sudo usbip bind -b {i}"], shell=True)

        #2. Attach device on client
        for i in server_usbIDs:
            command = f"C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe attach -r {args.lhost} -b {i}"
            print(command)
            requests.post(f"http://{args.rhost}:{PORT}/run", data=command)

        return redirect("/")

    app.run(host="0.0.0.0")

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--lhost', required=True)
        parser.add_argument('--rhost', required=True)
        parser.add_argument('--mode', required=True, choices=['client', 'server'])
        global args 
        args = parser.parse_args()

        if args.mode == 'client':
            pass

        elif args.mode == 'server':
            hkT = threading.Thread(target=switcher_web, args=())
            hkT.start()

            hkT.join()
    except Exception as e:
        logger.error(f"Error in main: {e}")


if __name__ == '__main__':
    main()
