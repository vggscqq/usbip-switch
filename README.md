# usbip-switch

Usbip-switch is a virtual KVM(except no V), which allows fast switching keyboard and mouse between two computers in one LAN.

## Project terminology:
* server - linux PC with keyboard and mouse connected to it. a.k.a. `--shost`
* client - windows or linux* PC without neither keyboard nor mouse. a.k.a. `--chost`

## Instalation:
1. `git clone https://github.com/vggscqq/usbip-switch.git`
2. `cd usbip-switch`
3. `sudo pip install -r ./requirements.txt` // sudo required since server app needs root permissions in order to run `usbip`

## Getting started:

### Server:
1. Load usbip kernel module
    `sudo modprobe usbip_host`
2. You might need to replace IDs of your devices on `aio.py` line 10
3. Replace path to your `usbip.exe` on `aio.py` line 11 (see below for installation)
4. Start server usbip-switch server
    `sudo python aio.py --mode server --lhost 192.168.1.169 --rhost 192.168.1.167`

### Client (windows example):
1. Download usbip.exe https://github.com/cezanne/usbip-win
2. Run `python win_client.py`

## Usage:
Open in your web browser http://SERVER_IP:5000