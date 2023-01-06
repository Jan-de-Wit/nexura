import hashlib
import json
import math
import os
import sqlite3
import struct
from binascii import hexlify
from datetime import datetime, timedelta
from shutil import rmtree
from sqlite3 import OperationalError

import biplist
import Crypto.Cipher.AES
import requests
from aes_keywrap import aes_unwrap_key
from calendarFetch import getNewCalendarDelta, processEvents
from callHistory import getCallHistoryDelta, processCallInfo
from Crypto.Cipher import AES
from db import dbConn
from decryptor_CLI import decryptBackup
from timeconverter import createDatetime
from whatsappFetch import getNewWhatsappDelta, whatsappFetch

WS_LOCAL_MSG = "        "
WS_SERVER_MSG = "         "
WS_STATUS_MSG = "         "

def getLoginData(BASE_PATH):
    if not os.path.exists(BASE_PATH + "config.json"):
        return None

    with open(BASE_PATH + "config.json", "rb+") as f:
        data = f.read()
    if data is None or data == b'':
        return False
    data = json.loads(data)
    if len(data) < 2:
        return False
    return data


def verifyResponse(response):
    if response is None:
        return None
    if response.status_code != 200:
        print(f"[SERVER] Error: {response.text} \
                \n{WS_SERVER_MSG}Status: {response.status_code}")
        return False
    else:
        text = json.loads(response.text)
        if text == "Success":
            return True
        else:
            print(f"[SERVER] Error: {response.text} \
                    \n{WS_SERVER_MSG}Status: {response.status_code}")
            return False


