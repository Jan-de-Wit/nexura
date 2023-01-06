import json
import math
import os
import sqlite3
from datetime import timedelta

from timeconverter import createDatetime

CHARS = "+#( "


def getCallHistory(db, deltaKey):
    """ Gets all of the call events out of the database """
    # Input validation
    if deltaKey is None or deltaKey == "":
        print("Error: Invalid deltatoken")
        return None
    if not db:
        print("Database not specified")
        return None
    try:
        # Gets all of the call events out of the database
        query = "SELECT ZADDRESS, ZDURATION, ZDATE, Z_PK FROM ZCALLRECORD WHERE Z_PK>?"
        result = db.execute(query, (deltaKey,))
        fetchCallInfo = result.fetchall()

        # Checks if it returned any calls
        if len(fetchCallInfo) == 0:
            print("No calls found.")
            return None
    except sqlite3.OperationalError:
        print("Error: Database is not initialized properly")
        return None

    return fetchCallInfo


def cleanNumber(phonenumber, db):
    """ Cleans the phonenumbers to make sure theres no glitches within verifying contacts """
    # Input validation
    if phonenumber is None or phonenumber == "":
        return None
    query = "SELECT ZNORMALIZEDVALUE FROM ZHANDLE WHERE ZVALUE = ? LIMIT 1"
    result = db.execute(query, (phonenumber,))
    result = result.fetchall()

    if len(result) != 1 or result is None:
        phonenumber = phonenumber.replace(" ", "")
        result = db.execute(query, (phonenumber,))
        result = result.fetchall()

        if len(result) != 1 or result is None:
            return phonenumber

    if result is None:
        return None
    else:
        if result[0] is None:
            return None
        else:
            if result[0][0] is None:
                return None
    return result[0][0].replace(" ", "")


def getContacts(contactDB, callDB):
    """ Gets all of the contacts stored in the contact database """
    # Input validation
    if contactDB is None or callDB is None:
        print("Error: Database not specified")
        return None

    contacts = []

    try:
        # Gets all of the contacts' phonenumber and id
        query = "SELECT record_id, value FROM ABMultiValue"
        result = contactDB.execute(query)
        fetch = result.fetchall()

        # Checks if the fetch returned nothing
        if len(fetch) == 0:
            print("Error: No contacts found")
            return None

        for result in fetch:
            add = [result[0], cleanNumber(result[1], callDB)]
            contacts.append(add)
    except sqlite3.OperationalError:
        print("Error: Database is not initialized properly")
        return None

    return contacts


def getContactName(phonenumber, contacts, contactDB, callDB):
    """ Gets the name of a contact based on a phonenumber """
    # Input validation
    if not phonenumber or phonenumber == "":
        return None
    if not contacts or contacts == "":
        print("Error: No contacts specified")
        return None
    if not contactDB or not callDB:
        print("Error: Database not specified")
        return None

    # Cleaning the data
    phonenumber = cleanNumber(phonenumber, callDB)

    fetchName = None
    fetchID = None

    # Checks if the phonenumber is in the address book
    for contact in contacts:
        if phonenumber == contact[1]:
            fetchID = contact[0]
            break

    try:
        # Queries the database to get the needed parameters for the full name
        query = "SELECT First, Middle, Last FROM ABPerson WHERE ROWID=?"
        result = contactDB.execute(query, (fetchID,))
        fetchName = result.fetchall()
    except sqlite3.OperationalError:
        print("Error: Database is not initialized properly")
        return None

    if len(fetchName) == 1:
        # Gets the displayed names and formats them
        first = fetchName[0][0]
        if not first:
            first = ""

        middle = fetchName[0][1]
        if not middle:
            middle = ""

        last = fetchName[0][2]
        if not last:
            last = ""

        # Formats the full displayed name
        full = f"{first} {middle} {last}".replace("  ", " ").strip()

        # Appends the name to a list of names
        return full
    return None


def getCallHistoryDelta(db):
    if not db:
        print("Error: Database not specified")
        return None

    query = "SELECT Z_PK FROM ZCALLRECORD ORDER BY Z_PK DESC LIMIT 1"
    result = db.execute(query)
    fetch = result.fetchall()

    if len(fetch) != 1:
        print("Error: Empty call history")
        return None
    return fetch[0][0]


def processCallInfo(callHistoryDB, BASE_PATH, contactDB, deltaKey):
    """ Processes all of the information about a call event """
    # Input validation
    if not callHistoryDB or not contactDB:
        print("Error: Database(s) not specified")
        return False
    if deltaKey is None or deltaKey == "":
        print("Error: No deltatoken specified")
        return False
    if BASE_PATH is None:
        print("Error: Base path not specified")
        return False

    filePath = BASE_PATH + "calls.json"
    with open(filePath, "wb+") as f:
        f.write("[".encode("utf-8"))

        # Gets the contacts
        contacts = getContacts(contactDB, callHistoryDB)

        # Contact validation
        if contacts is None or contacts == "":
            print("Error: No contacts found")

        # Gets the callhistory using the deltakey
        callHistory = getCallHistory(callHistoryDB, deltaKey)

        # Callhistory validation
        if callHistory is None or callHistory == "":
            print("Error: No Call History Found")
            os.remove(filePath)
            return False

        for callData in callHistory:
            phonenumber = callData[0]
            duration = callData[1]
            timestamp = callData[2]
            id = callData[3]

            # Gets displayed name out of contacts database
            if phonenumber is not None or phonenumber != "":
                name = getContactName(
                    phonenumber, contacts, contactDB, callHistoryDB)
                if duration is not None or duration != "":
                    duration = str(timedelta(seconds=math.ceil(duration)))
                    if timestamp is not None or timestamp != "":
                        date = createDatetime(timestamp)

                if id is None:
                    id = "None"
                if date is None:
                    date = "None"
                if duration is None:
                    duration = "None"
                if name is None:
                    name = "None"
                if phonenumber is None:
                    phonenumber = "None"
            add = {
                "ID": id,
                "DateUTC": date,
                "Duration": duration,
                "Name": name,
                "Phonenumber": str(str(phonenumber).replace("\\\\", "\\")),
            }
            f.write(f"{json.dumps(str(add))},".encode("utf-8"))

        # Removes last comma in file
        f.seek(-1, os.SEEK_END)
        f.truncate()

        f.write("]".encode("utf-8"))

    return True
