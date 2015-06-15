import time
import unicodedata

def filter_nick(name):
    """
    filter_nick(name) -> String

    Process the name and get rid of all whitespace, invisible characters and
    make it all lower case.
    """

    ret = "".join(c for c in name if unicodedata.category(c)[0] not in ["C", "Z"])

    ret = "".join(ret.split())
    ret = ret.lower()

    return ret

def extract_time(seconds):
    """
    extract_time(seconds) -> String

    Turn the time in seconds to a string containing the time formatted into
    hours and minutes.
    """

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    if (h == 0 and m == 0):
        return "%ds" % s
    elif (h == 0):
        return "%dm %ds" % (m, s)
    else:
        return "%dh %dm %ds" % (h, m, s)
