from database import CRPDatabase

db = CRPDatabase()

db.load_database()

print("Total CRPs :", db.number_of_crps())

print(db.get_response("00000000"))