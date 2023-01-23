from cassandra.cluster import Cluster, ConsistencyLevel
from cassandra.cluster import ExecutionProfile, EXEC_PROFILE_DEFAULT
#  
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import named_tuple_factory



class Database():
        
    def __init__(self, addresses=['127.0.0.1'], port=9042):
        self.profile = ExecutionProfile(
            consistency_level=ConsistencyLevel.QUORUM,
            # request_timeout=30,
            row_factory=named_tuple_factory
        )   

        self.cluster = Cluster(execution_profiles={EXEC_PROFILE_DEFAULT: self.profile})
        try:
            self.session = self.cluster.connect('clinic', wait_for_all_pools=True)
        except Exception as e:
            print("Could not connect to the cluster. ", e)
            raise e

        try:
            self.slc_patient_statement = self.session.prepare \
                ("SELECT * from patient WHERE ss_num=?;")
            self.slc_doctor_statement = self.session.prepare \
                ("SELECT * FROM doctor WHERE doctor_surname=?;")
            self.ins_patient_statement = self.session.prepare \
                ("INSERT INTO patient (first_name, patient_surname, ss_num) \
                    VALUES (?, ?, ?);")
            self.ins_visit_by_doctor_statement = self.session.prepare \
                ("INSERT INTO visits_by_doctor (doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname) \
                     VALUES (?, ?, ?, ?, ?, ?);")
            self.ins_visit_by_patient_statement = self.session.prepare \
                ("INSERT INTO visits_by_patient (doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname) \
                    VALUES (?, ?, ? ,?, ?, ?);")        
            self.slc_visits_by_patient_statement = self.session.prepare \
                ("SELECT * FROM visits_by_patient WHERE ss_num=?;")
            self.slc_visits_by_patient_mday_statement = self.session.prepare \
                ("SELECT * FROM visits_by_patient WHERE ss_num=? AND m_day=?;")
            self.slc_visits_by_doctor_statement = self.session.prepare \
                ("SELECT * FROM visits_by_doctor WHERE doctor_surname=? AND m_day=?;")
            self.slc_visit_timeuuid_statement = self.session.prepare \
                ("SELECT * FROM visits_by_patient WHERE ss_num=? AND m_day=?;")
            self.del_visit_by_doctor_statement = self.session.prepare \
                ("DELETE FROM visits_by_doctor WHERE doctor_surname=? AND m_day=? AND visit_uuid=?;")
            self.del_visit_by_patient_statement = self.session.prepare \
                ("DELETE FROM visits_by_patient WHERE ss_num=? AND m_day=? AND visit_uuid=?;")
            self.slc_doctors_names_statement = self.session.prepare \
                ("SELECT doctor_surname FROM doctor;")
        except Exception as e:
            print("Cant prepare statement")
            raise e
    
    def select_patient(self, ss_num):
        row = self.session.execute(self.slc_patient_statement,[ss_num]).one()
        return row
    
    def select_count(self, table):
        row = self.session.execute(f'select COUNT(*) from {table};')
        return row

    def select_doctor(self, doctor_surname):
        row = self.session.execute(self.slc_doctor_statement,[doctor_surname]).one()
        return row

    def insert_patient(self, first_name, patient_surname, ss_num):
        self.session.execute(self.ins_patient_statement,\
            [first_name, patient_surname, ss_num]).one()

    def insert_visit_by_doctor(self, doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname):
        return self.session.execute(self.ins_visit_by_doctor_statement, \
            [doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname])

    def insert_visit_by_patient(self, doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname):
        return self.session.execute(self.ins_visit_by_patient_statement,\
            [doctor_surname, m_day, visit_time, visit_uuid, ss_num, patient_surname])
    
    def select_visits_by_patient_mday(self, ss_num, m_day):
        rows = []
        try:
            rows = self.session.execute(self.slc_visits_by_patient_mday_statement,\
                [ss_num, m_day]).one()
        except Exception as e:
            print(e)
        else: return rows

    def select_visits_by_patient(self, ss_num):
        rows = []
        try:
            rows = self.session.execute(self.slc_visits_by_patient_statement,\
                [ss_num])
        except Exception as e:
            print(e)
        else: return rows

    def select_visits_by_doctor(self, doctor_surname, m_day):
        rows = []
        try:
            rows = self.session.execute(self.slc_visits_by_doctor_statement,\
                [doctor_surname, m_day])
        except Exception as e:
            print(e)
        return rows
    
    def select_doctors_names(self):
        rows = []
        try:
            rows = self.session.execute(self.slc_doctors_names_statement,\
                [])
        except Exception as e:
            print(e)
        else: return rows
    
    def select_visit_timeuuid(self, ss_num, m_day):
        try:
            row = self.session.execute(self.slc_visit_timeuuid_statement, [ss_num, m_day]).one()
        except Exception as e:
            print(e)
        else: return row
    
    def delete_visits_by_doctor(self, doctor_surname, m_day, visit_uuid):
        try:
            self.session.execute(self.del_visit_by_doctor_statement, [doctor_surname, m_day, visit_uuid])
        except Exception as e:
            print(e)
    
    def delete_visits_by_patient(self, ss_num, m_day, visit_uuid):
        try:
            self.session.execute(self.del_visit_by_patient_statement, [ss_num, m_day, visit_uuid])
        except Exception as e:
            print(e)

    def close(self):
        self.cluster.shutdown()