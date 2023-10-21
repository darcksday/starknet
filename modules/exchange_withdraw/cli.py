from termcolor import cprint

from config.settings import CEX_DEFAULT
from helpers.cli import get_amount_in_range


def print_exchange_withdraw_amount():
    try:
        while True:
            cprint("Withdraw ETH amount (number / range):", "yellow")
            return input("> ")
    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit


def print_approve_transaction(amount_str, wallet_list):
    try:
        approx_symbol = ""
        if '-' in amount_str:
            approx_symbol = "~"
            amount = get_amount_in_range(amount_str)
        else:
            amount = float(amount_str)

        cprint(f'{CEX_DEFAULT.upper()} Withdraw {amount_str} ETH using StarkNet chain for {len(wallet_list)} wallets.', 'blue')
        cprint(f'TOTAL: {approx_symbol}{round(len(wallet_list) * amount, 4)} ETH.\n', 'blue')

        approval = input("Do you approve withdraw? (y/N): ")
        if approval.lower() != "y":
            cprint(f'Action Canceled.\n', 'red')
            return False
        return True
    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit
