from termcolor import cprint

from common import TOKEN_ADDRESS
from helpers.cli import print_input_contract_address, print_input_amounts_range
from helpers.factory import run_script
from modules.zklend.functions.zklend_borrow import zklend_borrow_stable
from modules.zklend.functions.zklend_collateral import zklend_collateral_enable, zklend_collateral_disable
from modules.zklend.functions.zklend_deposit import zklend_deposit
from modules.zklend.functions.zklend_repay import zklend_repay_stable
from modules.zklend.functions.zklend_route import zklend_route
from modules.zklend.functions.zklend_withdraw import zklend_withdraw


def interface_zklend():
    try:
        while True:
            cprint(f'ZkLend » Select an action:', 'yellow')
            cprint(f'0. Exit', 'light_grey')
            cprint(f'1. Deposit token', 'yellow')
            cprint(f'2. Withdraw token', 'yellow')
            cprint(f'3. Enable collateral', 'yellow')
            cprint(f'4. Disable collateral', 'yellow')
            cprint(f'5. Borrow stableCoin', 'yellow')
            cprint(f'6. Repay stableCoin', 'yellow')
            cprint(f'7. Route: Deposit ETH > Enable collateral > Borrow random > Repay token > Withdraw ETH', 'yellow')
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
                run_script(zklend_deposit, amount_str, [token])
                break

            elif option == 2:
                token = print_input_contract_address("Withdraw token / address or symbol")
                run_script(zklend_withdraw, "0", [token])
                break

            elif option == 3:
                token = print_input_contract_address("Token / address or symbol")
                run_script(zklend_collateral_enable, "0", [token])
                break

            elif option == 4:
                token = print_input_contract_address("Token / address or symbol")
                run_script(zklend_collateral_disable, "0", [token])
                break

            elif option == 5:
                token = print_input_contract_address("Borrow token / address or symbol")
                amount_str = print_input_amounts_range('Borrow amount (empty for max)')
                run_script(zklend_borrow_stable, amount_str, [token])
                break

            elif option == 6:
                token = print_input_contract_address("Repay token / address or symbol")
                amount_str = print_input_amounts_range('Repay amount')
                run_script(zklend_repay_stable, amount_str, [token])
                break

            elif option == 7:
                amount_str = print_input_amounts_range('Deposit ETH amount')
                run_script(zklend_route, amount_str, [])
                break

            else:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit
