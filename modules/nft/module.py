import random

from termcolor import cprint
from helpers.factory import run_script, run_random_function
from modules.nft.functions.pyramid import nft_pyramid
from modules.nft.functions.starknet_id import nft_starknet_id
from modules.nft.functions.starkverse import nft_starkverse
from modules.nft.functions.unframed import nft_unframed


def interface_nft():
    try:
        while True:
            cprint(f'NFT » Select an action:', 'yellow')
            cprint(f'0. Exit', 'light_grey')
            cprint(f'1. Mint Starknet ID', 'yellow')
            cprint(f'2. Mint StarkVerse NFT', 'yellow')
            cprint(f'3. Mint NFT on Pyramid', 'yellow')
            cprint(f'4. Unframed marketplace call (cheap tx)', 'yellow')
            cprint(f'5. RANDOM: Call random NFT function', 'yellow')
            try:
                option = int(input("> "))
            except ValueError:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

            if option == 0:
                cprint(f'Exit, bye bye.', 'green')
                break

            elif 4 >= option >= 1:
                # chose nft function
                run_script(function_by_index(option), "0", [])
                break

            elif option == 5:
                # chose random nft function
                run_random_function([
                    nft_starknet_id,
                    nft_starkverse,
                    nft_pyramid,
                    nft_unframed
                ])
                break
            else:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit


def function_by_index(index):
    if index == 1:
        return nft_starknet_id
    elif index == 2:
        return nft_starkverse
    elif index == 3:
        return nft_pyramid
    elif index == 4:
        return nft_unframed
    else:
        return None
