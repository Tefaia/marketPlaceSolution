//index.js
const express = require('express');
const bodyParser = require('body-parser');
const apiRouter = require('./routes/api'); // Adjust the path as needed
const elliptic = require('elliptic');
const Blockchain = require('./Blockchain');
const PeerManager = require('./PeerManager');
const index = express();
const PORT = process.env.PORT || 3001;


function getBlockByIndex(index) {
  if (index >= 0 && index < blockchain.length) {
    return blockchain[index];
  } else {
    return null; // Block not found
  }
}

// Sample data for demonstration purposes
let blockchain = [];
let transactions = [];
let balances = {};
let miningJobs = [];
let peers = [];

// Helper function to retrieve a block by index
function getBlockByIndex(index) {
  return blockchain[index];
}

// Define APIs for various endpoints

// Middleware to parse JSON data in POST requests
index.use(express.json());


// GET /
index.get('/', (req, res) => {
  res.json({ message: 'Hello, world!' });
});

// GET /info
index.get('/info', (req, res) => {
    const info = {
      message: 'Welcome to My Blockchain App',
      version: '1.0.0'
    };
    res.json(info);
  });
  
// GET /debug
index.get('/debug', (req, res) => {
  // Simulate some debug data for demonstration purposes
  const debugData = {
    message: 'Debug information',
    data: {
      foo: 'bar',
      baz: 123,
      debugFlag: true
    }
  };
  
  // Send the debug data as a JSON response
  res.json(debugData);
});

// GET /debug/reset-chain
index.get('/debug/reset-chain', (req, res) => {
  // Reset the blockchain to an empty state (for demonstration purposes)
  blockchain = [];
  transactions = [];
  balances = {};
  miningJobs = [];
  peers = [];
  
  res.json({ message: 'Blockchain reset successfully' });
});

