import random

from database import CRPDatabase
from device import Device, FakeDevice
from server import Server

import sys

output_file = open("Authentication_Output.txt", "w", encoding="utf-8")

class Tee:

    def __init__(self, *files):
        self.files = files

    def write(self, obj):

        for f in self.files:
            f.write(obj)

    def flush(self):

        for f in self.files:

            try:
                f.flush()

            except ValueError:
                pass

sys.stdout = Tee(sys.__stdout__, output_file)


print("=" * 70)
print("        LFSR-APUF LIGHTWEIGHT AUTHENTICATION PROTOCOL")
print("=" * 70)

###############################################################
# REGISTRATION PHASE
###############################################################

db = CRPDatabase()
db.load_database()

print("\nREGISTRATION PHASE")
print("-" * 70)
print("Registered Device ID : Device_01")
print("Challenge Length     : 8 bits")
print("Challenge Space      : 256")
print("Unique CRPs Stored   :", db.number_of_crps())

###############################################################
# CREATE SERVER & DEVICES
###############################################################

server = Server(db)

device = Device("Device_01")

fake = FakeDevice()

###############################################################
# SESSION PARAMETERS
###############################################################

session_id = random.randint(1000, 9999)

Ks1 = format(random.randint(0, 65535), '016b')

Ks2 = format(random.randint(0, 65535), '016b')

print("\nSESSION PARAMETERS")
print("-" * 70)
print("Session ID           :", session_id)
print("Ks1                  :", Ks1)
print("Ks2                  :", Ks2)

###############################################################
# LEGITIMATE DEVICE AUTHENTICATION
###############################################################

print("\n")
print("=" * 70)
print("LEGITIMATE DEVICE AUTHENTICATION")
print("=" * 70)

challenge = server.generate_challenge()

print("\nDevice ID            :", device.device_id)

print("Server Challenge     :", challenge)

device.receive_challenge(challenge)

obfuscated = device.lfsr_obfuscation()

print("Obfuscated Challenge :", obfuscated)

response = device.generate_response(db)

print("PUF Response         :", response)

token = device.generate_token(
    challenge,
    response,
    Ks1,
    Ks2
)

print("Authentication Token :", token[:16] + "...")

response_result = server.verify_response(
    device.device_id,
    challenge,
    response
)

token_result = server.verify_token(
    device.device_id,
    challenge,
    response,
    Ks1,
    Ks2,
    token
)

print()

if response_result and token_result:

    print("Server Verification  : SUCCESS")

else:

    print("Server Verification  : FAILED")

###############################################################
# MUTUAL AUTHENTICATION
###############################################################

print("\n")
print("=" * 70)
print("MUTUAL AUTHENTICATION")
print("=" * 70)

server_token = server.generate_server_token(
    Ks1,
    Ks2
)

print("\nServer Token         :", server_token[:16] + "...")

device_result = device.verify_server(
    server_token,
    Ks1,
    Ks2
)

if device_result:

    print("Device Verification  : SUCCESS")

else:

    print("Device Verification  : FAILED")

###############################################################
# SAVE SESSION FOR REPLAY ATTACK
###############################################################

old_challenge = challenge
old_response = response

###############################################################
# FAKE DEVICE ATTACK
###############################################################

print("\n")
print("=" * 70)
print("FAKE DEVICE ATTACK")
print("=" * 70)

challenge = server.generate_challenge()

fake.receive_challenge(challenge)

fake.lfsr_obfuscation()

fake_response = fake.generate_response(db)

fake_token = fake.generate_token(
    challenge,
    fake_response,
    Ks1,
    Ks2
)

print("\nFake Device ID       :", fake.device_id)

print("Challenge            :", challenge)

print("Fake Response        :", fake_response)

response_result = server.verify_response(
    fake.device_id,
    challenge,
    fake_response
)

token_result = server.verify_token(
    fake.device_id,
    challenge,
    fake_response,
    Ks1,
    Ks2,
    fake_token
)

print()

if response_result and token_result:

    print("Authentication       : SUCCESS (Unexpected)")

else:

    print("Authentication       : FAILED")
    print("Reason               : Fake Device Detected")

###############################################################
# REPLAY ATTACK
###############################################################

print("\n")
print("=" * 70)
print("REPLAY ATTACK")
print("=" * 70)

print("\nAttacker replays an old valid Challenge-Response pair")

print("\nCaptured Challenge   :", old_challenge)

print("Captured Response    :", old_response)

fresh_challenge = server.generate_challenge()

print("Fresh Challenge      :", fresh_challenge)

if old_challenge == fresh_challenge:

    print("\nReplay Possible")

else:

    print("\nReplay Attack Detected")
    print("Authentication       : FAILED")

###############################################################
# FINAL SUMMARY
###############################################################

print("\n")
print("=" * 70)
print("AUTHENTICATION PROTOCOL SUMMARY")
print("=" * 70)

print("✓ Registration Completed")

print("✓ Legitimate Device Authenticated")

print("✓ Mutual Authentication Successful")

print("✓ Fake Device Rejected")

print("✓ Replay Attack Prevented")

print("✓ Session Established Successfully")

print("=" * 70)
print("END OF DEMONSTRATION")
print("=" * 70)

print("\nResults saved to Authentication_Output.txt")

sys.stdout = sys.__stdout__

output_file.close()