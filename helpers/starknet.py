import random
import sys
import time

from typing import Union, List
from loguru import logger
from starknet_py.cairo.felt import decode_shortstring
from starknet_py.contract import Contract
from starknet_py.hash.address import compute_address
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.account.account import Account
from starknet_py.net.client_models import Call
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models import StarknetChainId, Invoke
from starknet_py.net.signer.stark_curve_signer import KeyPair

from config.settings import *
from common import *
from helpers.common import int_to_wei


class Starknet:
    def __init__(self, _id: int, wallet_data) -> None:
        self._id = _id + 1
        self.private_key = wallet_data['starknet_private_key']
        self.key_pair = KeyPair.from_private_key(self.private_key)
        if len(CUSTOM_RPC) > 0:
            self.client = FullNodeClient(random.choice(RPC["starknet"]["rpc"]))
        else:
            self.client = GatewayClient("mainnet")

        self.address_original = wallet_data['starknet_address']
        self.address = self._create_account()
        self.account = Account(
            address=self.address,
            client=self.client,
            key_pair=self.key_pair,
            chain=StarknetChainId.MAINNET,
        )
        self.account.ESTIMATED_FEE_MULTIPLIER = WEB3_FEE_MULTIPLIER
        self.explorer = RPC["starknet"]["explorer"]
        if wallet_data['web3_private_key'] is not None and len(wallet_data['web3_private_key']) > 0:
            self.web3_private_key = wallet_data['web3_private_key']

    def _create_account(self) -> Union[int, None]:
        if TYPE_WALLET == "argent":
            return self._get_argent_address()
        elif TYPE_WALLET == "braavos":
            return self._get_braavos_account()
        else:
            logger.error("Type wallet error! Available values: argent or braavos")
            sys.exit()

    def _get_argent_address(self) -> int:
        if CAIRO_VERSION == 0:
            selector = get_selector_from_name("initialize")
            calldata = [self.key_pair.public_key, 0]
            address = compute_address(
                class_hash=ARGENTX_PROXY_CLASS_HASH,
                constructor_calldata=[ARGENTX_IMPLEMENTATION_CLASS_HASH, selector, len(calldata), *calldata],
                salt=self.key_pair.public_key,
            )
            return address
        else:
            address = compute_address(
                class_hash=ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW,
                constructor_calldata=[self.key_pair.public_key, 0],
                salt=self.key_pair.public_key,
            )
            return address

    def _get_braavos_account(self) -> int:
        selector = get_selector_from_name("initializer")
        call_data = [self.key_pair.public_key]
        address = compute_address(
            class_hash=BRAAVOS_PROXY_CLASS_HASH,
            constructor_calldata=[BRAAVOS_IMPLEMENTATION_CLASS_HASH, selector, len(call_data), *call_data],
            salt=self.key_pair.public_key,
        )
        return address

    def get_contract(self, contract_address: int, abi: Union[dict, None] = None, cairo_version: int = 0):
        if abi is None:
            abi = ERC20_ABI

        contract = Contract(
            address=contract_address,
            abi=abi,
            provider=self.account,
            cairo_version=cairo_version
        )
        return contract

    def get_balance(self, contract_address: int, retry=0) -> dict:
        contract = self.get_contract(contract_address)

        try:
            symbol_data = contract.functions["symbol"].call_sync()
            decimal = contract.functions["decimals"].call_sync()
            balance_wei = contract.functions["balanceOf"].call_sync(self.address)
            balance = balance_wei.balance / 10 ** decimal.decimals

            return {
                "balance_wei": balance_wei.balance,
                "balance": balance,
                "symbol": decode_shortstring(symbol_data.symbol),
                "decimal": decimal.decimals
            }
        except Exception as error:
            if retry > 3:
                raise Exception(f"Error: {error}. max retry reached")
            time.sleep(10)
            return self.get_balance(contract_address, retry + 1)

    def sign_transaction(self, calls: List[Call], cairo_version: int = 0, retry=0):
        try:
            nonce = self.account.get_nonce_sync()
            transaction = self.account.sign_invoke_transaction_sync(
                calls=calls,
                auto_estimate=True,
                nonce=nonce,
                cairo_version=cairo_version
            )
            return transaction
        except Exception as error:
            if retry > 3:
                raise Exception(f"Error: {error}. max retry reached")
            time.sleep(10)
            return self.sign_transaction(calls, cairo_version, retry + 1)

    def send_transaction(self, transaction: Invoke):
        transaction_response = self.account.client.send_transaction_sync(transaction)
        return transaction_response

    def wait_until_tx_finished(self, tx_hash: int):
        logger.info(f"Transaction: {self.explorer}{hex(tx_hash)}")
        self.account.client.wait_for_tx_sync(tx_hash, check_interval=10)
        logger.success(f"Transaction [{self._id}][{hex(self.address)}] SUCCESS!")

    def get_swap_amount(self, from_token, amount: float) -> int:
        balance = self.account.get_balance_sync(from_token)
        if amount == 0:
            amount_wei = balance
            if from_token == TOKEN_ADDRESS["ETH"]:
                amount_wei = amount_wei - int_to_wei(MIN_BALANCE_ETH, 18)
        else:
            token = self.get_contract(from_token).functions["decimals"].call_sync()
            amount_wei = int_to_wei(amount, token.decimals)

        if amount_wei <= 0 or amount_wei > balance:
            raise Exception(f"Insufficient balance: {balance}")
        return amount_wei
