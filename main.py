from config.settings import ETH_VOLUME_AMOUNT_PER_ACC, VOLUME_SWAP_REPEATS
from helpers.cli import *
from config.routes import USE_MULTIPLE_FUNCTIONS
from helpers.factory import run_script, run_multiple, run_one_of_multiple
from modules.activate_new.module import interface_deploy_argent_wallet
from modules.balance.module import interface_check_balance
from modules.dmail.module import dmail_send_email
from modules.exchange_withdraw.module import interface_exchange_withdraw
from modules.nft.module import interface_nft
from modules.nostra.module import interface_nostra
from modules.orbiter_bridge.module import interface_orbiter_bridge
from modules.swaps.module import interface_swaps
from modules.exchange_deposit.module import interface_transfer_to_exchange
from modules.tx_count.module import interface_tx_count
from modules.unused_contracts.module import interface_unused_contracts
from modules.volume.module import run_volume_wallet_by_wallet
from modules.zklend.module import interface_zklend

if __name__ == '__main__':
    try:
        if VOLUME_SWAP_REPEATS[0] == VOLUME_SWAP_REPEATS[1]:
            swaps_count = VOLUME_SWAP_REPEATS[0]
        else:
            swaps_count = '-'.join(map(str, VOLUME_SWAP_REPEATS))

        while True:
            cprint(f'Select an action:', 'yellow')
            cprint(f'0. Exit', 'light_grey')
            cprint(f'1. Check balances', 'yellow')
            cprint(f'2. Check transactions count', 'yellow')
            cprint(f'3. Exchange withdraw', 'yellow')
            cprint(f'4. Transfer to exchange', 'yellow')
            cprint(f'5. Orbiter bridge', 'yellow')
            cprint(f'6. Dmail: send email', 'yellow')
            cprint(f'7. Swaps: JediSwap/MySwap/10kSwap...', 'yellow')
            cprint(f'8. NFT: StarknetId/Starkverse/Pyramid...', 'yellow')
            cprint(f'9. ZkLend: supply/withdraw/borrow/repay...', 'yellow')
            cprint(f'10. Nostra: deposit/withdraw', 'yellow')
            cprint(f'11. Run one random function from routing (use config/routes.py)', 'yellow')
            cprint(f'12. Run all functions from routing randomly (use config/routes.py)', 'yellow')
            cprint(
                f'13. Volume ({ETH_VOLUME_AMOUNT_PER_ACC} ETH): wallet by wallet / OKX > ZkLend > AVNU/SithSwap/OpenOcean ({swaps_count} swaps) > ZkLend > OKX',
                'yellow'
            )
            cprint(f'14. Find and run unused contract for wallet', 'yellow')
            cprint(f'15. Deploy new argent wallets', 'yellow')

            try:
                option = int(input("> "))
            except ValueError:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

            if option == 0:
                cprint(f'Exit, bye bye.', 'green')
                break

            elif option == 1:
                interface_check_balance()
                break

            elif option == 2:
                interface_tx_count()
                break

            elif option == 3:
                interface_exchange_withdraw()
                break

            elif option == 4:
                interface_transfer_to_exchange()
                break

            elif option == 5:
                interface_orbiter_bridge()
                break

            elif option == 6:
                run_script(dmail_send_email, "0", [])
                break

            elif option == 7:
                interface_swaps()
                break

            elif option == 8:
                interface_nft()
                break

            elif option == 9:
                interface_zklend()
                break

            elif option == 10:
                interface_nostra()
                break

            elif option == 11:
                run_one_of_multiple(USE_MULTIPLE_FUNCTIONS)
                break

            elif option == 12:
                run_multiple(USE_MULTIPLE_FUNCTIONS)
                break

            elif option == 13:
                run_volume_wallet_by_wallet()
                break

            elif option == 14:
                interface_unused_contracts()
                break

            elif option == 15:
                interface_deploy_argent_wallet()
                break

            else:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit
