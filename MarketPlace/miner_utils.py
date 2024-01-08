# miner_utils.py
import hashlib
import random
import string

def generate_miner_address():
    # Generate a random string
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    # Hash the random string using SHA-256
    hashed_address = hashlib.sha256(random_string.encode('utf-8')).hexdigest()

    return hashed_address



























