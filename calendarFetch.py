import json
import os
from datetime import datetime
from sqlite3 import OperationalError

from timeconverter import createDatetime


def getEvents(db, deltaKey):
    """Get all events from the database"""
    # Input validation
    if deltaKey is None or deltaKey == "":
        print("Error: Invalid deltatoken")
        return None
    if not db:
        print("Database not specified")
        return None
    try:
        query = """ SELECT location_id, summary, description, start_date, end_date, conference_url_detected, rowid, calendar_id FROM calendaritem WHERE rowid > ? AND all_day = 0 AND start_date < ? """

        max_date = datetime.timestamp(datetime.now())
        max_date /= 1000000

        max_date = datetime.fromtimestamp(max_date)

        result = db.execute(query, (deltaKey, max_date,))
        fetch = result.fetchall()
        if len(fetch) == 0:
            print("No events found. You're all set.")
            return None
    except OperationalError as e:
        print("Error: Database is not initialized properly")
        print(f"   {e}")
        return None
    return fetch


def getNewCalendarDelta(db):
    """Get new calendar delta from the database"""
    # Input validation
    if not db:
        print("Database not specified")
        return None
    try:
        query = """ SELECT rowid FROM calendaritem WHERE all_day = 0 AND start_date < ? ORDER BY display_order DESC LIMIT 1 """
        
        max_date = datetime.timestamp(datetime.now())
        max_date /= 1000000

        max_date = datetime.fromtimestamp(max_date)
        
        result = db.execute(query, (max_date,))
        fetch = result.fetchall()
        if len(fetch) != 1:
            return None
    except OperationalError as e:
        print("Error: Database is not initialized properly")
        print(f"   {e}")
        return None
    return fetch[0][0]


def locationLookup(db, location_id):
    if location_id is None or location_id == "":
        print("Error: Invalid location id")
        return None
    if not db:
        print("Database not specified")
        return None
    try:
        query = """ SELECT title FROM location WHERE ROWID=? """
        result = db.execute(query, (location_id,))
        fetch = result.fetchall()
        if len(fetch) != 1:
            return None

    except OperationalError as e:
        print("Error: Database is not initialized properly")
        print(f"   {e}")
        return None

    return fetch[0][0]


def getDisplayedName(db, person):
    if person is None or person == "":
        return None
    if not db:
        return None

    try:
        query = """ SELECT display_name, first_name, last_name FROM identity WHERE address LIKE '%' || ? """
        result = db.execute(query, (person,))
        fetch = result.fetchall()
        if len(fetch) != 1:
            return None

        return fetch[0]

    except OperationalError as e:
        print("Error: Database is not initialized properly")
        print(f"   {e}")
        return None


def getParticipants(db, rowID):
    if rowID is None or rowID == "":
        return None
    if not db:
        return None

    try:
        query = """ SELECT email FROM participant WHERE owner_id = ? """
        result = db.execute(query, (rowID,))
        fetch = result.fetchall()
        if len(fetch) == 0:
            return None

        participants = []

        for person in fetch:
            identityQ = getDisplayedName(db, person[0])

            if identityQ is not None:
                displayName = identityQ[0]
                firstName = identityQ[1]
                lastName = identityQ[2]

                if displayName is not None:
                    participants.append(displayName)
                else:
                    name = None

                    if firstName is not None:
                        name = firstName

                    if lastName is not None:
                        name = f"{name} {lastName}"

                    participants.append(name)
        return participants

    except OperationalError as e:
        print("Error: Database is not initialized properly")
        print(f"   {e}")
        return None


def getCalendarGroup(db, ownerID):
    if ownerID is None or ownerID == "":
        return None
    if not db:
        return None

    try:
        query = """ SELECT title FROM calendar WHERE rowid = ? """
        result = db.execute(query, (ownerID,))
        fetch = result.fetchall()
        if len(fetch) != 1:
            return None
        return fetch[0][0]

    except OperationalError as e:
        print("Error: Database is not initialized properly")
        print(f"   {e}")
        return None


def processEvents(db, deltaKey, BASE_PATH):
    if deltaKey is None or deltaKey == "":
        print("Error: Invalid deltatoken")
        return False
    if not db:
        print("Database not specified")
        return False

    events = getEvents(db, deltaKey)
    if events is None:
        return False
    with open(BASE_PATH + "/calendar.json", "wb+") as f:
        f.write("[".encode("utf-8"))

        for event in events:
            location_id = event[0]
            summary = event[1]
            description = event[2]
            start_date = str(event[3]).replace("-", "")
            end_date = str(event[4]).replace("-", "")
            conference_url_detected = event[5]
            participants = getParticipants(db, event[6])
            calendarGroup = getCalendarGroup(db, event[7])

            if location_id != 0:
                location = locationLookup(db, location_id)
                if location == "":
                    location = None
            else:
                location = None
            add = {
                "summary": summary,
                "description": description,
                "start_date": createDatetime(start_date),
                "end_date": createDatetime(end_date),
                "conference_url": conference_url_detected,
                "location": location,
                "participants": str(participants),
                "calendarGroup": calendarGroup
            }
            f.write(f"{json.dumps(add)},".encode("utf-8"))

        # Removes last comma in file
        f.seek(-1, os.SEEK_END)
        f.truncate()

        f.write("]".encode("utf-8"))
    return True
