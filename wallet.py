# Import dependencies
import subprocess
import json
from dotenv import load_dotenv

# Load and set environment variables
import os
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
# YOUR CODE HERE
from constants import BTC, BTCTEST, ETH
from bit import wif_to_key
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from pathlib import Path
from getpass import getpass
 
 #connect Web3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

#enable PoA Middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Create a function called `derive_wallets`
def derive_wallets(mnemonic, coin, numderive):
    command = './derive -g --mnemonic="banner loan bitter involve diary blood snow stomach repeat cover cause fan attitude repeat lucky" --numderive="{numderive}" --cols=path,address,privkey,pubkey --coin="{coin}" --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {"eth", "btc-test", "btc"}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    # YOUR CODE HERE
    print(coin)
    print(priv_key)
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount):
    if coin == ETH:
        #estimate the gas cost
        gasEstimate = w3.eth.estimateGas({"from": account.address, 
                                        "to": recipient, 
                                        "value": amount
                                        })
        # return the raw transaction object
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        }

    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address,[(recipient, amount, BTC)])

eth_acc = priv_key_to_account(ETH, derive_wallets(mnemonic, ETH,5)[0]['privkey'])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    #create a raw transaction
    tx = create_tx(coin, account, recipient, amount)
    
    if coint ==ETH:
        #sign the transaction
        signed_tx = account.sign_transaction(tx)
        
        #send the transaction
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        #display the result hash (transaction verification)
        print(result.hex())
    
        #return the result hash
        return  result.hex()
    elif coin==BTCTEST:
        tx_btctest = create_tx(coin, account, recipient, amount)
        signed_txn = account.sign_transaction(txn)
        print(signed_txn)
        return NetworkAPI.broadcast_tx_testnet(signed)