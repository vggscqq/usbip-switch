import argparse
import subprocess
import threading
import requests
from flask import Flask, redirect
import logging

PORT = 5000

server_usbIDs = ["3-1.3.2.1.2", "3-1.3.2.1.1"]
usbipexepath = "C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe"
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
        try:
            for i in client_usbIDs:
                command = f"{usbipexepath} detach -p {i}"
                print(command)
                requests.post(f"http://{args.c}:{PORT}/run", data=command)
        except Exception:
            logger.error(f"Error in demanding to server: {e}")
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
        try:
            for i in server_usbIDs:
                command = f"{usbipexepath} attach -r {args.shost} -b {i}"
                print(command)
                requests.post(f"http://{args.c}:{PORT}/run", data=command)
        except Exception:
            logger.error(f"Error in demanding to client, unable to connect: {e}")
            logger.error("Unbinding...")
            for i in server_usbIDs:
                subprocess.run([f"sudo usbip unbind -b {i}"], shell=True)
        return redirect("/")

    app.run(host="0.0.0.0")

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--shost', required=True)
        parser.add_argument('--c', required=True)
        #parser.add_argument('--mode', required=True, choices=['client', 'server'])
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
