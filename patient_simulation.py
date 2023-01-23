import threading
import db_backend as Database
from cassandra.util import uuid_from_time
from datetime import timedelta, datetime

import time
import random
import basic_tools


class Patient(threading.Thread):
    
    def __init__(self, ss_num, first_name, last_name, database) -> None:
        super(Patient, self).__init__()
        self.ss_num = ss_num
        self.first_name = first_name
        self.last_name = last_name
        self.db = database
        self.thread_stop = False
        self.actions = ["Register_visit", "Sel_visits"]
        self.doctors_names = {}
        self.visit_minutes = timedelta(minutes=5)

        self.succesful_operations = 0
        self.failed_operations = 0

    def register_patient(self):
        self.db.insert_patient(self.first_name, self.last_name, self.ss_num)
    
    def register_patient_visit(self):
        self.doctors_names = basic_tools.select_doctors_names(self.db)
        doctor_name = random.choice(self.doctors_names)
        doctor_data = self.db.select_doctor(doctor_name)

        while True:
            visit_date = basic_tools.random_date().strftime("%Y-%m-%d")
            if basic_tools.check_date_correctnes(visit_date, doctor_data.avability):
                break

        visits_times = self.db.select_visits_by_doctor(doctor_name, visit_date)

        while True:
            visit_time = random.choice(basic_tools.get_visit_hours(doctor_data.work_start, doctor_data.work_end, visits_times, self.visit_minutes))
            time_flag, taken_hours = basic_tools.check_time_correctness(visit_time, self.visit_minutes, visits_times, (doctor_data.work_start, doctor_data.work_end))
            if time_flag:
                register_flag = self.register_visit_db(visit_date, visit_time, doctor_name)
                if register_flag:
                    break


    def run(self):
        self.register_patient()
        while True:
            if self.thread_stop:
                break
            picked_action = random.choice(self.actions)

            if picked_action == "Register_visit":
                self.register_patient_visit()
            elif picked_action == "Sel_visit":
                self.show_visits()
            time.sleep(0.01)
    
    def patient_stop(self):
        self.thread_stop = True
        print(f'Thread with ss_num and last name {self.ss_num}, {self.last_name} shutting down')


    def check_visit_times_by_doctor(self, visit_date, visit_time, doctor_last):
        doctor_mday_list = self.db.select_visits_by_doctor(doctor_last, visit_date)
        for row in doctor_mday_list:
            if row.visit_time.time().strftime('%H:%M:%S') == visit_time and row.ss_num != self.ss_num:
                return False
            return True

    def register_visit_db(self, visit_date, visit_time, doctor_last):
        generated_timeuuid = uuid_from_time(datetime.now())
        self.db.insert_visit_by_doctor(doctor_last, visit_date, visit_time, generated_timeuuid, self.ss_num, self.last_name)
        time.sleep(0.5)
        if self.check_visit_times_by_doctor(visit_date, visit_time, doctor_last):
            self.db.insert_visit_by_patient(doctor_last, visit_date, visit_time, generated_timeuuid, self.ss_num, self.last_name)
            self.succesful_operations += 1
            return True
        else:
            self.db.delete_visits_by_doctor(doctor_last, visit_date, generated_timeuuid)
            self.failed_operations += 1
            return False

    def show_visits(self):
        if self.ss_num:
            visits = self.db.select_visits(self.ss_num)
            self.succesful_operations += 1