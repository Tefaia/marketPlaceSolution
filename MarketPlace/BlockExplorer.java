//BlockExplorer.java
import java.util.ArrayList;
import java.util.List;

public class BlockExplorer {

    public static void main(String[] args) {   
        System.out.println("Hello, Block Explorer!");

        // Create a sample blockchain with dummy data
        List<Block> blockchain = new ArrayList<>();
        blockchain.add(new Block("0", "Genesis Block", "0", List.of("Genesis Transaction")));
        blockchain.add(new Block("1", "Block 1", blockchain.get(0).getHash(), List.of("Transaction 1")));
        blockchain.add(new Block("2", "Block 2", blockchain.get(1).getHash(), List.of("Transaction 2", "Transaction 3")));

        // Display information about the entire blockchain
        System.out.println("Blockchain Explorer");
        for (Block block : blockchain) {
            System.out.println("Block Hash: " + block.getHash());
            System.out.println("Previous Hash: " + block.getPreviousHash());
            System.out.println("Timestamp: " + block.getTimestamp());
            System.out.println("Transactions: " + block.getTransactions());
            System.out.println("---------------------------");
        }

        // Find and display details of a specific block by its hash
        String targetHash = "2"; // Replace with the hash of the block you want to find
        Block targetBlock = findBlockByHash(blockchain, targetHash);
        if (targetBlock != null) {
            System.out.println("Block found:");
            System.out.println("Block Hash: " + targetBlock.getHash());
            System.out.println("Previous Hash: " + targetBlock.getPreviousHash());
            System.out.println("Timestamp: " + targetBlock.getTimestamp());
            System.out.println("Transactions: " + targetBlock.getTransactions());
        } else {
            System.out.println("Block not found with the given hash.");
        }
    }

    // Method to find a block by its hash
    public static Block findBlockByHash(List<Block> blockchain, String hash) {
        for (Block block : blockchain) {
            if (block.getHash().equals(hash)) {
                return block;
            }
        }
        return null;
    }
}

class Block {
    private String hash;
    private String data;
    private String previousHash;
    private List<String> transactions;
    private long timestamp;

    public Block(String hash, String data, String previousHash, List<String> transactions) {
        this.hash = hash;
        this.data = data;
        this.previousHash = previousHash;
        this.transactions = transactions;
        this.timestamp = System.currentTimeMillis();
    }

    public String getHash() {
        return hash;
    }

    public String getPreviousHash() {
        return previousHash;
    }

    public List<String> getTransactions() {
        return transactions;
    }

    public long getTimestamp() {
        return timestamp;
    }
}
