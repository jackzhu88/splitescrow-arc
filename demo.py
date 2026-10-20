import json,time
from web3 import Web3
from eth_account import Account
w3=Web3(Web3.HTTPProvider("https://rpc.mainnet.arc.io")); cid=5042
acct=Account.from_key(open('wallet.key').read().strip())
d=json.load(open('deployed.mainnet.json')); abi=json.load(open('web/SplitEscrow.json'))['abi']
c=w3.eth.contract(address=d['address'],abi=abi)
JACK=Web3.to_checksum_address("0xe85620ce560cbc634c7c04c33179e2caf052ad35")
def send(fn,value=0):
    gp=max(w3.eth.gas_price,20*10**9)
    tx=fn.build_transaction({'from':acct.address,'value':value,'nonce':w3.eth.get_transaction_count(acct.address),'chainId':cid,'maxFeePerGas':gp*2,'maxPriorityFeePerGas':10**9})
    tx['gas']=int(w3.eth.estimate_gas(tx)*1.3)
    assert tx['gas']*tx['maxFeePerGas']/1e18<0.1
    h=w3.eth.send_raw_transaction(acct.sign_transaction(tx).raw_transaction); r=w3.eth.wait_for_transaction_receipt(h)
    assert r.status==1; return h.hex(), r.gasUsed*r.effectiveGasPrice
dl=int(time.time())+86400
h1,g1=send(c.functions.createDeal([acct.address,JACK],[5000,5000],dl,"SplitEscrow mainnet demo"),value=5*10**16)
id_=c.functions.dealCount().call()-1
h2,g2=send(c.functions.release(id_))
json.dump({"create":h1,"release":h2,"gas_wei":g1+g2,"dealId":id_},open('demo.mainnet.json','w'))
print(json.load(open('demo.mainnet.json')))
