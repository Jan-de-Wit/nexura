from datetime import datetime

AMOUNT_OF_SECONDS = 978_307_200


def createDatetime(timestamp) -> datetime:
    """ 
    Counters the offset of dates in the IOS databases.\n
    Returns a datetime represented in "YYYY-MM-DD hh:mm:ss" 
    """

    if timestamp is None or timestamp == "":
        return None

    timestamp = float(timestamp) + AMOUNT_OF_SECONDS
    dtObject = datetime.utcfromtimestamp(timestamp)

    return dtObject.strftime('%Y-%m-%d %H:%M:%S')
