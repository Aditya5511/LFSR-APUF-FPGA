import csv

DATABASE_FILE = "crp_database.csv"


def authenticate(challenge,response):

    with open(DATABASE_FILE,"r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Challenge"]==challenge:

                expected=int(row["Response"])

                if expected==response:

                    return True

                else:

                    return False

    return False