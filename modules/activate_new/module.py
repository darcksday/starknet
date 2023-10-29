from loguru import logger
from starknet_py.net.models import StarknetChainId

from common import ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW
from helpers.common import get_private_keys
from helpers.starknet import Starknet


def interface_deploy_argent_wallet():
    logger.info("Deploy new argent wallets")

    for _id, wallet in enumerate(get_private_keys()):
        account = Starknet(_id, wallet)
        nonce = account.account.get_nonce_sync()
        print('nonce', nonce)

        if nonce > 0:
            logger.info(f"Account {_id} already deployed")
            continue

        logger.info(f"[{account._id}][{account.address_original}] deploy...")
        transaction = account.account.deploy_account(
            address=account.address_original,
            class_hash=ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW,
            salt=account.key_pair.public_key,
            key_pair=account.key_pair,
            client=account.client,
            chain=StarknetChainId.MAINNET,
            constructor_calldata=[account.key_pair.public_key, 0],
            auto_estimate=True
        )

        account.wait_until_tx_finished(transaction.transaction_hash)
