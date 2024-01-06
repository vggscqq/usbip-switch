import socket
import argparse
import time
import subprocess
import threading
import keyboard
import requests
from flask import Flask

PORT = 5000


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


def hotkey_handler(mode, host):
    release_keys()
    if mode == "client":
        keyboard.add_hotkey('ctrl + alt + 1', client_usb, args=('attach', host,))
        keyboard.wait('ctrl + alt + 3')
        exit()
    else:
        keyboard.add_hotkey('ctrl + alt + 2', server_usb, args=('attach', host,))
        keyboard.wait('ctrl + alt + 3')
        exit()


def client_usb(action, host):
    release_keys()
    if action == "attach":
        print("CLIENT: Hotkey handler attach")

        addr = f"http://{host}:{PORT}/"
        requests.post(addr + "sattach")
        time.sleep(1)

        for device_id in ["3-1.3.2.1.2", "3-1.3.2.1.1"]:
            subprocess.run(f"C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe attach -r {host} -b {device_id}", shell=True)
        print("usbip.exe attach")

    else:
        print("CLIENT: Hotkey handler detach")
        for port_id in ["00", "01"]:
            subprocess.run(f"C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe detach -p {port_id}", shell=True)
        print("usbip.exe detach")

        print("CLIENT: HTTP handler detach")
        addr = f"http://{host}:{PORT}/"
        requests.post(addr + "sdetach")

    release_keys()


def server_usb(action, host):
    release_keys()
    if action == "attach":
        for device_id in ["3-1.3.2.1.2", "3-1.3.2.1.1"]:
            subprocess.run(["sudo", "usbip", "bind", "-b", device_id])
        print("sudo usbip bind")

        addr = f"http://{host}:{PORT}/"
        requests.post(addr + "cattach")

    else:
        for device_id in ["3-1.3.2.1.2", "3-1.3.2.1.1"]:
            subprocess.run(["sudo", "usbip", "unbind", "-b", device_id])
        print("sudo usbip unbind")

        addr = f"http://{host}:{PORT}/"
        requests.post(addr + "cdetach")

    release_keys()


def server(host):
    app = Flask(__name__)

    @app.route('/sattach', methods=['POST'])
    def attach():
        print("SERVER: Attach demand received.")
        for device_id in ["3-1.3.2.1.2", "3-1.3.2.1.1"]:
            subprocess.run(["sudo", "usbip", "bind", "-b", device_id])
        print("sudo usbip bind")
        release_keys()
        return ""

    @app.route('/sdetach', methods=['POST'])
    def detach():
        print("Detach demand received.")
        for device_id in ["3-1.3.2.1.2", "3-1.3.2.1.1"]:
            subprocess.run(["sudo", "usbip", "unbind", "-b", device_id])
        print("sudo usbip unbind")
        release_keys()
        return ""

    app.run(host="0.0.0.0")


def client(host):
    app = Flask(__name__)

    @app.route('/cattach', methods=['POST'])
    def attach():
        print("CLIENT: Send attach request")
        addr = f"http://{host}:{PORT}/"
        requests.post(addr + "sattach")

        time.sleep(1)
        for device_id in ["3-1.3.2.1.2", "3-1.3.2.1.1"]:
            subprocess.run(f"C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe attach -r {host} -b {device_id}", shell=True)
        print("usbip.exe attach")
        release_keys()
        return ""

    @app.route('/cdetach', methods=['POST'])
    def detach():
        print("CLIENT: Send detach request")
        addr = f"http://{host}:{PORT}/"
        requests.post(addr + "sdetach")

        for port_id in ["00", "01"]:
            subprocess.run(f"C:\\Users\\vgscq\\Desktop\\usbip\\usbip.exe detach -p {port_id}", shell=True)
        print("usbip.exe detach")
        release_keys()
        return ""

    app.run(host="0.0.0.0")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True)
    parser.add_argument('--mode', required=True, choices=['client', 'server'])
    args = parser.parse_args()

    if args.mode == 'client':
        hkT = threading.Thread(target=hotkey_handler, args=(args.mode, args.host))
        hkT.start()

        cT = threading.Thread(target=client, args=(args.host,))
        cT.start()

        hkT.join()
        cT.join()
    else:
        hkT = threading.Thread(target=hotkey_handler, args=(args.mode, args.host))
        hkT.start()

        sT = threading.Thread(target=server, args=(args.host,))
        sT.start()

        hkT.join()
        sT.join()


if __name__ == '__main__':
    main()