def main(BASE_PATH_DATA, BASE_PATH_DATABASES):
    if not os.path.exists(BASE_PATH_DATA):
        os.makedirs(BASE_PATH_DATA)
    if not os.path.exists(BASE_PATH_DATABASES):
        os.makedirs(BASE_PATH_DATABASES)

    callHistorySuccess = False
    whatsappSuccess = False
    calendarSuccess = False

    # Gets user credentials from config.json file
    noCredentials = True
    loginData = False
    while noCredentials:
        loginData = getLoginData(BASE_PATH_DATA)
        if not loginData:
            email = str(input("Email: "))
            password = str(input("Password: "))

            if email != "" and password != "":
                add = {
                    "email": email.lower(),
                    "password": password,
                }
                with open(BASE_PATH_DATA + "config.json", "w") as f:
                    f.write(json.dumps(add))
        else:
            noCredentials = False

    # Sets global variables for the urls
    BASE_URL = "http://127.0.0.1:5000/api"
    LOGIN_URL = f"{BASE_URL}/auth/login"
    FETCH_DELTA_URL = f"{BASE_URL}/fetch/deltakeys"
    UPLOAD_DELTA_URL = f"{BASE_URL}/upload/deltakeys"
    UPLOAD_URL = f"{BASE_URL}/upload/json"

    # Gets the authentication token from the server
    print("[STATUS] Logging you in...")

    accessToken = None
    response = requests.post(LOGIN_URL, data={
                             "email": loginData["email"], "password": loginData["password"]})
    if response.status_code != 200:
        if response.text == "User not found":
            configPath = BASE_PATH_DATA + "config.json"
            if os.path.exists(configPath):
                os.remove(configPath)
                print(f"[SERVER] Error: {response.text} \
                        \n{WS_SERVER_MSG}Status: {response.status_code}")
                print("Please supply us with the correct credentials.")
                main(BASE_PATH_DATA, BASE_PATH_DATABASES)
        else:
            print(f"[SERVER] Error: {response.text} \
                    \n{WS_SERVER_MSG}Status: {response.status_code}")
            return False
    else:
        accessToken = json.loads(response.text)["Token"]

    if accessToken is None or accessToken == "":
        print(f"[SERVER] No Authentication Token found. \
                \n{WS_SERVER_MSG}Found: {accessToken}")
        rmtree(BASE_PATH_DATABASES)
        return False

    print("[STATUS] Successfully Authenticated...")

    # Gets user input for decrypting the backup
    backupPassword = str(input(
        "Please enter the password for the iPhone backup (not neccessarily the iPhone's password): "))
    backupFolder = str(input("Please enter the path to the backup folder: "))

    # Decrypts the backup
    try:
        decryptBackup(BASE_PATH_DATA, backupFolder, backupPassword)
        print("[STATUS] Successfully decrypted the Backup")
    except Exception as e:
        print(f"[LOCAL] An error occurred while decrypting the backup: \
                \n{WS_LOCAL_MSG}{e}")
        return False

    # Gets deltakeys
    print("[STATUS] Fetching Deltatokens...")
    deltaKeys = None
    try:
        deltaKeys = requests.post(FETCH_DELTA_URL, headers={
            "x-access-tokens": accessToken})
    except requests.exceptions.ConnectionError as e:
        deltaKeys = e
        print(f"[SERVER/LOCAL] Failed to connect to the server. \
                \n           Error: {e}")

    if deltaKeys.status_code != 200:
        print(f"[SERVER] Error: {response.text} \
                \n{WS_SERVER_MSG}Status: {deltaKeys.status_code} \
                \n{WS_SERVER_MSG}Missing: DeltaKeys")
        rmtree(BASE_PATH_DATABASES)
        return False
    else:
        if deltaKeys.text is None or deltaKeys.text == "":
            print(f"[SERVER] Error: No delta keys found. \
                    \n{WS_SERVER_MSG}Found: {deltaKeys.text}")
            whatsappDeltaKey = 0
            callHistoryDeltaKey = 0
        else:
            deltaKeys = json.loads(deltaKeys.text)
            try:
                whatsappDeltaKey = deltaKeys["WhatsApp"]
                callHistoryDeltaKey = deltaKeys["CallHistory"]
                calendarDeltaKey = deltaKeys["Calendar"]

                if whatsappDeltaKey is None:
                    whatsappDeltaKey = 0
                if callHistoryDeltaKey is None:
                    callHistoryDeltaKey = 0
                if calendarDeltaKey is None:
                    calendarDeltaKey = 0
            except KeyError as e:
                print(f"[SERVER] Error: {deltaKeys['exception']}, {deltaKeys['message']} \
                        \n{WS_SERVER_MSG}Status: {deltaKeys.status_code} \
                        \n{WS_SERVER_MSG}Missing: DeltaKeys")
                print(f"[LOCAL] Corresponding error: \
                        \n{WS_LOCAL_MSG}{e}")
                return False

    print("[STATUS] Successfully fetched the Deltatokens \
            \n[STATUS] Starting data processing...")

    whatsappDBPath = BASE_PATH_DATABASES + "ChatStorage.sqlite"
    whatsappDB = dbConn(whatsappDBPath)
    newWhatsappDelta = getNewWhatsappDelta(whatsappDB)

    if newWhatsappDelta != whatsappDeltaKey:
        print(f"[STATUS] Fetching WhatsApp Messages.")
        if whatsappFetch(BASE_PATH_DATABASES, whatsappDB, whatsappDeltaKey):
            filePath = BASE_PATH_DATABASES + "messages.json"
            responseWhatsapp = None
            try:
                with open(filePath, "rb") as filedata:
                    responseWhatsapp = requests.post(UPLOAD_URL, headers={
                        "x-access-tokens": accessToken}, files={'file': filedata})
            except requests.exceptions.ConnectionError as e:
                responseWhatsapp = e

            if os.path.exists(filePath):
                os.remove(filePath)
        else:
            print("[LOCAL] Error: Failed to fetch messages. \
                    \nContinuing...")

        if verifyResponse(responseWhatsapp):
            whatsappSuccess = True
            print("[STATUS] Successfully fetched the messages. \
                    \nContinuing...")
    else:
        print("[STATUS] No whatsapp messages to be fetched. You're all set. \
                \nContinuing...")

    callHistoryDBPath = BASE_PATH_DATABASES + "CallHistory.storedata"
    callHistoryDB = dbConn(callHistoryDBPath)
    contactDBPath = BASE_PATH_DATABASES + "AddressBook.sqlitedb"
    contactDB = dbConn(contactDBPath)
    newCallHistoryDelta = getCallHistoryDelta(callHistoryDB)
    if newCallHistoryDelta != callHistoryDeltaKey:
        print(f"[STATUS] Fetching Call History.")
        responseCallHistory = None
        if processCallInfo(callHistoryDB, BASE_PATH_DATABASES, contactDB, callHistoryDeltaKey):
            filePath = BASE_PATH_DATABASES + "calls.json"
            responseCallHistory = None
            try:
                with open(filePath, "rb") as filedata:
                    responseCallHistory = requests.post(UPLOAD_URL, headers={
                                                        "x-access-tokens": accessToken}, files={'file': filedata})
            except requests.exceptions.ConnectionError as e:
                responseCallHistory = e

            if os.path.exists(filePath):
                os.remove(filePath)
        else:
            print("[LOCAL] Error: Failed to fetch Call History. \
                    \nContinuing...")

        if verifyResponse(responseCallHistory):
            callHistorySuccess = True
            print("[STATUS] Successfully fetched the Call History. \
                    \nContinuing...")
    else:
        print("[STATUS] No call history to be fetched. You're all set.\
                \nContinuing...")

    calenderDBPath = BASE_PATH_DATABASES + "Calendar.sqlitedb"
    calenderDB = dbConn(calenderDBPath)
    newCalendarDelta = getNewCalendarDelta(calenderDB)
    if newCalendarDelta != calendarDeltaKey:
        print(f"[STATUS] Fetching Calendar Events.")
        responseCalendar = None
        if processEvents(calenderDB, calendarDeltaKey, BASE_PATH_DATABASES):
            filePath = BASE_PATH_DATABASES + "calendar.json"
            try:
                with open(filePath, "rb") as filedata:
                    responseCalendar = requests.post(UPLOAD_URL, headers={
                        "x-access-tokens": accessToken}, files={'file': filedata})
            except requests.exceptions.ConnectionError as e:
                responseCalendar = e
            if os.path.exists(filePath):
                os.remove(filePath)
        else:
            print("[LOCAL] Error: Failed to fetch Calendar Events. \
                    \nContinuing...")

        if verifyResponse(responseCalendar):
            calendarSuccess = True
            print("[STATUS] Successfully fetched the Calendar Events. \
                    \nContinuing...")
    else:
        print("[STATUS] No calendar events to be fetched. You're all set.\nContinuing...")

    if not whatsappSuccess:
        newWhatsappDelta = None
    if not callHistorySuccess:
        newCallHistoryDelta = None
    if not calendarSuccess:
        newCalendarDelta = None
    
    print("[STATUS] Uploading Deltatokens...")
    if whatsappSuccess or callHistorySuccess or calendarSuccess:
        responseUploadDelta = requests.post(UPLOAD_DELTA_URL, headers={
            "x-access-tokens": accessToken}, data={"WhatsApp": newWhatsappDelta, "CallHistory": newCallHistoryDelta, "Calendar": newCalendarDelta})

        if not verifyResponse(responseUploadDelta):
            print("[SERVER/LOCAL] Error: Something went wrong when uploading the deltatokens")
            return False
    return True

def master():
    BASE_PATH_DATA = os.path.abspath(
        __name__.replace("__main__", "")) + "/AppData/"
    print(f"[CONFIG-FOLDER] {BASE_PATH_DATA}")
    BASE_PATH_DATABASES = BASE_PATH_DATA + "Decrypted/"
    if main(BASE_PATH_DATA, BASE_PATH_DATABASES) == True:
        print(f"[STATUS] Successfully uploaded the items! \
                \n{WS_STATUS_MSG}Note: This doesn't include the failed items..")
    rmtree(BASE_PATH_DATABASES)

if __name__ == "__main__":
    master()
