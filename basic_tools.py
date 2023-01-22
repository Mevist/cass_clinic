from datetime import datetime, time, timedelta, date
from random import randrange, random

search_range = timedelta(days=120)
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def doctors_workdays(cass_set):
    work_days = [day for day in weekdays if day in cass_set]
    return work_days

def select_doctors_names(db):
    rows = db.select_doctors_names()
    return [name.doctor_surname for name in rows]

def check_date_correctnes(week_day : date, doctor_avability : list) -> bool:
    week_day_date_obj = datetime.strptime(week_day, '%Y-%m-%d')
    return week_day_date_obj >= datetime.today() and week_day_date_obj.strftime('%A') in list(doctor_avability)

def check_time_correctness(patient_time, visit_minutes, visits_times, working_time) -> bool:
    list_times = [visit.visit_time.time() for visit in visits_times]
    patient_timestamp = time.fromisoformat(patient_time)
    start_timestamp = working_time[0].time()
    end_timestamp = working_time[1].time()

    if patient_timestamp >= end_timestamp or patient_timestamp < start_timestamp:
        return False, list_times

    if patient_timestamp in list_times:
        return False, list_times

    if not list_times:
        return True, list_times

    list_times.append(patient_timestamp)
    list_times.sort()

    index = list_times.index(patient_timestamp)
    result_end = datetime.combine(date.today(), list_times[index]) + visit_minutes
    result_start = datetime.combine(date.today(), list_times[index]) - visit_minutes

    if index == len(list_times) - 1 and result_end.time() <= end_timestamp:
        return True, list_times

    if list_times[index - 1] <= result_start.time() and list_times[index + 1] >= result_end.time():
        return True
    else: return False, list_times
    # print(result_start.time(), result_end.time(), patient_timestamp)


def random_ssnum(ss_nums_list : list) -> str:
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

def get_visit_hours(start, end, db_visits, visit_minutes):
    db_visits = [visit.visit_time.time() for visit in db_visits]
    visit_hours = []
    start = start.time()
    end = end.time()
    counter_time = start
    while counter_time <= end:
        visit_hours.append(counter_time)
        counter_time = (datetime.combine(date.today(), counter_time) + visit_minutes).time()

    visit_hours = [visit.strftime('%H:%M:%S') for visit in visit_hours if visit not in db_visits]
    return visit_hours

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
    end_date = start_date + search_range
    return start_date + (end_date - start_date) * random()