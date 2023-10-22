import random
import time

from loguru import logger
from common import TOKEN_ADDRESS
from config.routes import USE_MULTIPLE_FUNCTIONS
from config.settings import *
from helpers.cli import sleeping
from helpers.factory import run_script_one, run_multiple
from helpers.starknet import Starknet
from modules.exchange_withdraw.config import CEX_KEYS
from modules.exchange_withdraw.functions import call_exchange_withdraw
from modules.exchange_deposit.functions import transfer_eth
from modules.swaps.functions.avnu import swap_token_avnu
from modules.swaps.functions.sithswap import swap_token_sithswap
from modules.volume.helpers import check_wait_wallet_balance, get_okx_token_balance, get_okx_account
from modules.zklend.functions.zklend_borrow import zklend_borrow_stable, get_max_borrow_amount
from modules.zklend.functions.zklend_collateral import zklend_collateral_enable
from modules.zklend.functions.zklend_deposit import zklend_deposit
from modules.zklend.functions.zklend_repay import zklend_repay_stable
from modules.zklend.functions.zklend_withdraw import zklend_withdraw


def run_one_wallet_volume(wallet, recipient, cex_network):
    csv_name = f'volume_report'
    account = Starknet(wallet['index'], wallet)

    logger.info(f"[{account._id}][{account.address_original}]: Run TX Volume")

    rand_pct = ETH_VOLUME_AMOUNT_PER_ACC * 0.03
    amount = round(ETH_VOLUME_AMOUNT_PER_ACC - random.uniform(0, rand_pct), 4)
    logger.info(f'Amount: {amount} ETH')

    # ------------------ Withdraw ETH ------------------

    call_exchange_withdraw(account.address_original, cex_network, round(amount + 0.0001, 4), 'ETH', 'okx')
    sleeping(MIN_SLEEP, MAX_SLEEP)

    # --------------- Check wallet balance ---------------

    check_wait_wallet_balance(account, amount, 'ETH')
    sleeping(MIN_SLEEP, MAX_SLEEP)

    # --------- zkLend - supply ETH, borrow USDC ----------

    # Enable ETH collateral
    run_script_one(account, zklend_collateral_enable, "", [TOKEN_ADDRESS['ETH']], csv_name)
    sleeping(int(MIN_SLEEP / 2), int(MAX_SLEEP / 2))

    zeth_amount = amount * 0.99

    # Deposit ETH
    run_script_one(account, zklend_deposit, str(zeth_amount), [TOKEN_ADDRESS['ETH']], csv_name)
    sleeping(MIN_SLEEP, MAX_SLEEP)

    # Borrow USDC
    max_borrow_usdc = get_max_borrow_amount(account, 'USDC')
    run_script_one(account, zklend_borrow_stable, "0", [TOKEN_ADDRESS['USDC']], csv_name)

    check_wait_wallet_balance(account, max_borrow_usdc * 0.99, 'USDC', TOKEN_ADDRESS['USDC'])
    sleeping(MIN_SLEEP, MAX_SLEEP)

    # ---------------- Swap USDC/USDT ----------------

    swap_repeats = VOLUME_SWAP_REPEATS
    if type(swap_repeats) is list:
        swap_repeats = random.randint(swap_repeats[0], swap_repeats[1])

    for step in range(swap_repeats):
        # 50% chance to run random function before each step
        rand_chance = random.randint(0, 1)
        # if rand_chance == 1:
        #     logger.info(
        #         f"[{account._id}][{account.address_original}] Random function before step #{step + 1}"
        #     )
        #     selected_random_function = random.choice(USE_MULTIPLE_FUNCTIONS)
        #     if selected_random_function:
        #         run_script_one(account, selected_random_function, "0", [], csv_name)
        #         sleeping(int(MIN_SLEEP / 2), MAX_SLEEP * 2)
        #     else:
        #         logger.info(f"[{account._id}][{account.address_original}] No random functions available in 'config/routes.py'")

        logger.info(
            f"[{account._id}][{account.address_original}] swap USDC > USDT (step {step + 1}/{swap_repeats})"
        )

        swap_function = random.choice([swap_token_avnu, swap_token_sithswap, swap_token_avnu])
        run_script_one(account, swap_function, "0", [TOKEN_ADDRESS['USDC'], TOKEN_ADDRESS['USDT']], csv_name)

        check_wait_wallet_balance(account, max_borrow_usdc * 0.99, 'USDT', TOKEN_ADDRESS['USDT'])
        sleeping(MIN_SLEEP, MAX_SLEEP)

        logger.info(
            f"[{account._id}][{account.address_original}] swap USDT > USDC (step {step + 1}/{swap_repeats})"
        )
        swap_function = random.choice([swap_token_avnu, swap_token_sithswap, swap_token_avnu])
        run_script_one(account, swap_function, "0", [TOKEN_ADDRESS['USDT'], TOKEN_ADDRESS['USDC']], csv_name)

        check_wait_wallet_balance(account, max_borrow_usdc * 0.99, 'USDC', TOKEN_ADDRESS['USDC'])
        sleeping(MIN_SLEEP, MAX_SLEEP)

    # ------------- zkLend - repay USDC ---------------

    balance_before_repay = account.get_balance(TOKEN_ADDRESS['USDC'])['balance']
    run_script_one(account, zklend_repay_stable, "0", [TOKEN_ADDRESS['USDC']], csv_name)
    sleeping(MIN_SLEEP, MAX_SLEEP)

    while True:
        balance = account.get_balance(TOKEN_ADDRESS['USDC'])['balance']
        if balance < balance_before_repay:
            break
        time.sleep(5)
        continue

    # -------------- zkLend - withdraw ETH ----------------

    run_script_one(account, zklend_withdraw, "0", [TOKEN_ADDRESS['ETH']], csv_name)
    check_wait_wallet_balance(account, amount, 'ETH')
    sleeping(MIN_SLEEP, MAX_SLEEP)

    # ---------------- Withdraw ETH to OKX ----------------

    amount_to_withdraw = round(amount - ETH_VOLUME_LEFT_ON_WALLET, 4)
    transfer_eth(account, recipient, amount_to_withdraw)
    sleeping(MIN_SLEEP, MAX_SLEEP)

    # ---------------- Check OKX balance ----------------

    while True:
        logger.info(f"[{account._id}] Check OKX main account balance")
        main_acc_balance = get_okx_token_balance(0)

        if main_acc_balance >= amount_to_withdraw:
            logger.success(f"[{account._id}] {main_acc_balance} ETH found")
            break
        else:
            for sub_account_num in range(1, 6):
                if is_okx_sub_account(sub_account_num):
                    logger.info(f"[{account._id}] Check OKX subAccount {get_okx_sub_account_name(sub_account_num)}")
                    acc_balance = get_okx_token_balance(sub_account_num)

                    if acc_balance >= amount_to_withdraw:
                        logger.success(f"[{account._id}] {acc_balance} ETH found, transfer to OKX main account")
                        okx_account = get_okx_account()
                        okx_account.transfer("ETH", acc_balance, get_okx_sub_account_name(sub_account_num), 'master')
                        time.sleep(3)
                        break
                    elif acc_balance > 0:
                        logger.info(f"[{account._id}] Only {acc_balance} ETH found, waiting {amount_to_withdraw} ETH...")

        sleeping(MIN_SLEEP, MAX_SLEEP)
        continue


def is_okx_sub_account(num):
    return len(CEX_KEYS[f'okx-sub-{num}']['api_key']) > 0


def get_okx_sub_account_name(num):
    return CEX_KEYS[f'okx-sub-{num}']['name']
