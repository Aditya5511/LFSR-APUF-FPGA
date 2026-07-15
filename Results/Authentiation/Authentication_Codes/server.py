import random
import hashlib


class Server:

    def __init__(self, database):

        self.database = database

    #########################################################
    # Generate Random Challenge
    #########################################################

    def generate_challenge(self):

        challenge = format(random.randint(0, 255), '08b')

        return challenge

    #########################################################
    # Verify PUF Response
    #########################################################

    def verify_response(self,
                        device_id,
                        challenge,
                        response):

        expected = self.database.get_response(
            device_id,
            challenge
        )

        if expected is None:

            return False

        return expected == response

    #########################################################
    # Verify Authentication Token
    #########################################################

    def verify_token(self,
                     device_id,
                     challenge,
                     response,
                     ks1,
                     ks2,
                     token):

        data = (
            device_id +
            challenge +
            str(response) +
            ks1 +
            ks2
        )

        expected_token = hashlib.sha256(
            data.encode()
        ).hexdigest()

        return expected_token == token

    #########################################################
    # Generate Server Token
    # (Used for Mutual Authentication)
    #########################################################

    def generate_server_token(self,
                              ks1,
                              ks2):

        data = ks1 + ks2

        server_token = hashlib.sha256(
            data.encode()
        ).hexdigest()

        return server_token