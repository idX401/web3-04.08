import json

from web3 import Web3
from web3.middleware import geth_poa_middleware

PRIVATE_KEY = "691b7337ce755a4c1b34d68753889f98519ac051a5ead9c67dfac50c31f03e84"

rpc = 'https://polygon-pokt.nodies.app'

web3 = Web3(Web3.HTTPProvider(endpoint_uri=rpc))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
web3.eth.account.enable_unaudited_hdwallet_features()

account = web3.eth.account.from_key(PRIVATE_KEY)

woofi_contract_address = '0x4c4AF8DBc524681930a27b2F1Af5bcC8062E6fB7'
woofi_contract = web3.eth.contract(address=woofi_contract_address, abi=json.load(open('abi/woofi.json')))

usdt_contract_address = '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'
usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=json.load(open('abi/ERC20.json')))
usdt_decimals = usdt_contract.functions.decimals().call()

matic_address = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

matic_price = 0.699888
usdt_amount = 0.1
matic_decimals = 18

slippage = 0.5
min_to_amount = matic_price * usdt_amount * (1 - slippage / 100)

matic_amount = int(min_to_amount * 10 ** matic_decimals)
usdt_amount = int(usdt_amount * 10 ** usdt_decimals)

tx_args = woofi_contract.encodeABI(fn_name='swap', args=(usdt_contract_address, matic_address, usdt_amount, matic_amount, account.address, account.address))

last_block = web3.eth.get_block('latest')
base_fee = last_block['baseFeePerGas']

tx_params = {
    'chainId': web3.eth.chain_id,
    'maxPriorityFeePerGas': web3.eth.max_priority_fee,
    'maxFeePerGas': base_fee + web3.eth.max_priority_fee,
    'nonce': web3.eth.get_transaction_count(account.address),
    'from': account.address,
    'to': woofi_contract.address,
    'data': tx_args,
    'value': matic_amount,
}
tx_params['gas'] = int(web3.eth.estimate_gas(tx_params)*1.2)



sign = web3.eth.account.sign_transaction(tx_params, PRIVATE_KEY)
tx = web3.eth.send_raw_transaction(sign.rawTransaction)
tx_data = web3.eth.wait_for_transaction_receipt(tx, timeout=200)
print(tx_data)





