"""Deploy SplitEscrow. Usage: python deploy.py testnet|mainnet  (key read from wallet.key, never printed)"""
import sys, json
from web3 import Web3
from eth_account import Account
NET={"testnet":("https://rpc.testnet.arc.io",5042002),"mainnet":("https://rpc.mainnet.arc.io",5042)}
rpc,cid=NET[sys.argv[1]]
w3=Web3(Web3.HTTPProvider(rpc)); acct=Account.from_key(open('wallet.key').read().strip())
art=json.load(open('web/SplitEscrow.json'))
C=w3.eth.contract(abi=art['abi'],bytecode=art['bytecode'])
gp=max(w3.eth.gas_price,20*10**9)
tx=C.constructor().build_transaction({'from':acct.address,'nonce':w3.eth.get_transaction_count(acct.address),'chainId':cid,'maxFeePerGas':gp*2,'maxPriorityFeePerGas':10**9})
tx['gas']=int(w3.eth.estimate_gas(tx)*1.2)
cost=tx['gas']*tx['maxFeePerGas']/1e18
print("max cost (USDC):",cost); assert cost<0.5, "over cap"
h=w3.eth.send_raw_transaction(acct.sign_transaction(tx).raw_transaction)
r=w3.eth.wait_for_transaction_receipt(h)
print("contract",r.contractAddress,"tx",h.hex())
json.dump({"network":sys.argv[1],"address":r.contractAddress,"tx":h.hex()},open(f'deployed.{sys.argv[1]}.json','w'))
