import random
import csv

DATABASE_FILE = "crp_database.csv"

DEVICE_ID = "Device_01"

NUM_CRPS = 1000


def register_device():

    print("="*50)
    print("REGISTRATION PHASE")
    print("="*50)

    with open(DATABASE_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["DeviceID","Challenge","Response"])

        for i in range(NUM_CRPS):

            challenge = format(random.randint(0,255),'08b')

            response = random.randint(0,1)

            writer.writerow([DEVICE_ID,challenge,response])

    print()
    print("Registration Completed")
    print("Device ID :",DEVICE_ID)
    print("CRPs Stored :",NUM_CRPS)


if __name__ == "__main__":

    register_device()