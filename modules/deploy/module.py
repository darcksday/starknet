from termcolor import cprint

from helpers.factory import run_script
from modules.deploy.functions import deploy_token, deploy_nft


def interface_deploy():
    try:
        while True:
            cprint(f'Deploy smart-contract » Select an action:', 'yellow')
            cprint(f'0. Exit', 'light_grey')
            cprint(f'1. Deploy Token', 'yellow')
            cprint(f'2. Deploy NFT', 'yellow')
            try:
                option = int(input("> "))
            except ValueError:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

            if option == 0:
                cprint(f'Exit, bye bye.', 'green')
                break

            elif option == 1:
                run_script(deploy_token, "0", [])
                break

            elif option == 2:
                run_script(deploy_nft, "0", [])
                break

            else:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit