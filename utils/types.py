import parsedatetime
from time import mktime
from datetime import date


def parse_str_date(string):
    """ 
    make a date out of
    string using parsedatetime lib,
    return for import
    https://pypi.python.org/pypi/parsedatetime/
    """
    if string:
        try:
            the_date = date.fromtimestamp(mktime(parsedatetime.Calendar().parse(string)[0]))
            if the_date != date.today():
                return the_date
        except:
            return None

def intify(string):
    if not string:
        return 0
    try:
        return int(string)
    except:
        return None

