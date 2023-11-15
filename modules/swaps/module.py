from termcolor import cprint

from helpers.cli import print_input_amounts_range, print_input_contract_address
from helpers.factory import run_script, run_random_swap
from modules.swaps.functions.avnu import swap_token_avnu
from modules.swaps.functions.jediswap import swap_token_jediswap
from modules.swaps.functions.myswap import swap_token_myswap
from modules.swaps.functions.open_ocean import swap_token_open_ocean
from modules.swaps.functions.protoss import swap_token_protoss
from modules.swaps.functions.sithswap import swap_token_sithswap
from modules.swaps.functions.tenk_swap import swap_token_10kswap
from modules.swaps.swap_routes import SWAP_ROUTES


def interface_swaps():
    try:
        while True:
            cprint(f'Swaps » Select an action:', 'yellow')
            cprint(f'0. Exit', 'light_grey')
            cprint(f'1. AVNU', 'yellow')
            cprint(f'2. JediSwap', 'yellow')
            cprint(f'3. 10kSwap', 'yellow')
            cprint(f'4. MySwap', 'yellow')
            cprint(f'5. SithSwap', 'yellow')
            cprint(f'6. Protoss', 'yellow')
            cprint(f'7. OpenOcean', 'yellow')
            cprint(f'8. Random Swap: ETH > Random Token > ETH / Random Dex', 'yellow')
            try:
                option = int(input("> "))
            except ValueError:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

            if option == 0:
                cprint(f'Exit, bye bye.', 'green')
                break

            elif 7 >= option >= 1:
                from_token = print_input_contract_address("From token / address or symbol")
                to_token = print_input_contract_address("To token / address or symbol")
                amount_str = print_input_amounts_range('Swap amount')
                params = [from_token, to_token]

                # chose swap function
                run_script(function_by_index(option), amount_str, params)
                break

            elif option == 8:
                # chose random swap function
                amount_str = print_input_amounts_range('Swap ETH amount')
                run_random_swap(SWAP_ROUTES, amount_str)
                break

            else:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit


def function_by_index(index):
    if index == 1:
        return swap_token_avnu
    elif index == 2:
        return swap_token_jediswap
    elif index == 3:
        return swap_token_10kswap
    elif index == 4:
        return swap_token_myswap
    elif index == 5:
        return swap_token_sithswap
    elif index == 6:
        return swap_token_protoss
    elif index == 7:
        return swap_token_open_ocean
    else:
        return None
