import hashlib
import time
from datetime import datetime
import json
from colorama import init, Fore, Style

# Initialize colorama to support colored console output (Windows and Unix)
init(autoreset=True)

# -----------------------------------------------------------------------------------
# BlockHeader Class
# -----------------------------------------------------------------------------------

class BlockHeader:
    """
    Contains metadata for each block, similar to headers used in real-world blockchains.
    Stores the block index, timestamp, previous block hash, nonce, difficulty, and hash.
    """
    def __init__(self, index, timestamp, previous_hash, difficulty):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0  # Will be incremented during mining
        self.difficulty = difficulty
        self.hash = None  # Final hash will be computed after mining


# -----------------------------------------------------------------------------------
# Block Class
# -----------------------------------------------------------------------------------

class Block:
    """
    Represents a complete block containing a header and the user-provided data.
    Mining is automatically triggered during initialization.
    """
    def __init__(self, index, data, previous_hash, difficulty):
        timestamp = str(datetime.now())
        self.header = BlockHeader(index, timestamp, previous_hash, difficulty)
        self.data = data
        self.header.hash = self.mine_block()  # Begin mining when block is created

    def calculate_hash(self):
        """
        Generates a SHA-256 hash based on the block's attributes.
        """
        content = (
            f"{self.header.index}{self.header.timestamp}"
            f"{self.data}{self.header.previous_hash}{self.header.nonce}"
        )
        return hashlib.sha256(content.encode()).hexdigest()

    def mine_block(self):
        """
        Proof-of-Work algorithm: iteratively searches for a nonce that produces
        a hash with the required number of leading zeros.
        """
        prefix = '0' * self.header.difficulty
        start_time = time.time()

        while True:
            hash_attempt = self.calculate_hash()
            if hash_attempt.startswith(prefix):
                self.mining_time = round(time.time() - start_time, 4)
                return hash_attempt
            self.header.nonce += 1


# -----------------------------------------------------------------------------------
# Blockchain Class
# -----------------------------------------------------------------------------------

class Blockchain:
    """
    Manages the full blockchain, including:
    - Block creation and mining
    - Chain validation
    - Searching, tampering, and saving the chain
    """
    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]  # Initialize with Genesis Block

    def create_genesis_block(self):
        """
        Creates the first block in the chain, known as the Genesis Block.
        """
        return Block(0, "Genesis Block", "0", self.difficulty)

    def get_latest_block(self):
        """
        Returns the most recent block in the chain.
        """
        return self.chain[-1]

    def add_block(self, data):
        """
        Adds a new block with user-provided data to the blockchain.
        Mining is performed automatically.
        """
        last_block = self.get_latest_block()
        new_block = Block(len(self.chain), data, last_block.header.hash, self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        Validates the blockchain by checking:
        1. If the current block's stored hash matches the recalculated hash.
        2. If the previous_hash value matches the actual hash of the previous block.
        """
        valid = True
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            recalculated_hash = current.calculate_hash()

            if current.header.hash != recalculated_hash:
                print(Fore.RED + f"[Block {i}] Invalid hash! Stored: {current.header.hash}, Calculated: {recalculated_hash}")
                valid = False
            elif current.header.previous_hash != previous.header.hash:
                print(Fore.RED + f"[Block {i}] Invalid previous hash! Stored: {current.header.previous_hash}, Expected: {previous.header.hash}")
                valid = False
            else:
                print(Fore.GREEN + f"[Block {i}] Valid.")

        return valid

    def print_chain(self):
        """
        Prints the contents of the entire blockchain to the console in a readable format.
        """
        for block in self.chain:
            print(Fore.CYAN + "-" * 50)
            print(Fore.YELLOW + "Block Header:")
            print(f"  Index         : {block.header.index}")
            print(f"  Timestamp     : {block.header.timestamp}")
            print(f"  Nonce         : {block.header.nonce}")
            print(f"  Previous Hash : {block.header.previous_hash}")
            print(f"  Hash          : {block.header.hash}")
            print(f"  Difficulty    : {block.header.difficulty}")
            print(Fore.YELLOW + "Block Data:")
            print(f"  Data          : {block.data}")
            print(f"  Mining Time   : {getattr(block, 'mining_time', 'N/A')} seconds")

    def search_block(self, keyword):
        """
        Searches all blocks in the chain for a keyword within the data field.
        """
        found = False
        for block in self.chain:
            if keyword.lower() in str(block.data).lower():
                print(Fore.GREEN + f"Found in Block {block.header.index}: {block.data}")
                found = True
        if not found:
            print(Fore.RED + "Keyword not found.")

    def tamper_block(self, index):
        """
        Manually modifies a block’s data (for demo/testing purposes).
        This simulates tampering and should break chain validity.
        """
        if 0 < index < len(self.chain):
            self.chain[index].data = "Tampered Data"
            print(Fore.RED + f"Block {index} has been tampered.")
        else:
            print(Fore.YELLOW + "Cannot tamper Genesis block or out-of-range index.")

    def save_to_file(self, filename="blockchain.json"):
        """
        Exports the entire blockchain to a local JSON file.
        Useful for analysis, backup, or reloading.
        """
        chain_data = []
        for block in self.chain:
            block_info = {
                "index": block.header.index,
                "timestamp": block.header.timestamp,
                "nonce": block.header.nonce,
                "previous_hash": block.header.previous_hash,
                "hash": block.header.hash,
                "difficulty": block.header.difficulty,
                "data": block.data,
                "mining_time": getattr(block, "mining_time", "N/A")
            }
            chain_data.append(block_info)

        with open(filename, "w") as f:
            json.dump(chain_data, f, indent=4)
        print(Fore.GREEN + f"Blockchain saved to '{filename}'")