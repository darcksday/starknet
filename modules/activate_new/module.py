from loguru import logger
from starknet_py.net.models import StarknetChainId

from common import ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW
from helpers.common import get_private_keys
from helpers.starknet import Starknet


def interface_deploy_argent_wallet():
    logger.info("Deploy new argent wallets")

    for _id, wallet in enumerate(get_private_keys()):
        account = Starknet(_id, wallet)
        if not account.address_original:
            logger.error(f'Error: No wallet address provided')
            continue

        logger.info(f"[{account._id}][{account.address_original}] deploy...")

        try:
            transaction = account.account.deploy_account_sync(
                address=account.address_original,
                class_hash=ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW,
                salt=account.key_pair.public_key,
                key_pair=account.key_pair,
                client=account.client,
                chain=StarknetChainId.MAINNET,
                constructor_calldata=[account.key_pair.public_key, 0],
                auto_estimate=True
            )
            print('transaction', transaction)
            account.wait_until_tx_finished(transaction.transaction_hash)
        except Exception as e:
            logger.error(f'Error: {e}')
            continue
