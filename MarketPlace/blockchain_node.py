#blockchain_node.py
from flask import Flask, jsonify, request
import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

app = Flask(__name__)

class BlockchainNode:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()

        # Create the genesis block
        self.create_block(previous_hash='1', proof=100)

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        self.transactions = []  # Reset the transactions list
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while not self.valid_proof(new_proof, previous_proof):
            new_proof += 1
        return new_proof

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def valid_proof(self, new_proof, previous_proof):
        guess = f'{new_proof}{previous_proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def valid_transaction(self, transaction):
        required_fields = ['sender', 'recipient', 'amount']
        return all(field in transaction for field in required_fields)

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block['transactions']:
                if tx['sender'] == address:
                    balance -= tx['amount']
                elif tx['recipient'] == address:
                    balance += tx['amount']
        return balance

    def new_transaction(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.get_previous_block()['index'] + 1

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        previous_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block['previous_hash'] != self.hash(previous_block):
                return False

            if not self.valid_proof(block['proof'], previous_block['proof']):
                return False

            previous_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        neighbors = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json().get('length', 0)
                chain = response.json().get('chain', [])

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def send_funds(self, sender, recipient, amount):
        # Create a new transaction
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.transactions.append(transaction)

        # Add the transaction to the latest block
        latest_block = self.get_previous_block()
        latest_block['transactions'].append(transaction)

        return f"Funds sent successfully from {sender} to {recipient} ({amount} coins)"

# Instantiate the BlockchainNode
blockchain_node = BlockchainNode()

# Define API endpoints for the blockchain node
@app.route('/')
def home():
    return 'Welcome to the Blockchain Node!'

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain_node.get_previous_block()
    last_proof = last_block['proof']
    proof = blockchain_node.proof_of_work(last_proof)

    # Reward the miner for mining
    blockchain_node.new_transaction(sender="0", recipient="Your Miner Address", amount=1)

    previous_hash = blockchain_node.hash(last_block)
    block = blockchain_node.create_block(proof, previous_hash)

    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required_fields = ['sender', 'recipient', 'amount']
    if not all(field in values for field in required_fields):
        return jsonify({'message': 'Missing fields'}), 400

    index = blockchain_node.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain_node.chain,
        'length': len(blockchain_node.chain)
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return jsonify({'message': 'Error: Please supply a valid list of nodes'}), 400

    for node in nodes:
        blockchain_node.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain_node.nodes)
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain_node.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain_node.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain_node.chain
        }

    return jsonify(response), 200

# Add this route handler for checking transactions
@app.route('/transactions', methods=['GET'])
def get_transactions():
    response = {
        'transactions': blockchain_node.transactions,
        'length': len(blockchain_node.transactions)
    }
    return jsonify(response), 200

# Add the /faucet endpoint
@app.route('/faucet', methods=['POST'])
def faucet():
    values = request.get_json()

    required_fields = ['address', 'amount']
    if not all(field in values for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400

    # Simulate sending funds by creating a transaction on the blockchain
    sender_address = "Faucet"
    recipient_address = values['address']
    amount = values['amount']
    result = blockchain_node.send_funds(sender_address, recipient_address, amount)

    response = {'message': result}
    return jsonify(response), 200

# Run the blockchain node
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
