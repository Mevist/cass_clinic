from datetime import datetime, time, timedelta, date
from random import randrange, random

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def date_to_datetime():
    return True

def doctors_workdays(cass_set):
    work_days = [day for day in weekdays if day in cass_set]
    return work_days

def select_doctors_names(db):
    rows = db.select_doctors_names()
    return [(name, spec) for name, spec in rows]

def random_ssnum(ss_nums_list):
    return str(ss_nums_list.pop(randrange(0, len(ss_nums_list))))

def read_names(filename):
    surnames = []
    filename = "./" + filename
    with open(filename, 'r') as data_file:
        for line in data_file:
            surnames.extend(line.strip().split(',')) 
    return surnames

def rand_datetime(start, end):

    return datetime.fromtimestamp(randrange(
        round(start.timestamp()), round(end.timestamp())
    ))

def choose_visit_time(start, end):
    start = time.fromisoformat(start)
    end = time.fromisoformat(end)
    return rand_datetime(
        datetime.combine(dt0 := datetime.fromtimestamp(0), start),
        datetime.combine(
            dt0 if start < end else dt0 + timedelta(days=1),
            end
        )
    ).time()

def random_date():
    start_date = date.today()
    end_date = start_date + timedelta(days=30)
    return start_date + (end_date - start_date) * random()