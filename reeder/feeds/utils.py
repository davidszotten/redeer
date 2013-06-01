import time


def to_timestamp(dt):
    return int(time.mktime(dt.timetuple()))
