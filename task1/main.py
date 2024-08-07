import requests
import time
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

PRIVATE_KEY = "ed3056508c7bfa9299cca3ea2f2912ec1ef81c90889603655bd3f04c5c83d154"
WETH = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
WMATIC = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'

RPCETH = 'https://eth.llamarpc.com'
RPCBNB = 'https://bsc-dataseed.bnbchain.org'
RPCMATIC = 'https://polygon.llamarpc.com'

woofiABI = json.load(open('abi/woofi.json'))

def log(message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] {message}")


def swap(src_network, dst_network, src_token, dst_token, src_amount, slippage):
    log("Starting WooSwap")

    rpc = RPCETH
    if src_network == 'ethereum':
        rpc = RPCETH
    if src_network == 'bsc':
        rpc = RPCBNB
    if src_network == 'polygon':
        rpc = RPCMATIC

    url_src_token = src_token
    if src_network == 'ethereum' and src_token.lower() == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
        url_src_token = WETH
    if src_network == 'bsc' and src_token.lower() == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
        url_src_token = WBNB
    if src_network == 'polygon' and src_token.lower() == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
        url_src_token = WMATIC

    #url = f"https://fi-api.woo.org/woofi_swap?from_token=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c&to_token=0x55d398326f99059fF775485246999027B3197955&from_amount=5000000000000000&network=bsc&slippage=1"
    url = f"https://fi-api.woo.org/woofi_swap?from_token={url_src_token}&to_token={dst_token}&from_amount={src_amount}&network={src_network}&slippage={slippage}"


    response = requests.request("GET", url)
    json = response.json()
    print(json['data'])

    #src_token
    #dst_token
    #src_amount
    #to_amount
    #account.address
    #account.address

    to_amount = json['data']['to_amount']

    web3 = Web3(Web3.HTTPProvider(endpoint_uri=rpc))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    web3.eth.account.enable_unaudited_hdwallet_features()

    account = web3.eth.account.from_key(PRIVATE_KEY)
    #account = web3.eth.account.from_mnemonic("friend brain average machine ability orbit general benefit zoo hold old best")
    print("accountAddress", account.address)
    #print("accountPK", Web3.to_hex(account.key))
    #0x3c53ea168c385af2Cba3F2E8942E9EceA25c17f9

    woofi_contract_address = '0x4c4AF8DBc524681930a27b2F1Af5bcC8062E6fB7'
    woofi_contract = web3.eth.contract(address=woofi_contract_address, abi=woofiABI)

    tx_args = woofi_contract.encodeABI(fn_name='swap', args=(src_token, dst_token, int(src_amount), int(to_amount), account.address, account.address))

    print(tx_args)

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
        'value': int(src_amount),
    }
    tx_params['gas'] = int(web3.eth.estimate_gas(tx_params)*1.2)

    sign = web3.eth.account.sign_transaction(tx_params, PRIVATE_KEY)
    tx = web3.eth.send_raw_transaction(sign.rawTransaction)
    tx_data = web3.eth.wait_for_transaction_receipt(tx, timeout=200)
    print(tx_data)

def cross(src_network, dst_network, src_token, dst_token, src_amount, slippage):
    log("Starting CrossSwap")
    url = "https://fi-api.woo.org/v3/cross_chain_swap?src_network=polygon&dst_network=bsc&src_token=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&dst_token=0x55d398326f99059fF775485246999027B3197955&src_amount=4000000000000000000&slippage=1"

    response = requests.request("GET", url)
    print(response.json())

    #refId

    #to = account.address
    #src_infos['from_token']
    #src_infos['bridge_token']
    #src_infos['from_amount']
    #src_infos['min_bridge_amount']

    #dst_infos['chain_id']
    #dst_infos['to_token']
    #dst_infos['bridged_token']
    #dst_infos['min_to_amount']
    #dst_infos['dst_gas_for_call']

    #src_1inch['swap_router']
    #src_1inch['data']

    #dst_1inch['swap_router']
    #dst_1inch['data']


def main():
    src_network = input("Сеть источника: ")
    dst_network = input("Сеть получателя: ")
    src_token = input("Токен источника: ")
    dst_token = input("Токен получателя: ")
    src_amount = input("Количество токенов для свапа: ")
    slippage = input("Проскальзывание: ")

    if src_network == dst_network:
        swap(src_network, dst_network, src_token, dst_token, src_amount, slippage)
    else:
        cross(src_network, dst_network, src_token, dst_token, src_amount, slippage)


if __name__ == "__main__":
    main()
