import hashlib
import random

class Device:

    def __init__(self, device_id):

        self.device_id = device_id
        self.challenge = ""
        self.obfuscated = ""

    # Receive Challenge from Server
    def receive_challenge(self, challenge):

        self.challenge = challenge

    # LFSR Obfuscation
    # (Placeholder in software because the real LFSR is implemented on FPGA)
    def lfsr_obfuscation(self):

        self.obfuscated = self.challenge

        return self.obfuscated

    # Generate PUF Response
    def generate_response(self, database):

        response = database.get_response(
            self.device_id,
            self.obfuscated
        )

        return response

    # Generate Authentication Token
    def generate_token(self,
                       challenge,
                       response,
                       ks1,
                       ks2):

        data = (
            self.device_id +
            challenge +
            str(response) +
            ks1 +
            ks2
        )

        token = hashlib.sha256(
            data.encode()
        ).hexdigest()

        return token

    # Verify Server (Mutual Authentication)
    def verify_server(self,
                      server_token,
                      ks1,
                      ks2):

        expected = hashlib.sha256(
            (ks1 + ks2).encode()
        ).hexdigest()

        return expected == server_token


###############################################################
# Fake Device
###############################################################

class FakeDevice:

    def __init__(self):

        self.device_id = "Fake_Device"
        self.challenge = ""
        self.obfuscated = ""

    def receive_challenge(self, challenge):

        self.challenge = challenge

    def lfsr_obfuscation(self):

        self.obfuscated = self.challenge

        return self.obfuscated

    # Fake Device simply guesses
    def generate_response(self, database):

        return random.randint(0, 1)

    # Fake Device also generates a fake token
    def generate_token(self,
                       challenge,
                       response,
                       ks1,
                       ks2):

        fake_data = str(random.randint(0,100000))

        token = hashlib.sha256(
            fake_data.encode()
        ).hexdigest()

        return token

    # Fake Device can never verify the server correctly
    def verify_server(self,
                      server_token,
                      ks1,
                      ks2):

        return False