import os
from dotenv import load_dotenv
from web3 import Web3, HTTPProvider, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware
import json
from eth_account import Account

load_dotenv()

# Get the private key from environment variables
private_key = os.getenv('PRIVATE_KEY')

# Connect to Ethereum node
web3 = Web3(HTTPProvider(os.getenv('SEPOLIA_RPC_URL')))

# Ensure you're connected to Ethereum
assert web3.is_connected()

with open("Token_bytecode.txt", "r") as file:
    contract_bytecode = file.read().strip()

with open("Token.json", "r") as file:
    contract_abi = json.load(file)

# Create a contract factory
Token = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

account = Account.from_key(private_key)
nonce = web3.eth.get_transaction_count(account.address)
chain_id = 11155111 # Change according to your network
gas_price = web3.eth.gas_price

initial_supply = 1000000

# This is a sample constructor argument. Replace/append according to your contract's constructor
transaction = {
    'from': account.address,
    'nonce': nonce,
    'gas': 2000000,
    'gasPrice': gas_price,
    'data': Token.constructor(initial_supply).data_in_transaction,
    'chainId': chain_id
}

signed_tx = account.sign_transaction(transaction)
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(tx_hash.hex())  # This prints the transaction hash

tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print("Deployed at:", tx_receipt['contractAddress'])  # This prints the contract address
