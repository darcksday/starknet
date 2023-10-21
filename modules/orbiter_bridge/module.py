from helpers.cli import *
from modules.orbiter_bridge.cli import print_input_network
from modules.orbiter_bridge.functions import orbiter_bridge_to_starknet, orbiter_bridge_from_starknet
from helpers.factory import run_script


def interface_orbiter_bridge():
    try:
        while True:
            cprint(f'Orbiter Bridge » Select an action:', 'yellow')
            cprint(f'0. Exit', 'light_grey')
            cprint(f'1. Bridge to StarkNet', 'yellow')
            cprint(f'2. Bridge from StarkNet', 'yellow')
            try:
                option = int(input("> "))
            except ValueError:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

            if option == 0:
                cprint(f'Exit, bye bye.', 'green')
                break

            elif option == 1:
                from_network = print_input_network("From network")
                amount = print_input_amounts_range('Bridge amount')
                run_script(orbiter_bridge_to_starknet, amount, [from_network])
                break

            elif option == 2:
                to_network = print_input_network("To network")
                amount = print_input_amounts_range('Bridge amount')
                run_script(orbiter_bridge_from_starknet, amount, [to_network])
                break

            else:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit
