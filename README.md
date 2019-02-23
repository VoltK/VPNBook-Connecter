# VPNBook-Connecter

## This script will connect you automatically to VPNBook OpenVPN without asking for credentials

### Installation

You will need OpenVPN config file from [VPNBook](https://www.vpnbook.com/)

```
apt-get install -y openvpn
apt install tesseract-ocr
apt install libtesseract-dev
pip3 install pytesseract 
pip3 install requests 
pip3 install beautifulsoup4
```

### Run

```
python3 VPNBookConnect.py -c config_file.ovpn -u (if running for the first time or auth fails)
```
