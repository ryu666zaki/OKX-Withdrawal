import ccxt
import time
import random


def get_balance(exchange, symbol):
    try:
        balance = exchange.fetch_balance()
        return balance['total'][symbol.upper()]
    except KeyError:
        return None


def calculate_withdrawable_amount(amount, fee, balance):
    total_withdraw = amount + fee
    if balance < total_withdraw:
        return round((balance - fee) / 10) * 10, 7
    return round(amount, 7)


print("Important: for the script to work, make sure that the balance of the token is on the trading account")
input("Press Enter to continue...")

api_key = input("Enter Api-key: ")
secret = input("Enter Secret: ")
passphrase = input("Enter Passphrase: ")

symbol = input("Token to Withdraw: ")

exchange = ccxt.okx({
    'apiKey': api_key,
    'secret': secret,
    'password': passphrase,
    'enableRateLimit': True,
})

info = exchange.fetch_currencies()
available_networks = info[symbol]['networks'].keys()
print(f"Available networks for {symbol}: {', '.join(available_networks)}")
selected_network = input("Choose network: ")
chainName = info[symbol]['networks'][selected_network]['id']
network_fee = info[symbol]['networks'][selected_network]['fee']

wallets_input = input(
    "Enter addresses and amounts (e.g wallet1:amount1,wallet2:amount2, ...): ")
wallets = [tuple(wallet.split(':')) for wallet in wallets_input.split(',')]

min_delay = float(input("Min delay (seconds): "))
max_delay = float(input("Max delay (seconds): "))

balance = get_balance(exchange, symbol)

if balance is None:
    print(
        "No such token was found on your balance. Make sure you entered the correct name of the token and that the balance of the token is on the trading-account.")
    symbol = input("Enter token to withdraw again: ")
    balance = get_balance(exchange, symbol)
else:
    for wallet, amount_str in wallets:
        amount = float(amount_str)
        balance = get_balance(exchange, symbol)
        withdrawable_amount = calculate_withdrawable_amount(amount, network_fee, balance)

        if withdrawable_amount != amount:
            print(f"Insufficient funds to withdraw {amount} {symbol} to address {wallet}.")
            print(f"Max amount to withdraw : {withdrawable_amount} {symbol}.")
            while True:
                user_choice = input("Enter a new amount to withdraw or 'yes' to withdraw the proposed max amount: ").lower()
                if user_choice == 'yes':
                    amount = withdrawable_amount
                    break
                else:
                    new_amount = float(user_choice)
                    if new_amount <= withdrawable_amount:
                        amount = new_amount
                        break
                    else:
                        print(
                            f" The entered amount still exceeds the available balance."
                            f" Max amount to withdraw : {withdrawable_amount} {symbol}.")

        print(f"Withdraw {amount} {symbol} to wallet {wallet}")

        try:
            result = exchange.withdraw(symbol, amount, wallet, params={'toAddress': wallet, 'chainName': chainName, 'dest': 4, 'fee': network_fee, 'pwd': '-', 'amt': str(amount)})
            print("Successful withdrawal")
            print(result)
        except Exception as e:
            print("Withdraw error")
            print(e)

        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

