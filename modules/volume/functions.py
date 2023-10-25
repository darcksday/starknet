import random
import time

from loguru import logger
from common import TOKEN_ADDRESS
from config.settings import *
from helpers.cli import sleeping
from helpers.factory import run_script_one
from helpers.starknet import Starknet
from modules.dmail.module import dmail_send_email
from modules.exchange_withdraw.config import CEX_KEYS
from modules.exchange_withdraw.functions import call_exchange_withdraw
from modules.exchange_deposit.functions import transfer_eth
from modules.nft.functions.pyramid import nft_pyramid
from modules.nft.functions.starknet_id import nft_starknet_id
from modules.nft.functions.starkverse import nft_starkverse
from modules.nft.functions.unframed import nft_unframed
from modules.swaps.functions.avnu import swap_token_avnu
from modules.swaps.functions.sithswap import swap_token_sithswap
from modules.volume.helpers import check_wait_wallet_balance, get_okx_token_balance, get_okx_account
from modules.zklend.functions.zklend_borrow import zklend_borrow_stable, get_max_borrow_amount
from modules.zklend.functions.zklend_collateral import zklend_collateral_enable
from modules.zklend.functions.zklend_deposit import zklend_deposit
from modules.zklend.functions.zklend_repay import zklend_repay_stable
from modules.zklend.functions.zklend_withdraw import zklend_withdraw


def run_one_wallet_volume(account: Starknet, recipient, cex_network):
    csv_name = f'volume_report'
    logger.info(f"[{account._id}][{account.address_original}]: Run TX Volume")

    if ETH_VOLUME_AMOUNT_PER_ACC <= ETH_VOLUME_LEFT_ON_WALLET:
        raise Exception(f'Configuration error: ETH_VOLUME_AMOUNT_PER_ACC <= ETH_VOLUME_LEFT_ON_WALLET')

    rand_pct = ETH_VOLUME_AMOUNT_PER_ACC * 0.03
    withdraw_amount = round(ETH_VOLUME_AMOUNT_PER_ACC - random.uniform(0, rand_pct), 4)
    logger.info(f'Amount: {withdraw_amount} ETH')

    # ------------------ Withdraw ETH ------------------

    call_exchange_withdraw(account.address_original, cex_network, round(withdraw_amount + 0.0001, 4), 'ETH', 'okx')
    sleeping(MIN_SLEEP, MAX_SLEEP)

    # --------------- Check wallet balance ---------------

    check_wait_wallet_balance(account, withdraw_amount, 'ETH')
    sleeping(MIN_SLEEP, MAX_SLEEP)

    # Use amount without ETH_VOLUME_LEFT_ON_WALLET - left for fees
    amount = round(withdraw_amount - ETH_VOLUME_LEFT_ON_WALLET, 4)

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
        if rand_chance == 1:
            random_call_before_swaps(account, step)

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

    transfer_eth(account, recipient, amount)
    sleeping(MIN_SLEEP, MAX_SLEEP)

    # ---------------- Check OKX balance ----------------

    while True:
        logger.info(f"[{account._id}] Check OKX main account balance")
        main_acc_balance = get_okx_token_balance(0)

        if main_acc_balance >= amount:
            logger.success(f"[{account._id}] {main_acc_balance} ETH found")
            break
        else:
            for sub_account_num in range(1, 6):
                if is_okx_sub_account(sub_account_num):
                    logger.info(f"[{account._id}] Check OKX subAccount {get_okx_sub_account_name(sub_account_num)}")
                    acc_balance = get_okx_token_balance(sub_account_num)

                    if acc_balance >= amount:
                        logger.success(f"[{account._id}] {acc_balance} ETH found, transfer to OKX main account")
                        okx_account = get_okx_account()
                        okx_account.transfer("ETH", acc_balance, get_okx_sub_account_name(sub_account_num), 'master')
                        time.sleep(3)
                        break
                    elif acc_balance > 0:
                        logger.info(
                            f"[{account._id}] Only {acc_balance} ETH found, waiting {amount} ETH...")

        sleeping(int(MIN_SLEEP / 2), int(MAX_SLEEP / 2))
        continue


def is_okx_sub_account(num):
    return len(CEX_KEYS[f'okx-sub-{num}']['api_key']) > 0


def get_okx_sub_account_name(num):
    return CEX_KEYS[f'okx-sub-{num}']['name']


def random_call_before_swaps(account, step):
    logger.info(
        f"[{account._id}][{account.address_original}] Random function before step #{step + 1}"
    )
    random_function = random.choice([
        nft_pyramid,
        nft_starknet_id,
        nft_starkverse,
        nft_unframed,
        dmail_send_email,
        zklend_collateral_enable,
    ])

    run_script_one(account, random_function, "0", [], random_function.__name__)
    sleeping(int(MIN_SLEEP / 2), MAX_SLEEP * 2)
