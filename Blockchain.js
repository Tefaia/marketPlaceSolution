//Blockchain.js
const Block = require('./Block');
const Transaction = require('./Transaction');

class Blockchain {
  constructor() {
    this.chain = [this.createGenesisBlock()];
    this.pendingTransactions = [];
    this.difficulty = 4;
    this.reward = 10;
  }

  createGenesisBlock() {
    return new Block(0, Date.now(), [], '0');
  }

  getLatestBlock() {
    return this.chain[this.chain.length - 1];
  }

  addBlock(block) {
    this.chain.push(block);
  }

  addTransaction(transaction) {
    this.pendingTransactions.push(transaction);
  }

  minePendingTransactions(minerAddress) {
    const rewardTransaction = new Transaction(
      null,
      minerAddress,
      this.reward,
      Date.now()
    );
    this.pendingTransactions.push(rewardTransaction);

    const block = new Block(
      this.chain.length,
      Date.now(),
      this.pendingTransactions,
      this.getLatestBlock().hash
    );
    block.mineBlock(this.difficulty);

    this.addBlock(block);
    this.pendingTransactions = [];
  }

  getBalance(address) {
    let balance = 0;

    for (const block of this.chain) {
      for (const transaction of block.transactions) {
        if (transaction.sender === address) {
          balance -= transaction.amount;
        }
        if (transaction.recipient === address) {
          balance += transaction.amount;
        }
      }
    }

    return balance;
  }

  isValid() {
    for (let i = 1; i < this.chain.length; i++) {
      const currentBlock = this.chain[i];
      const previousBlock = this.chain[i - 1];

      if (currentBlock.hash !== currentBlock.calculateHash()) {
        return false;
      }

      if (currentBlock.previousHash !== previousBlock.hash) {
        return false;
      }
    }

    return true;
  }
}

module.exports = Blockchain;