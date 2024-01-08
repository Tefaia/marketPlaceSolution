#miner.py
import hashlib
import time

class Miner:
    def __init__(self, node, blockchain):
        self.node = node
        self.blockchain = blockchain

    def mine(self, transactions):
        # Get the last block in the blockchain
        last_block = self.blockchain.get_last_block()

        # Create a new block
        new_block = {
            'index': last_block['index'] + 1,
            'timestamp': time.time(),
            'transactions': transactions,
            'previous_hash': last_block['hash']
        }

        # Solve the proof-of-work puzzle
        new_block['nonce'] = self.proof_of_work(new_block)

        # Calculate the hash of the new block
        new_block['hash'] = self.calculate_hash(new_block)

        # Add the new block to the blockchain
        self.blockchain.add_block(new_block)

        return new_block

    def proof_of_work(self, block, difficulty=4):
        target = '0' * difficulty
        nonce = 0
        while self.valid_proof(block, nonce, target) is False:
            nonce += 1
        return nonce

    @staticmethod
    def valid_proof(block, nonce, target):
        guess = f'{block}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == target

    @staticmethod
    def calculate_hash(block):
        block_string = f"{block['index']}{block['timestamp']}{block['transactions']}{block['previous_hash']}"
        return hashlib.sha256(block_string.encode()).hexdigest()
