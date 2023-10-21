from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call
from common import TOKEN_ADDRESS, ZETH_TOKEN_ADDRESS
from helpers.common import int_to_wei, price_token, all_prices, wei_to_int
from modules.zklend.common import get_deposit_amount
from modules.zklend.config import ZKLEND_CONCTRACTS, ZKLEND_MAX_BORROW


def get_max_borrow_amount(account, token_symbol):
    zeth_wei = get_deposit_amount(account, ZETH_TOKEN_ADDRESS)
    eth_price = price_token(all_prices(), "ETH")
    return int(float(eth_price) * wei_to_int(zeth_wei) * ZKLEND_MAX_BORROW[token_symbol])


def zklend_borrow_stable(account, amount: float = 0, token=None):
    logger.info(f"[{account._id}][{account.address_original}]: ZkLend Borrow")
    if not token:
        token = TOKEN_ADDRESS["USDC"]

    token_symbols = {v: k for k, v in TOKEN_ADDRESS.items()}
    token_symbol = token_symbols.get(token)
    token_decimals = account.get_balance(token)["decimal"]

    if not ZKLEND_MAX_BORROW.get(token_symbol):
        logger.error(f"Wrong token: {token_symbol}, we borrow only stable coins")
        return

    # Borrow not more than max allowed in config
    max_borrow = get_max_borrow_amount(account, token_symbol)
    if not amount:
        amount = max_borrow

    if 0 < amount <= max_borrow:
        logger.info(f"[{account._id}][{account.address_original}]: Borrow {amount} {token_symbol}")

        amount_wei = int_to_wei(amount, token_decimals)
        borrow_call = Call(
            to_addr=ZKLEND_CONCTRACTS["router"],
            selector=get_selector_from_name("borrow"),
            calldata=[token, amount_wei],
        )

        transaction = account.sign_transaction([borrow_call])
        transaction_response = account.send_transaction(transaction)

        return transaction_response.transaction_hash
    else:
        error = f"Wrong amount: {amount} {f'is more than max borrow {max_borrow}' if amount > max_borrow else 'too small'}"
        logger.error(f"[{account._id}][{account.address_original}] Borrow error: {error}")
