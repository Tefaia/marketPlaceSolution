# transaction_handler.py

class TransactionHandler:
    def __init__(self, wallet, blockchain):
        self.wallet = wallet
        self.blockchain = blockchain

    def create_transaction(self, recipient, amount):
        # Create a new transaction and sign it with the wallet's private key
        transaction = {
            'sender': self.wallet.generate_address(),
            'recipient': recipient,
            'amount': amount,
            'signature': self.wallet.sign_transaction(transaction_data)
        }
        return transaction

    def send_transaction(self, transaction):
        # Validate and add the transaction to the blockchain
        if self.blockchain.validate_transaction(transaction):
            self.blockchain.add_transaction(transaction)
