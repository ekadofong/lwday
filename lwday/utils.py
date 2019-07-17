import datetime


_DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

def now (as_string=False):
    now =  datetime.datetime.now ()
    if as_string:
        return dt_to_string ( now )
    else:
        return now

def dt_to_string ( dt, fmt=_DEFAULT_DATETIME_FORMAT ):
    return dt.strftime ( fmt )

def get_timediff ( s1, s2, fmt=_DEFAULT_DATETIME_FORMAT ):    
    dt1 = datetime.datetime.strptime ( s1, fmt )
    dt2 = datetime.datetime.strptime ( s2, fmt )
    delta_time = dt2-dt1
    if delta_time.days < 0:
        raise ValueError ("time difference is negative!")
    else:
        return delta_time
