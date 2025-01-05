import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        value = str(self.index) + self.previous_hash + str(self.timestamp) + str(self.transactions)
        return hashlib.sha256(value.encode()).hexdigest()

    def __repr__(self):
        return f"Block(index={self.index}, transactions={self.transactions}, hash={self.hash})"

def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block")

def create_new_block(previous_block, transactions):
    index = previous_block.index + 1
    timestamp = time.time()
    return Block(index, previous_block.hash, timestamp, transactions)

class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]
        self.pending_transactions = []

    def add_block(self):
        if len(self.pending_transactions) == 0:
            print("No transactions to add to the block!")
            return
        new_block = create_new_block(self.chain[-1], self.pending_transactions)
        self.chain.append(new_block)
        self.pending_transactions = [] 
    
    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def print_chain(self):
        for block in self.chain:
            print(block)

class User:
    def __init__(self, name, balance=100):
        self.name = name
        self.balance = balance

    def __repr__(self):
        return f"User({self.name}, balance={self.balance})"
    
    def send_coins(self, recipient, amount):
        if self.balance < amount:
            raise ValueError(f"{self.name} does not have enough balance.")
        self.balance -= amount
        recipient.balance += amount
        return f"{self.name} sends {amount} coins to {recipient.name}"

# Simulating a Finney Attack
def finney_attack(blockchain, attacker, recipient, amount):
    print(f"\nInitial balance of {attacker.name}: {attacker.balance} coins")
    print(f"Initial balance of {recipient.name}: {recipient.balance} coins")
    
    # Attacker pre-mines a block with a fake transaction
    print("\n--- Attacker Pre-mining Block ---")
    attacker_transaction = attacker.send_coins(recipient, amount)
    blockchain.add_transaction(attacker_transaction)
    
    print(f"Pending transaction: {blockchain.pending_transactions}")
    # Attacker mines the pre-mined block privately
    attacker_pre_mined_block = create_new_block(blockchain.chain[-1], blockchain.pending_transactions)
    blockchain.pending_transactions = []  # Clear pool after private mining
    
    print(f"Attacker pre-mined block: {attacker_pre_mined_block}")
    
    # Honest miner mines a valid block
    print("\n--- Honest Miners Mining Next Block ---")
    blockchain.add_transaction("Miner sends 5 coins to Recipient")  # Honest miner transaction
    blockchain.add_block()
    print(f"Honest miner's block: {blockchain.chain[-1]}")

    # Attacker reveals pre-mined block
    print("\n--- Attacker Reveals Pre-mined Block ---")
    blockchain.chain.pop()  # Remove honest block
    blockchain.chain.append(attacker_pre_mined_block)  # Add attacker's block
    
    print("\nBlockchain after the Finney attack:")
    blockchain.print_chain()
    
    # Balances after attack
    print(f"\nFinal balance of {attacker.name}: {attacker.balance} coins (unchanged due to the attack)")
    print(f"Final balance of {recipient.name}: {recipient.balance} coins (unchanged because attacker's transaction was never broadcasted)")

def build_blockchain():
    blockchain = Blockchain()
    attacker = User("Attacker", 100)
    recipient = User("Recipient", 0)

    while True:
        print("\nOptions:")
        print("1. Add Transaction")
        print("2. Mine Block")
        print("3. Display Blockchain")
        print("4. Initiate Finney Attack")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            try:
                amount = int(input("Enter amount to send: "))
                transaction = attacker.send_coins(recipient, amount)
                blockchain.add_transaction(transaction)
                print(f"Transaction added: {transaction}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            blockchain.add_block()
            print("Block mined and added to the blockchain.")
        
        elif choice == '3':
            print("\nCurrent Blockchain:")
            blockchain.print_chain()

        elif choice == '4':
            try:
                amount = int(input("Enter the amount of coins for the Finney attack: "))
                finney_attack(blockchain, attacker, recipient, amount)
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '5':
            print("Exiting the blockchain simulator.")
            break
        
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    build_blockchain()
