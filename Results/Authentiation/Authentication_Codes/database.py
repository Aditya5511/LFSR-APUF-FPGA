import csv

DATABASE_FILE="crp_database.csv"

class CRPDatabase:

    def __init__(self):

        self.database={}

    def load_database(self):

        self.database.clear()

        with open(DATABASE_FILE,"r") as file:

            reader=csv.DictReader(file)

            for row in reader:

                key=(row["DeviceID"],row["Challenge"])

                self.database[key]=int(row["Response"])

    def get_response(self,device_id,challenge):

        return self.database.get((device_id,challenge),None)

    def number_of_crps(self):

        return len(self.database)