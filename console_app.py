from datetime import datetime
from random import sample, choice
from cassandra.util import uuid_from_time

from db_backend import Database

import os
import basic_tools
import patient_simulation
import time
import uuid
class App:
    
    def __init__(self, database):
        self.patient_surname = 'Brenner'
        self.ss_num = '9909290'
        self.active = True
        self.db = database
        self.menu_msg = f'Logged in as {self.patient_surname}' if self.patient_surname else str()

        self.patients_threads = []
        self.threads_active = True
        self.surnames_list = basic_tools.read_names('surnames')
        self.names_list = basic_tools.read_names('names')
        self.ss_nums_list = sample(range(1000000,9999999), 100)

    def clear_messages(self):
        os.system('clear')
        
    def menu(self):
        print(self.menu_msg)
        # self.clear_messages()
        print(f'1 - Log in')
        print(f'2 - Register patient')
        print(f'3 - Register visit') 
        print(f'4 - Show visits')
        print(f'5 - Delete visit')
        print(f'6 - Start stress test')
        print(f'7 - Stop stress test')
        print(f'8 - Check threads')
        print(f'Q - Exit')

    def execute(self, action):
        self.clear_messages()
        self.menu_msg = str()
        if action.isalpha():
            action = action.upper()

        if action == '1':
            self.log_in()
        elif action == '2':
            self.register_patient()
        elif action == '3':
            self.register_visits()
        elif action == '4':
            self.show_visits()
        elif action == '5':
            self.del_visit_menu()
        elif action == '6':
            self.start_stress_test()
            # self.patient_main_thread.start()
        elif action == '7':
            self.stop_stress_test()
        elif action == '8':
            self.check_threads()
        elif action == 'Q':
            self.stop_stress_test()
            self.active = False

    def check_threads(self):
        for t in self.patients_threads:
            print(t.is_alive())

    def start_stress_test(self):
        for _ in range(50):
            name_temp = choice(self.names_list)
            last_temp = choice(self.surnames_list)
            ss_num = basic_tools.random_ssnum(self.ss_nums_list)
            print(f'Starting {name_temp}, {last_temp}, {ss_num}')
            self.patients_threads.append(patient_simulation.Patient(ss_num, name_temp, last_temp, self.db))

        for thread_p in self.patients_threads:
            thread_p.start()
        
            
    
    def stop_stress_test(self):
        # self.patient_main_thread.join()
        for thread_p in self.patients_threads:
            thread_p.patient_stop()
            thread_p.join()
        self.patients_threads = []

    def log_in(self):
        patient_last_name = input('Provide your last name: ')
        ss_num = input('Provide your Social Security number: ')
        try:
            patient = self.db.select_patient(ss_num)
        except Exception as e:
            print(f'Couldnt log in as {patient_last_name}. ')
            print(e)
        if patient:
            self.patient_surname = patient_last_name
            self.ss_num = ss_num
            self.menu_msg = "You logged in as " + self.patient_surname
        else:
            print(f'Patient {patient_last_name} is not registered in clinic')

    def register_patient(self):
        first_name = input('Provide your first name: ')
        patient_last_name = input('Provide your last name: ')
        ss_num = input('Provide your Social Security number: ')

        # try except blocks probably will be removed
        try:
            self.db.insert_patient(first_name, patient_last_name, ss_num)
            self.menu_msg = "Patient " + first_name + " " + patient_last_name + " registered"
        except Exception as e:
            print("Couldnt register this patient")
            print(e)

    def del_visit_menu(self):
        self.show_visits()
        print(self.menu_msg)
        print()
        doctor_last = input("What doctor visit you want to cancel? ")
        m_day = input("and at what day? ")
        self.delete_visit(doctor_last, m_day)
        self.menu_msg = "Visit on " + m_day + " canceled"

    def delete_visit(self, doctor_last, m_day):
        visit_uuid = self.db.select_visit_timeuuid(self.ss_num, m_day).visit_uuid

        self.db.delete_visits_by_doctor(doctor_last, m_day, visit_uuid)
        self.db.delete_visits_by_patient(self.ss_num, m_day, visit_uuid)

    def update_visit(self):
        pass

    def check_doctor_availability(self, doctor_last):
        doctor = self.db.select_doctor(doctor_last)

        work_days = basic_tools.doctors_workdays(doctor.avability)
        return (work_days, doctor.work_start, doctor.work_end)
    
    def register_visit_db(self, visit_date, visit_time, doctor_last):
        generated_timeuuid = uuid_from_time(datetime.now())
        self.db.insert_visit_by_doctor(doctor_last, visit_date, visit_time, generated_timeuuid, self.ss_num, self.patient_surname)
        time.sleep(1)
        # make here select on doctor_last, visit_date, create function to validate if
        # added visits is the only one at the time, if yes add row to visit_by_patient
        # else delete the one row from visits_by_doctor

    def register_visits(self, ):
        if self.ss_num:
            doctor_last = input('Provide Doctors last name: ')
            # doctor_specialization = input('Provide Doctors specialization: ')

            doctor_hours = self.check_doctor_availability(doctor_last)
            print(f'Doctor is working on {", ".join(f"{day}" for day in doctor_hours[0])} \
                from {doctor_hours[1].time().strftime("%H:%M:%S")} to {doctor_hours[2].time().strftime("%H:%M:%S")}')

            visit_date = input('Provide date of visit: ')
            visit_time = input('and time: ')

            visit_flag = self.register_visit_db(visit_date, visit_time, doctor_last)

            if visit_flag:
                self.menu_msg = "Visit registered"
                # print(f'TESTING {visit_flag}')
            else:
                self.menu_msg = "Wrong date, pick another"
                # print(f'TESTING {visit_flag}')
        else:
            print("First you must log in to register visits")

    def show_visits(self):
        if self.ss_num:
            visits = self.db.select_visits_by_patient(self.ss_num)
            for row in visits:
                for item in row:
                    self.menu_msg += str(item) + " | "
                self.menu_msg += " \n"
        else:
            print("First you must log in to check visits")