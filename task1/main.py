import requests
import time
import json
from web3 import Web3

PRIVATE_KEY = "691b7337ce755a4c1b34d68753889f98519ac051a5ead9c67dfac50c31f03e84"
WETH = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
WMATIC = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'

web3 = Web3(Web3.HTTPProvider(endpoint_uri=rpc))
web3.eth.account.enable_unaudited_hdwallet_features()

account = web3.eth.account.from_key(PRIVATE_KEY)



def log(message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] {message}")


def swap(src_network, dst_network, src_token, dst_token, src_amount, slippage):
    log("Starting WooSwap")
    url_src_token = src_token
    if src_network == 'ethereum' and src_token.lower() == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
        url_src_token = WETH
    if src_network == 'bsc' and src_token.lower() == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
        url_src_token = WBNB
    if src_network == 'polygon' and src_token.lower() == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
        url_src_token = WMATIC

    url = "https://fi-api.woo.org/woofi_swap?from_token=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c&to_token=0x55d398326f99059fF775485246999027B3197955&from_amount=5000000000000000&network=bsc&slippage=1"

    response = requests.request("GET", url)
    print(response.json())

    #src_token
    #dst_network
    #src_amount
    #to_amount
    #account.address
    #account.address


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


def test():

def main():
    test()
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
