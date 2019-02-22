import requests, bs4
from urllib.request import urlopen
from pytesseract import image_to_string
import cv2
import numpy as np
import subprocess
import argparse
import sys

def check_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-c', '--config', help='VPNBook config file: -c config_file.ovpn')

    args_list = parse.parse_args()

    return args_list

def get_password(url):
    response = urlopen(url)
    arr = np.asarray(bytearray(response.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, 0)
    # correct password depends on picking correct size. sometimes it returns wrong pass
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    password = image_to_string(img, lang="eng")
    return password

def get_creds(url):
    print("[*] Trying to get credentials from vpnbook.com")
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')

    username_line = soup.find('ul', class_="tabs-content").find('li', id='openvpn').find('ul').find_all('li')[-2]
    username = username_line.text.split(":")[1].strip()

    # find image with password and get plain text password
    url += soup.find('ul', class_="tabs-content").find('li', id='openvpn').find('img')['src']
    password = get_password(url)

    return username, password

def save_creds(usr, psw):
    with open('pass.txt', 'w') as creds:
        creds.write(f"{usr}\n{psw}")
    print('[+] Credentials are saved and ready to use')

def connect(vpn_file):
    try:
        print("[*] Trying to connect to VPN server.")

        command = f"openvpn --config {vpn_file} --auth-user-pass pass.txt"
        connection = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

        while True:
            output = connection.stdout.readline().decode('utf-8')

            if output == '' and connection.poll() is not None:
                print("[!] Disconnected!!!")
                break

            if output:
                print(output.strip())
                if "Initialization Sequence Completed" in output:
                    print("\n[+] Successfully connected to VPN. Opening Firefox")
                    subprocess.call(['firefox', 'whoer.net'])

    except KeyboardInterrupt:
        print("[!] Ctrl-C pressed. Terminate connection...")
    except:
        print("[!] Disconnected!!!")


def main():
    url = "https://www.vpnbook.com/"

    config = check_args().config
    if config is None:
        sys.exit("[-] Error. You didn't specify openvpn config file.")
    print(f"[!] Configuration file was specified: {config}")

    username, password = get_creds(url)
    print(f'[+] username {username}\n[+] password: {password}')
    save_creds(username, password)

    connect(config)

if __name__ == '__main__':
    main()