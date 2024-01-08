#app.py
from address_generator import generate_miner_address
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import hashlib

# Method 1: Generate miner's address using address_generator module
miner_address_1 = generate_miner_address()
print("Miner Address (Method 1):", miner_address_1)

# Method 2: Generate miner's address using cryptography library
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
address = hashlib.sha256(public_key_bytes).hexdigest()
print("Miner Address (Method 2):", address)
