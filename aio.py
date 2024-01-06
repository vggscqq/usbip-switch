import socket
import argparse
import time
import subprocess
import threading
import keyboard

import requests
from flask import Flask, request


# ctrl + alt + 1 -> pass to host
# ctrl + alt + 2 -> pass to client
# ctrl + alt + 2 -> exit()

PORT = 5000

def do_release():
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


def hotkey_handler(mode, host):
    if mode == "client":
        keyboard.add_hotkey('ctrl + alt + 1', client_usb, args =('detach', host,))
        keyboard.wait('ctrl + alt + 3')
        exit() 
    else:
        keyboard.add_hotkey('ctrl + alt + 2', server_usb, args =('attach', host,))
        keyboard.wait('ctrl + alt + 3')
        exit() 

def client_usb(action, host):
    do_release()
    if action == "attach":
        print("CLIENT: hotkey handler attach")

        addr = "http://{}:{}/".format(host, PORT)
        requests.post(addr + "sattach")

        time.sleep(1)
        
        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe attach -r {host} -b 3-1.3.2.1.2".format(host=host), shell=True)
        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe attach -r {host} -b 3-1.3.2.1.1".format(host=host), shell=True)
        print("usbip.exe attach")

    else:
        print("CLIENT: hotkey handler detach")
        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe detach -p 00", shell=True)
        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe detach -p 01", shell=True)
        print("usbip.exe detach")

        print("CLIENT: http handler detach")
        addr = "http://{}:{}/".format(host, PORT)
        requests.post(addr + "sdetach")
    do_release()

def server_usb(action, host):
    do_release()
    if action == "attach":
        subprocess.run(["sudo usbip bind -b 3-1.3.2.1.2"], shell=True)
        subprocess.run(["sudo usbip bind -b 3-1.3.2.1.1"], shell=True)
        print("sudo usbip bind")
        #TODO send attach request to client

        addr = "http://{}:{}/".format(host, PORT)
        requests.post(addr + "cattach")


    else:
        subprocess.run(["sudo usbip unbind -b 3-1.3.2.1.2"], shell=True)
        subprocess.run(["sudo usbip unbind -b 3-1.3.2.1.1"], shell=True)
        print("sudo usbip ubind")
        # TODO send detach request to client
        
        addr = "http://{}:{}/".format(host, PORT)
        requests.post(addr + "cdetach")
    do_release()



def server(host):

    app = Flask(__name__)

    @app.route('/sattach', methods=['POST'])
    def attach():
        print("SERVER: Attach demand recieved.")
        
        subprocess.run(["sudo usbip bind -b 3-1.3.2.1.2"], shell=True)
        subprocess.run(["sudo usbip bind -b 3-1.3.2.1.1"], shell=True)

        print("sudo usbip bind")
        do_release()
        
        return ""

    @app.route('/sdetach', methods=['POST'])
    def detach():

        print("Detach demand recieved.")

        subprocess.run(["sudo usbip unbind -b 3-1.3.2.1.2"], shell=True)
        subprocess.run(["sudo usbip unbind -b 3-1.3.2.1.1"], shell=True)

        print("sudo usbip unbind")
        do_release()
        
        return ""

    app.run(host="0.0.0.0")
        

def client(host):

    app = Flask(__name__)

    @app.route('/cattach', methods=['POST'])
    def attach():
        print("CLIENT: Send attach request")
        addr = "http://{}:{}/".format(host, PORT)
        requests.post(addr + "sattach")

        time.sleep(1)
        
        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe attach -r {host} -b 3-1.3.2.1.2".format(host=host), shell=True)
        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe attach -r {host} -b 3-1.3.2.1.1".format(host=host), shell=True)
        print("usbip.exe attach")
        do_release()

        return ""

    @app.route('/cdetach', methods=['POST'])
    def detach():
        print("CLIENT: Send detach request")
        addr = "http://{}:{}/".format(host, PORT)
        requests.post(addr + "sdetach")

        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe detach -p 00", shell=True)
        subprocess.run("C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe detach -p 01", shell=True)
        print("usbip.exe detach")
        do_release()
        
        return ""

    app.run(host="0.0.0.0")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True)
    #parser.add_argument('--port', required=True)
    #parser.add_argument('--action', required=True, choices=['attach', 'detach'])
    parser.add_argument('--mode', required=True, choices=['client', 'server'])
    
    args = parser.parse_args()


    if args.mode == 'client':
        # hotkey handler
        hkT = threading.Thread(target=hotkey_handler, args=(args.mode, args.host))
        hkT.start()

        # rest api
        cT = threading.Thread(target=client, args=(args.host,))
        cT.start()
        
        hkT.join()
        cT.join()

    else:
        # hotkey handler
        hkT = threading.Thread(target=hotkey_handler, args=(args.mode, args.host))
        hkT.start()

        # rest api
        sT = threading.Thread(target=server, args=(args.host,))
        sT.start()

        hkT.join()
        sT.join()


if __name__ == '__main__':
    main()