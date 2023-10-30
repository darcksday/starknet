from config.settings import MIN_SLEEP, MAX_SLEEP
from helpers.cli import sleeping
from helpers.common import get_private_keys
from helpers.starknet import Starknet
from modules.unused_contracts.functions import run_random_unused_function


def interface_unused_contracts():
    prt_keys = get_private_keys()
    for _id, wallet in enumerate(prt_keys):
        account = Starknet(wallet["index"], wallet)
        run_random_unused_function(account)

        if _id < len(prt_keys) - 1:
            sleeping(MIN_SLEEP, MAX_SLEEP)
