from cassandra.cluster import Cluster
#  ExecutionProfie, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory



class Database():
        
    def __init__(self, addresses=['127.0.0.1'], port=9042):
        # self.profile = ExecutionProfile(
        #     load_balancing_policy=WhiteListRoundRobinPolicy(['127.0.0.1']),
        #     retry_policy=DowngradingConsistencyRetryPolicy(),
        #     consistency_level=ConsistencyLevel.LOCAL_QUORUM,
        #     serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
        #     request_timeout=15,
        #     row_factory=tuple_factory
        # )   

        # cluster = Cluster(execution_profiles={EXEC_PROFILE_DEFAULT: profile})
        # session = cluster.connect()
        self.cluster = Cluster(addresses, port)
        try:
            self.session = self.cluster.connect('clinic', wait_for_all_pools=True)
        except Exception as e:
            print("Could not connect to the cluster. ", e)
            raise e

        try:
            self.slc_patient_statement = self.session.prepare \
                ("SELECT * from patient WHERE ss_num=?;")
            self.slc_doctor_statement = self.session.prepare \
                ("Select * from doctor WHERE last_name=? AND specialization=?;")
            self.ins_patient_statement = self.session.prepare \
                ("INSERT INTO patient (first_name, last_name, ss_num) \
                    VALUES (?, ?, ?);")
            self.ins_doctor_visit = self.session.prepare \
                ("INSERT INTO doctor_visits (last_name, m_day, visit_time, visit_uuid, ss_num, patient_last) \
                     VALUES (?, ?, ?, ?, ?, ?) IF NOT EXISTS;")
            self.ins_visit_statement = self.session.prepare \
                ("INSERT INTO visits (visit_uuid, patient_last, m_day, visit_time, ss_num, doctor_last) \
                    VALUES (now(), ?, ? ,?, ?, ?) IF NOT EXISTS;")        
            self.slc_visits_statement = self.session.prepare \
                ("SELECT * FROM visits WHERE ss_num=?;")
            self.slc_doctor_visits_statement = self.session.prepare \
                ("SELECT * FROM doctor_visits WHERE last_name=? AND m_day=?;")
            self.slc_visit_timeuuid = self.session.prepare \
                ("SELECT * FROM visits WHERE ss_num=? AND m_day=?;")
            self.del_doctor_visit = self.session.prepare \
                ("DELETE FROM doctor_visits WHERE last_name=? AND m_day=? AND ss_num=?;")
            self.del_visit = self.session.prepare \
                ("DELETE FROM visits WHERE ss_num=? AND m_day=? AND doctor_last=?;")
            self.slc_doctors_names = self.session.prepare \
                ("SELECT last_name, specialization FROM doctor;")
        except Exception as e:
            print("Cant prepare statement")
            raise e
    
    def select_patient(self, ss_num):
        row = self.session.execute(self.slc_patient_statement,[ss_num]).one()
        return row

    def select_doctor(self, doctor_last, specialization):
        row = self.session.execute(self.slc_doctor_statement,[doctor_last, specialization]).one()
        return row

    def insert_patient(self, first_name, patient_last, ss_num):
        self.session.execute(self.ins_patient_statement,\
            [first_name, patient_last, ss_num]).one()

    def insert_visit(self, patient_last, m_day, visit_time,ss_num, doctor_last):
        return self.session.execute(self.ins_visit_statement,\
            [patient_last, m_day, visit_time, ss_num, doctor_last])
    
    def insert_doctor_visit(self, doctor_last, m_day, visit_time, visit_uuid, ss_num, patient_last):
        return self.session.execute(self.ins_doctor_visit, \
            [doctor_last, m_day, visit_time, visit_uuid, ss_num, patient_last])

    def select_visits(self, ss_num):
        rows = []
        try:
            rows = self.session.execute(self.slc_visits_statement,\
                [ss_num])
        except Exception as e:
            print(e)
        else: return rows
    
    def select_doctors_names(self):
        rows = []
        try:
            rows = self.session.execute(self.slc_doctors_names,\
                [])
        except Exception as e:
            print(e)
        else: return rows

    def select_doctor_visits(self, doctor_last, m_day):
        rows = []
        try:
            rows = self.session.execute(self.slc_doctor_visits_statement,\
                [doctor_last, m_day])
        except Exception as e:
            print(e)
        else: return rows
    
    def select_visit_timeuuid(self, ss_num, m_day):
        try:
            row = self.session.execute(self.slc_visit_timeuuid, [ss_num, m_day]).one()
        except Exception as e:
            print(e)
        else: return row
    
    def delete_doctor_visit(self, doctor_last, m_day, ss_num):
        try:
            self.session.execute(self.del_doctor_visit, [doctor_last, m_day, ss_num])
        except Exception as e:
            print(e)
    
    def delete_visit(self, ss_num, m_day, doctor_last):
        try:
            self.session.execute(self.del_visit, [ss_num, m_day, doctor_last])
        except Exception as e:
            print(e)

    def close(self):
        self.cluster.shutdown()