import decimal
import random
from loguru import logger
from common import TOKEN_ADDRESS
from helpers.common import int_to_wei, wei_to_int, get_min_balance_eth
from helpers.starknet import Starknet
from helpers.web3_account import Web3Account
from modules.orbiter_bridge.config import *


def orbiter_bridge_to_starknet(account: Starknet, amount: float, from_chain: str):
    if not account.web3_private_key:
        raise Exception(f'No web3 private key for account #{account._id}')
    if not account.address_original or len(account.address_original) != 66:
        raise Exception(f'Wrong starknet recipient "{account.address_original}" for account #{account._id}')

    web3_account = Web3Account(account._id, account.web3_private_key, from_chain)
    web3_balance = web3_account.get_web3_token_balance(web3_account.address, "", True)
    if not amount:
        amount = web3_balance - get_min_balance_eth()
    amount = __get_orbiter_eth_value(amount, "starknet")
    amount_wei = int_to_wei(amount, 18)

    logger.info(f"[{account._id}][{web3_account.address}] Orbiter bridge {amount} ETH to Starknet")

    if amount < 0.005 or amount > 3:
        logger.error(f"Limit range amount for bridge 0.005 - 3 ETH | {amount} ETH")
    elif amount_wei + ORBITER_NETWORKS["starknet"] >= int_to_wei(web3_balance, 18):
        logger.error(f"Wrong amount ETH, not enough balance | {amount} ETH")
    else:
        contract = web3_account.get_contract(ORBITER_DEPOSIT_CONTRACTS[from_chain], ORBITER_DEPOSIT_ABI)
        starknet_wallet = account.address_original
        starknet_wallet = f'030{starknet_wallet[3:]}' if starknet_wallet[:3] == '0x0' else f'030{starknet_wallet[2:]}'
        recipient = bytes.fromhex(starknet_wallet)

        contract_txn = contract.functions.transfer(
            web3_account.w3.to_checksum_address(ORBITER_DEPOSIT_ROUTER),
            recipient
        ).build_transaction(
            {
                'chainId': web3_account.w3.eth.chain_id,
                "from": web3_account.address,
                "nonce": web3_account.w3.eth.get_transaction_count(web3_account.address),
                "value": amount_wei,
                'gas': 0,
                'gasPrice': 0
            }
        )

        contract_txn = web3_account.add_gas_price(contract_txn)
        contract_txn = web3_account.add_gas_limit(contract_txn)
        txn_hash = web3_account.sign_tx(contract_txn)
        web3_account.wait_until_tx_finished(txn_hash)


def orbiter_bridge_from_starknet(account: Starknet, amount, to_chain):
    web3_account = Web3Account(account._id, account.web3_private_key, to_chain)
    bridge_contract = account.get_contract(ORBITER_CONTRACT_WITHDRAW, ORBITER_WITHDRAW_ABI)
    approve_contract = account.get_contract(TOKEN_ADDRESS["ETH"])

    balance = account.account.get_balance_sync()
    if not amount:
        amount = wei_to_int(balance) - get_min_balance_eth()
    amount = __get_orbiter_eth_value(amount, to_chain)
    amount_wei = int_to_wei(amount, 18)

    logger.info(f"[{account._id}][{account.address_original}] Orbiter bridge {amount} ETH from Starknet")

    if amount < 0.005 or amount > 3:
        logger.error(f"Limit range amount for bridge 0.005 - 3 ETH | {amount} ETH")
    elif amount_wei + ORBITER_NETWORKS["starknet"] >= balance:
        logger.error(f"Wrong amount ETH, not enough balance | {amount} ETH")
    else:
        approve_call = approve_contract.functions["approve"].prepare(ORBITER_CONTRACT_WITHDRAW, 2 ** 128)
        transfer_call = bridge_contract.functions["transferERC20"].prepare(
            TOKEN_ADDRESS["ETH"],
            0x64a24243f2aabae8d2148fa878276e6e6e452e3941b417f3c33b1649ea83e11,
            amount_wei,
            int(web3_account.address, 16)
        )

        transaction = account.sign_transaction([approve_call, transfer_call])
        transaction_response = account.send_transaction(transaction)

        return transaction_response.transaction_hash


def __get_orbiter_eth_value(base_num, chain):
    base_num_dec = decimal.Decimal(str(base_num))
    orbiter_amount_dec = decimal.Decimal(str(ORBITER_AMOUNT[chain]))
    difference = base_num_dec + orbiter_amount_dec

    random_offset = decimal.Decimal(str(random.uniform(-0.000000000000001, 0.000000000000001)))
    result_dec = difference + random_offset
    orbiter_str = str(ORBITER_NETWORKS[chain])[-4:]
    result_str = '{:.18f}'.format(result_dec.quantize(decimal.Decimal('0.000000000000000001')))
    result_str = result_str[:-4] + orbiter_str
    return decimal.Decimal(result_str)
