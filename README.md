# ChubbyBunny Framework
## BIG UPDATE VERY SOON

[![Version](https://img.shields.io/badge/ChubbyBunny-1.0.0-brightgreen.svg)]()
[![Stage](https://img.shields.io/badge/Release-Stable-brightgreen.svg)]()
[![Build](https://img.shields.io/badge/Supported_OS-Linux-orange.svg)]()

<img align="left" width="150" height="300"  src="https://image.flaticon.com/icons/svg/1303/1303583.svg">

__This project requires Python 3.__ This is a basic reverse shell with custom commands all coded in Python 3. This is a PROTOTYPE ONLY. There are still many bugs. **Using this professionaly is not recommended**. The list of upcoming features are bugs are listed down below. Feel free to report any more bugs you find or any features you would think be cool to add.

## Linux operating systems I recommend :cd::
- Kali Linux 2
- Cyborg
- Parrot
- BackTrack
- Backbox
- Devuan

## How to Install :arrow_down::
#### Please use Linux for server and Windows x86 for client
1. ```git clone https://github.com/0BL1V10N-V01D/ChubbyBunny.git```
2. ```cd ChubbyBunny```
3. ```pip install -r requirements.txt```

## How to Use :question::
1. ```cd ChubbyBunny```
2. Find ```client.py``` file in downloaded directory
3. Go to line 26 and replace the default connect back address with what you want
4. Go to line 47 and replace the port with what you want
5. Save file
6. ```python3 server.py```
7. Now send the client.py to your client

## Upcoming Features :white_check_mark::
#### Short-term goals:
* Create a way list all connected USB devices
* Create a way to take a picture through the camera and send it
* Stream a live feed of the camera to an http server
* Lock keyboard
* Lock mouse
* Make a keylogger or mouselogger
* Remove directories
* Delete the functionality of <kbd>^C
#### Long-term goals:
* Change desktop background
* A way to find password hash
* Create a way to maintain connection

## Bugs :beetle::
* Inproper socket exit on both machines
* The actual shell part of the code doest't work (it's very glitchy)
* __Submit any issues that you find__
