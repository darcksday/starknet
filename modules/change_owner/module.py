import json
from datetime import datetime

from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.hash.utils import message_signature, compute_hash_on_elements
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

from common import ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW
from config.settings import MIN_SLEEP, MAX_SLEEP
from helpers.cli import sleeping
from helpers.common import get_private_keys
from helpers.csv_helper import write_csv_error, write_csv_success, start_csv
from helpers.gas_checker import check_gas
from helpers.starknet import Starknet


def interface_change_owner():
    logger.info("Change wallet owner")

    csv_name = 'change_owner'
    start_csv(csv_name)

    wallet_list = get_private_keys()
    for _id, wallet in enumerate(wallet_list):
        account = Starknet(wallet["index"], wallet)
        if not account.address_original:
            logger.error(f'Error: No wallet address provided')
            continue

        logger.info(f"[{account._id}][{account.address_original}] deploy...")

        try:

            change_owner(account, wallet['new_private_key'],csv_name)
            #
            if _id < len(wallet_list) - 1:
                sleeping(MIN_SLEEP, MAX_SLEEP)

        except Exception as e:
            logger.error(f'Error: {e}')
            continue

@check_gas
def change_owner(account, new_private_key,csv_name):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    new_owner=KeyPair.from_private_key(new_private_key)
    selector = get_selector_from_name("change_owner")




    try:


        hash = compute_hash_on_elements([
            selector,
            StarknetChainId.MAINNET,
            account.account.address,
            account.key_pair.public_key

        ])

        r, s = message_signature(hash, new_owner.private_key)

        with open('abi/argent_wallet_abi.json') as file:
            abi = json.load(file)

        contract = account.get_contract(account.address_original, abi, 1)




        call = contract.functions["change_owner"].prepare(
            new_owner.public_key,
            r,
            s
        )
        transaction = account.sign_transaction([call])


        transaction_response = account.send_transaction(transaction)
        account.wait_until_tx_finished(transaction_response.transaction_hash)



        logger.info(f"[{account._id}][{account.address_original}] changed")
        write_csv_success(account._id, {
            'status': 1,
            'csv_name': csv_name,
            'function': 'activate_wallet',
            'date': formatted_datetime,
        })


    except Exception as e:

        logger.error(f'Error: {e}')