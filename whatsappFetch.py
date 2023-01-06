import json
import os
import sqlite3

from timeconverter import createDatetime


def getWhatsappMessages(db, deltaKey):
    """ Queries the database for all stored WhatsApp messages and returns those (DeltaKey has to be a value of Z_PK) """
    # Input validation
    if deltaKey is None or deltaKey == "":
        print("Error: Invalid deltatoken")
        return None
    if not db:
        print("Database not specified")
        return None

    try:
        # Sets up the connection to the database
        query = "SELECT ZISFROMME, ZFROMJID, ZTOJID, ZMESSAGEDATE, ZTEXT, ZGROUPMEMBER, Z_PK FROM ZWAMESSAGE WHERE Z_PK>?;"

        # Queries the database to get all of the messages (in delta)
        result = db.execute(query, (deltaKey,))
        fetch = result.fetchall()
        if len(fetch) == 0:
            print("No messages found. You're all set.")
            return None
        return fetch
    except sqlite3.OperationalError:
        print("Error: Database is not initialized properly")
        return None


def getDisplayedName(db, JID):
    """ Returns displayed name mentioned in the ZWACHATSESSION database using a JID """
    if not db:
        print("Error: Database not specified")
        return None
    if not JID or JID == "":
        print("Error: No phonenumber specified")

    try:
        query = "SELECT ZPARTNERNAME FROM ZWACHATSESSION WHERE ZCONTACTJID=?"
        result = db.execute(query, (JID,))

        fetch = result.fetchall()
        if len(fetch) != 1:
            # print("Error: Could not get contacts' name")
            return None

        return fetch[0][0]
    except sqlite3.OperationalError:
        print("Error: Database not initialized properly")
        return None


def getUsernameInGroup(db, ZGROUPMEMBER):
    """ Returns displayed name mentioned in the ZWACHATSESSION table using a ZGROUPMEMBER id """
    if not db:
        print("Error: Database not specified")
        return None
    if not ZGROUPMEMBER or ZGROUPMEMBER == "":
        print("Error: No groupmember specified")

    try:
        query = "SELECT ZPARTNERNAME, ZCONTACTJID FROM ZWACHATSESSION WHERE ZCONTACTJID=(SELECT ZMEMBERJID FROM ZWAGROUPMEMBER WHERE Z_PK=?);"
        result = db.execute(query, (ZGROUPMEMBER,))
        fetch = result.fetchall()
    except sqlite3.OperationalError:
        print("Error: Database not initialized properly")
        return None

    if len(fetch) != 1:
        return None

    displayName = fetch[0][0]
    phoneNumberSplit = fetch[0][1].split("@")

    if len(phoneNumberSplit) != 2:
        return [displayName, None]

    phoneNumber = phoneNumberSplit[0]

    return [displayName, phoneNumber]


def getNewWhatsappDelta(db):
    if not db:
        print("Error: Database not specified")
        return None
    try:
        query = "SELECT Z_PK FROM ZWAMESSAGE ORDER BY Z_PK DESC LIMIT 1"
        result = db.execute(query)
        fetch = result.fetchall()

        if len(fetch) != 1:
            print("Error: Empty message list")
            return None
    except sqlite3.OperationalError:
        print("Error: Database not initialized properly")
        return None
    return fetch[0][0]


def processMessages(db, deltaKey, filePath):
    """ Processes all of the messages """
    if deltaKey is None or deltaKey == "":
        print("Error: Invalid deltatoken")
        return False
    if not db:
        print("Error: Database not specified")
        return False

    messages = getWhatsappMessages(db, deltaKey)
    if messages is None or messages == "":
        return False

    with open(filePath, "wb+") as f:
        f.write("[".encode('utf-8'))

        for message in messages:
            # Checks if the message is an image
            if message[4] is not None:
                mID = message[6]
                timestamp = message[3]
                mDateUTC = createDatetime(timestamp)

                mText = message[4]
                mTextPreview = mText[0:255]

                # Makes local variables global
                msgToPhonenumber = None
                msgToUsername = None
                msgFromPhonenumber = None
                msgFromUsername = None
                msgFromUsername = None
                groupName = None

                # Checks if the message is sent by me
                if message[0] == 1:
                    msgToJID = str(message[2])
                    split = msgToJID.split("@")

                    # Checks if it didn't split on more or less points making the address invalid
                    if len(split) == 2:
                        # Checks if the message was sent in a group or private chat
                        domain = split[1]

                        if domain == "s.whatsapp.net":
                            msgToUsername = getDisplayedName(db, msgToJID)
                            msgToPhonenumber = split[0]
                            msgType = "fm_dm"
                        elif domain == "g.us":
                            msgToUsername = getDisplayedName(db, msgToJID)
                            msgType = "fm_gm"

                else:
                    msgFromJID = str(message[1])
                    split = msgFromJID.split("@")

                    if len(split) == 2:
                        domain = split[1]
                        ZGROUPMEMBER = message[5]

                        if domain == "s.whatsapp.net":
                            msgType = "nfm_dm"
                            msgFromUsername = getDisplayedName(db, msgFromJID)
                            msgFromPhonenumber = split[0]
                        elif domain == "g.us":
                            msgType = "nfm_gm"
                            groupName = getDisplayedName(db, msgFromJID)
                            if ZGROUPMEMBER is not None:
                                displayName = getUsernameInGroup(
                                    db, ZGROUPMEMBER)
                                if displayName is None:
                                    displayName = ["User not found", "Unknown"]
                                msgFromUsername = displayName[0]
                                msgFromPhonenumber = displayName[1]
                add = {
                    "msgType": msgType,
                    "mID": mID,
                    "mDateUTC": mDateUTC,
                    "mText": mText,
                    "mTextPreview": mTextPreview,
                    "msgToUsername": msgToUsername,
                    "msgToPhonenumber": msgToPhonenumber,
                    "msgFromUsername": msgFromUsername,
                    "msgFromPhonenumber": msgFromPhonenumber,
                    "msgGroupname": groupName,
                }
                f.write(f"{json.dumps(add)},".encode("utf-8"))

        # Removes last comma in file
        f.seek(-1, os.SEEK_END)
        f.truncate()

        f.write("]".encode("utf-8"))
    return True


def whatsappFetch(BASE_PATH, db, deltaKey):
    """ Gets all of the whatsapp messages and returns them to the server """
    if deltaKey is None or deltaKey == "":
        print("Deltakey not specified")
        return False
    if BASE_PATH is None:
        print("Base path not specified")
        return False
    if not db:
        print("Database not specified")
        return False

    filePath = BASE_PATH + "messages.json"

    if not processMessages(db, deltaKey, filePath):
        print("Error: Failed to process messages.")
        return False
    return True
