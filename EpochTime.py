from datetime import datetime,timedelta

def get_current_time():
    return datetime.now()

def get_current_utc_time():
    return datetime.utcnow()


def epoch_time():
    return datetime(1970,1,1)

def get_current_epoch_time():
    epoch = epoch_time()
    current = get_current_utc_time()
    return (current-epoch).total_seconds()

def get_epoch_time(day, month, year, hour, minute, second=None):
    epoch = epoch_time()
    if second:
        time = datetime(year,month,day,hour,minute,second)
    else:
        time = datetime(year,month,day,hour,minute,0)
    time = time - timedelta(hours=10)
    return (time - epoch).total_seconds()
