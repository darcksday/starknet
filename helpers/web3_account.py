import sys
import time
import math
from hexbytes import HexBytes
from loguru import logger
from web3 import Web3
from eth_account import Account as EthereumAccount
from web3.exceptions import TransactionNotFound
from config.settings import WEB3_FEE_MULTIPLIER
from common import CHAINS, ERC20_ABI
from helpers.common import wei_to_int


class Web3Account:
    def __init__(self, _id: int, private_key: str, chain: str = "ethereum") -> None:
        self._id = _id
        self.private_key = private_key

        self.w3 = Web3(Web3.HTTPProvider(CHAINS[chain]['rpc']))
        self.account = EthereumAccount.from_key(private_key)
        self.address = self.account.address
        self.explorer = CHAINS[chain]["explorer"]

    def get_contract(self, contract_address: str, abi=None):
        contract_address = Web3.to_checksum_address(contract_address)

        if abi is None:
            abi = ERC20_ABI
        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        return contract

    def add_gas_price(self, contract_txn):
        try:
            contract_txn['gasPrice'] = int(self.w3.eth.gas_price)
        except Exception as error:
            logger.error(f'Gas Price error: {error}')
        return contract_txn

    def add_gas_limit(self, contract_txn):
        gas_limit = self.w3.eth.estimate_gas(contract_txn)
        contract_txn['gas'] = int(gas_limit * WEB3_FEE_MULTIPLIER)
        return contract_txn

    def sign_tx(self, contract_txn):
        signed_tx = self.w3.eth.account.sign_transaction(contract_txn, self.private_key)
        raw_tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = self.w3.to_hex(raw_tx_hash)

        return tx_hash

    def wait_until_tx_finished(self, tx_hash: HexBytes, max_wait_time=180):
        start_time = time.time()
        while True:
            try:
                receipts = self.w3.eth.get_transaction_receipt(tx_hash)
                status = receipts.get("status")
                if status == 1:
                    logger.success(f"[{self._id}][{self.address}] {self.explorer}{tx_hash.hex()} successfully!")
                    return True
                elif status is None:
                    time.sleep(1)
                else:
                    logger.error(f"[{self._id}][{self.address}] {self.explorer}{tx_hash.hex()} transaction failed!")
                    return False
            except TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    logger.error(f'TX FAILED: {tx_hash.hex()}')
                    return False
                time.sleep(1)

    def check_data_token(self, token_address, abi=None):
        if abi is None:
            abi = ERC20_ABI

        try:
            token_contract = self.w3.contract(address=self.w3.to_checksum_address(token_address), abi=abi)
            decimals = token_contract.functions.decimals().call()
            symbol = token_contract.functions.symbol().call()
            return token_contract, decimals, symbol

        except Exception as error:
            logger.error(f'Error: {error}')

    def get_web3_token_balance(self, wallet_address: str, contract_address: str = '', balance_round: bool = False):
        try:
            if contract_address == '':
                balance = self.w3.eth.get_balance(self.w3.to_checksum_address(wallet_address))
                token_decimal = 18
            else:
                token_contract, token_decimal, symbol = self.check_data_token(contract_address)
                balance = token_contract.functions.balanceOf(self.w3.to_checksum_address(wallet_address)).call()

            if balance_round:
                wei = wei_to_int(balance, token_decimal)
                round_decimals = 8
                factor = 10 ** round_decimals
                rounded_number = math.floor(wei * factor) / factor
                return rounded_number
            return int(balance)

        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f'{exc_type}: {str(error)}. {exc_tb.tb_frame.f_code.co_filename}, line: {exc_tb.tb_lineno}')
            time.sleep(10)
            return self.get_web3_token_balance(wallet_address, contract_address, balance_round)
