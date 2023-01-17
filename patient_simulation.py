import threading
import db_backend as Database
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
        # self.patient_thread = threading.Thread(target=self.patient_start)
        self.doctors_names = {}

        # self.patient_start()

    def register_patient(self):
        self.db.insert_patient(self.first_name, self.patient_last_name, self.ss_num)
    

    def testing_func(self):
        test_list = basic_tools.select_doctors_names(self.db)
        print(test_list)


    def register_patient_visit(self):
        self.doctors_names = basic_tools.select_doctors_names(self.db)

        doctor_name, doctor_spec = random.choice(self.doctors_names)
        doctor_data = self.db.select_doctor(doctor_name, doctor_spec)

        doctor_work_start = doctor_data.work_start.time().strftime("%H:%M:%S")
        doctor_work_end = doctor_data.work_end.time().strftime("%H:%M:%S")

        
        while True:
            visit_date = basic_tools.random_date()
            if visit_date.strftime('%A') in list(doctor_data.avability):
                break

        while True:
            visit_time = basic_tools.choose_visit_time(doctor_work_start, doctor_work_end)
            visit_flag = self.register_visit_db(visit_date, visit_time, doctor_name)
            if visit_flag:
                break

        # print(visit_date.strftime("%Y-%m-%d"), visit_time.strftime("%H:%M:%S"))


    def run(self):
        # self.patient_thread.start()
        while True:
            if self.thread_stop:
                break
            picked_action = random.choice(self.actions)

            if picked_action == "Register_visit":
                self.register_patient_visit()
            elif picked_action == "Sel_visit":
                self.show_visits()
            # print(f'Running: {self.ss_num}')
            time.sleep(5)
    
    def patient_stop(self):
        self.thread_stop = True
        print(f'Thread with ss_num and last name {self.ss_num}, {self.last_name} shutting down')
        time.sleep(1)
        # self.patient_thread.join()

    def register_visit_db(self, visit_date, visit_time, doctor_last):
        self.db.insert_visit(self.last_name, visit_date, visit_time, self.ss_num, doctor_last)
        row_uuid = self.db.select_visit_timeuuid(self.ss_num, visit_date).visit_uuid
        visit_flag = self.db.insert_doctor_visit(doctor_last, visit_date, visit_time, row_uuid, self.ss_num, self.last_name)
        return visit_flag

    def show_visits(self):
        if self.ss_num:
            visits = self.db.select_visits(self.ss_num)