// GET /debug/mine/:minerAddress/:difficulty
index.get('/debug/mine/:minerAddress/:difficulty', (req, res) => {
  const { minerAddress, difficulty } = req.params;

  try {
    // Check if the blockchain is empty
    if (blockchain.length === 0) {
      // Handle the case when the blockchain is empty
      res.status(404).json({ error: 'Blockchain is empty. Mine a genesis block first.' });
      return;
    }

    // Simulate mining logic for demonstration purposes
    const minedBlock = {
      index: blockchain.length,
      timestamp: new Date().getTime(),
      transactions: transactions,
      previousHash: getBlockByIndex(blockchain.length - 1).hash,
      nonce: 0 // Replace with actual mining logic
    };

    // Simulate updating blockchain and related data structures
    blockchain.push(minedBlock);
    transactions = [];
    balances[minerAddress] = (balances[minerAddress] || 0) + 10; // Reward the miner

    res.json({ message: 'Block mined successfully', minedBlock });
  } catch (error) {
    console.error('Error in /debug/mine:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// GET /blocks
index.get('/blocks', (req, res) => {
  // Retrieve the list of blocks from the blockchain
  const blocks = blockchain;

  res.json(blocks);
});

index.get('/blocks/:index', (req, res) => {
  const index = parseInt(req.params.index);

  // Retrieve the block at the specified index from the blockchain
  const block = getBlockByIndex(index);

  if (block) {
    res.json(block);
  } else {
    res.status(404).json({ error: 'Block not found' });
  }
});

// GET /transactions/pending
index.get('/transactions/pending', (req, res) => {
  // Retrieve the list of pending transactions
  const pendingTransactions = transactions;

  res.json(pendingTransactions);
});

// GET /transactions/confirmed
index.get('/transactions/confirmed', (req, res) => {
  // Retrieve the list of confirmed transactions
  const confirmedTransactions = blockchain.reduce((transactions, block) => {
    return transactions.concat(block.transactions);
  }, []);

  res.json(confirmedTransactions);
});

// GET /transactions/:tranHash
index.get('/transactions/:tranHash', (req, res) => {
  const tranHash = req.params.tranHash;

  // Find the transaction with the specified transaction hash
  const transaction = blockchain
    .reduce((transactions, block) => transactions.concat(block.transactions), [])
    .find(tx => tx.hash === tranHash);

  if (transaction) {
    res.json(transaction);
  } else {
    res.status(404).json({ error: 'Transaction not found' });
  }
});

// GET /balances
index.get('/balances', (req, res) => {
  // Retrieve balances for all addresses
  const addressBalances = {};

  for (const address in balances) {
    addressBalances[address] = balances[address];
  }

  res.json(addressBalances);
});

// GET /address/:address/transactions
index.get('/address/:address/transactions', (req, res) => {
  const address = req.params.address;

  // Filter transactions associated with the specified address
  const addressTransactions = blockchain
    .reduce((transactions, block) => transactions.concat(block.transactions), [])
    .filter(tx => tx.from === address || tx.to === address);

  res.json(addressTransactions);
});

// GET /address/:address/balance
index.get('/address/:address/balance', (req, res) => {
  const address = req.params.address;

  // Retrieve the balance for the specified address
  const balance = balances[address] || 0;

  res.json({ address, balance });
});

// POST /transactions
index.post('/transactions', (req, res) => {
  const { from, to, amount } = req.body;

  // Perform validation on the transaction data
  if (!from || !to || !amount) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  // Create a new transaction object
  const newTransaction = {
    from,
    to,
    amount,
    timestamp: new Date().getTime(),
    hash: 'dummyHash' // Generate a hash for the transaction (replace with your hash generation logic)
  };

  // Add the new transaction to the pending transactions array
  transactions.push(newTransaction);

  res.json({ message: 'Transaction submitted successfully', transaction: newTransaction });
});
  
// GET /peers
index.get('/peers', (req, res) => {
  // Retrieve the list of connected peers
  const connectedPeers = peers;

  res.json(connectedPeers);
});

// POST /peers/connect
index.post('/peers/connect', (req, res) => {
  const { peerUrl } = req.body;

  // Perform validation on the peer URL
  if (!peerUrl) {
    return res.status(400).json({ error: 'Missing required field: peerUrl' });
  }

  // Add the new peer URL to the list of connected peers
  peers.push(peerUrl);

  res.json({ message: 'Connected to peer', peerUrl });
});

// POST /peers/notify-new-block
index.post('/peers/notify-new-block', (req, res) => {
  const { block } = req.body;

  // Perform validation on the received block data
  if (!block) {
    return res.status(400).json({ error: 'Missing required field: block' });
  }

  // Notify connected peers about the new block (replace with your actual notification logic)
  // ...

  res.json({ message: 'Notified peers about the new block', block });
});

// GET /mining/get-mining-job/:address
index.get('/mining/get-mining-job/:address', (req, res) => {
  const minerAddress = req.params.address;

  // Create a mining job with required data (replace with your actual mining job generation logic)
  const miningJob = {
    index: blockchain.length,
    transactions: transactions,
    difficulty: 4, // Replace with actual difficulty calculation
    minerAddress: minerAddress
  };

  res.json(miningJob);
});

// POST /mining/submit-mined-block
index.post('/mining/submit-mined-block', (req, res) => {
  const { minedBlock } = req.body;

  // Perform validation on the submitted mined block
  if (!minedBlock) {
    return res.status(400).json({ error: 'Missing required field: minedBlock' });
  }

  // Process the submitted mined block (replace with your actual block validation and processing logic)
  // ...

  res.json({ message: 'Mined block submitted successfully', minedBlock });
});

// POST /transactions/send
index.post('/transactions/send', (req, res) => {
  const { from, to, amount } = req.body;

  // Perform validation on the transaction data
  if (!from || !to || !amount) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  // Check if the sender has sufficient balance
  const senderBalance = balances[from] || 0;
  if (senderBalance < amount) {
    return res.status(400).json({ error: 'Insufficient balance' });
  }

  // Generate a hash for the transaction
  const crypto = require('crypto'); // Import the crypto module
  const transactionData = `${from}-${to}-${amount}-${new Date().getTime()}`;
  const transactionHash = crypto.createHash('sha256').update(transactionData).digest('hex');

   // Create a new transaction object
  const newTransaction = {
    from,
    to,
    amount,
    timestamp: new Date().getTime(),
    hash: transactionHash // Use the generated hash
  };

  // Add the new transaction to the pending transactions array
  transactions.push(newTransaction);

  res.json({ message: 'Transaction submitted successfully', transaction: newTransaction });
});

// Start the server
index.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});