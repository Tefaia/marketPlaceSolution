#wallet.py
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class Wallet:
    def __init__(self):
        # Generate a new key pair for the wallet
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def generate_address(self):
        # Generate a new address from the public key
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        address = hashlib.sha256(public_key_bytes).hexdigest()
        return address

    def sign_transaction(self, transaction):
        # Sign a transaction using the private key
        signature = self.private_key.sign(
            transaction.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def check_balance(self, blockchain):
        # Check the balance of the wallet by iterating through blockchain transactions
        balance = 0
        for block in blockchain.chain:
            for tx in block['transactions']:
                if tx['sender'] == self.generate_address():
                    balance -= tx['amount']
                if tx['recipient'] == self.generate_address():
                    balance += tx['amount']
        return balance
