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


print("Важно: для работы скрипта убедитесь, что баланс токена находится на spot-аккаунте, а не на funding-аккаунте.")
input("Нажмите Enter, чтобы продолжить...")

api_key = input("Введите API-ключ: ")
secret = input("Введите секретный ключ: ")
passphrase = input("Введите кодовую фразу: ")

symbol = input("Введите название токена: ")

exchange = ccxt.okx({
    'apiKey': api_key,
    'secret': secret,
    'password': passphrase,
    'enableRateLimit': True,
})

info = exchange.fetch_currencies()
available_networks = info[symbol]['networks'].keys()
print(f"Доступные сети для {symbol}: {', '.join(available_networks)}")
selected_network = input("Введите выбранную сеть: ")
chainName = info[symbol]['networks'][selected_network]['id']
network_fee = info[symbol]['networks'][selected_network]['fee']

wallets_input = input(
    "Введите список кошельков и суммы вывода через запятую (например, кошелек1:сумма1,кошелек2:сумма2): ")
wallets = [tuple(wallet.split(':')) for wallet in wallets_input.split(',')]

min_delay = float(input("Введите минимальную задержку между выводами (в секундах): "))
max_delay = float(input("Введите максимальную задержку между выводами (в секундах): "))

balance = get_balance(exchange, symbol)

if balance is None:
    print(
        "Такого токена у вас на балансе не найдено. Убедитесь, что вы верно ввели название токена и что баланс токена на спот-аккаунте.")
    symbol = input("Введите название токена еще раз: ")
    balance = get_balance(exchange, symbol)
else:
    for wallet, amount_str in wallets:
        amount = float(amount_str)
        balance = get_balance(exchange, symbol)
        withdrawable_amount = calculate_withdrawable_amount(amount, network_fee, balance)

        if withdrawable_amount != amount:
            print(f"Недостаточно средств для вывода {amount} {symbol} на адрес {wallet}.")
            print(f"Максимально возможная сумма к выводу: {withdrawable_amount} {symbol}.")
            while True:
                user_choice = input("Введите новую сумму для вывода или 'yes' для вывода предложенной суммы: ").lower()
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
                            f"Введенная сумма все еще превышает доступный баланс."
                            f" Максимально возможная сумма к выводу: {withdrawable_amount} {symbol}.")

        print(f"Вывод {amount} {symbol} на адрес {wallet}")

        try:
            result = exchange.withdraw(symbol, amount, wallet, params={'toAddress': wallet, 'chainName': chainName, 'dest': 4, 'fee': network_fee, 'pwd': '-', 'amt': str(amount)})
            print("Вывод успешно выполнен")
            print(result)
        except Exception as e:
            print("Ошибка при выводе")
            print(e)

        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

