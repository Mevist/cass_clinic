from cassandra.cluster import Cluster
from console_app import App
from db_backend import Database
from patient_simulation import Patient

if __name__ == "__main__":
 
    db = Database()

    cl_app = App(db)

    while cl_app.active:
        cl_app.menu()

        action = input('Choose action: ')
        cl_app.execute(action)

    db.close()