import ccxt
import time
import random

API_KEY = 'api_key'  # Enter api_key
SECRET = 'secret'  # Enter secret
PASSPHRASE = 'passphrase'  # Enter passphrase

TOKEN = 'USDC'  # Enter token => 'ETH', 'BNB', 'AVAX', 'USDC', 'USDT', etc.
NETWORK = 'Polygon'  # Enter network => 'Arbitrum one', 'Polygon', 'ERC20', 'zkSync Lite', 'Optimism', 'BSC', 'TRC20', 'Avalanche C-Chain', etc.
AMOUNT = round(random.uniform(1.0, 1.5), 6)  # 10 - min amount, 20 - max amount, 6 - digits after . (eg. 10.647293) => enter your min and max

MIN_DELAY = 20  # Min seconds for delay between withdraws
MAX_DELAY = 50  # Max seconds for delay between withdraws

exchange = ccxt.okx({
        'apiKey': API_KEY,
        'secret': SECRET,
        'password': PASSPHRASE,
        'enableRateLimit': True,
    })


def token_fee(token, network):
    info = exchange.fetch_currencies()
    network_fee = info[token]['networks'][network]['fee']
    return network_fee


def withdraw_info(value, wallet, token, amount, network):
    if value == 'success':
        result = f"**** Succesfull withdrawal {amount} {token} to {wallet} on {network} network ****"
        return result
    elif value == 'error':
        result = f"**** Withdrawal error ****"
        return result


def withdraw(token, network, amount, wallet):
    network_fee = token_fee(token, network)
    try:
        exchange.withdraw(token, amount, wallet, params={
            'toAddress': wallet,
            'chainName': network,
            'dest': 4,
            'fee': network_fee,
            'pwd': '-',
            'amt': amount,
            'network': network
        })

        print(withdraw_info('success', wallet, token, amount, network))
    except Exception:
        print(withdraw_info('error', wallet, token, amount, network))


def main():
    with open('wallets.txt', 'r') as f:
        wallets_list = [row.strip() for row in f]
    for wallet in wallets_list:
        withdraw(TOKEN, NETWORK, AMOUNT, wallet)
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)


if __name__ == '__main__':
    main()
