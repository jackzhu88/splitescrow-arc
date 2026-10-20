import json, solcx
from web3 import Web3, EthereumTesterProvider
src=open('contracts/SplitEscrow.sol').read()
out=solcx.compile_standard({"language":"Solidity","sources":{"SplitEscrow.sol":{"content":src}},
 "settings":{"optimizer":{"enabled":True,"runs":200},"evmVersion":"paris","outputSelection":{"*":{"*":["abi","evm.bytecode.object"]}}}},solc_version='0.8.24')
c=out['contracts']['SplitEscrow.sol']['SplitEscrow']
json.dump({"abi":c['abi'],"bytecode":c['evm']['bytecode']['object']},open('web/SplitEscrow.json','w'))
w3=Web3(EthereumTesterProvider()); a=w3.eth.accounts
C=w3.eth.contract(abi=c['abi'],bytecode=c['evm']['bytecode']['object'])
h=C.constructor().transact({'from':a[0]}); addr=w3.eth.get_transaction_receipt(h).contractAddress
e=w3.eth.contract(address=addr,abi=c['abi'])
now=w3.eth.get_block('latest').timestamp
b1,b2=w3.eth.get_balance(a[1]),w3.eth.get_balance(a[2])
e.functions.createDeal([a[1],a[2]],[7000,3000],now+3600,"dinner").transact({'from':a[0],'value':10**18})
try: e.functions.release(0).transact({'from':a[1]}); raise SystemExit("FAIL non-payer")
except Exception as x: pass
try: e.functions.refund(0).transact({'from':a[0]}); raise SystemExit("FAIL early refund")
except Exception: pass
e.functions.release(0).transact({'from':a[0]})
assert w3.eth.get_balance(a[1])-b1==7*10**17 and w3.eth.get_balance(a[2])-b2==3*10**17
e.functions.createDeal([a[1]],[10000],now+10,"x").transact({'from':a[0],'value':5})
w3.provider.ethereum_tester.time_travel(now+100); w3.provider.ethereum_tester.mine_blocks(1)
e.functions.refund(1).transact({'from':a[0]})
assert e.functions.getDeal(1).call()[3]
print("all tests passed")
