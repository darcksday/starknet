from termcolor import cprint

from helpers.cli import print_input_contract_address, print_input_amounts_range
from helpers.factory import run_script
from modules.nostra.functions.nostra_deposit import nostra_deposit
from modules.nostra.functions.nostra_route import nostra_route
from modules.nostra.functions.nostra_withdraw import nostra_withdraw


def interface_nostra():
    try:
        while True:
            cprint(f'Nostra » Select an action:', 'yellow')
            cprint(f'0. Exit', 'light_grey')
            cprint(f'1. Deposit token', 'yellow')
            cprint(f'2. Withdraw token', 'yellow')
            cprint(f'3. Deposit and Withdraw ETH', 'yellow')
            try:
                option = int(input("> "))
            except ValueError:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

            if option == 0:
                cprint(f'Exit, bye bye.', 'green')
                break

            elif option == 1:
                token = print_input_contract_address("Deposit token / address or symbol")
                amount_str = print_input_amounts_range('Deposit amount')
                run_script(nostra_deposit, amount_str, [token])
                break

            elif option == 2:
                token = print_input_contract_address("Withdraw token / address or symbol")
                amount_str = print_input_amounts_range('Withdraw amount')
                run_script(nostra_withdraw, amount_str, [token])
                break

            elif option == 3:
                amount_str = print_input_amounts_range('Deposit ETH amount')
                run_script(nostra_route, amount_str, [])
                break

            else:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit
