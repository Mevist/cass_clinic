from cassandra.cluster import Cluster
from console_app import App
from db_backend import Database
from patient_simulation import Patient

if __name__ == "__main__":
 
    # try:
    db = Database()
    # except Exception as e:
    #     print("ERRRRRRRRRRRRROR")
    #     print(e)
    # patient = Patient('9909040', 'Szymi', 'Test', db)

    cl_app = App(db)

    while cl_app.active:
        cl_app.menu()

        action = input('Choose action: ')
        cl_app.execute(action)

    db.close()