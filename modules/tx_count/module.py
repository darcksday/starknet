from loguru import logger
from helpers.common import get_private_keys
from helpers.starknet import Starknet
from modules.tx_count.functions import one_wallet_tx_count


def interface_tx_count():
    logger.info("Check Transactions Count")

    for _id, wallet in enumerate(get_private_keys()):
        account = Starknet(wallet["index"], wallet)
        one_wallet_tx_count(account)
