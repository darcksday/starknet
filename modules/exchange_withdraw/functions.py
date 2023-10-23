import ccxt
from loguru import logger

from modules.exchange_withdraw.config import CEX_KEYS
from modules.exchange_withdraw.cli import *


def call_exchange_withdraw(
        wallet_address: str,
        network: str,
        amount: float,
        token: str,
        cex: str = CEX_DEFAULT
):
    try:
        logger.info(f"{CEX_DEFAULT.upper()} - Start withdraw to {wallet_address}")
        ccxt_account = get_ccxt_account(cex)
        params = {}

        if cex == 'okx':
            ccxt_account.load_markets()
            networks = ccxt_account.currencies[token]['networks']
            params['fee'] = networks[network]['fee']
            params['pwd'] = CEX_KEYS[cex]['password']

        params['network'] = network
        ccxt_account.withdraw(
            code=token,
            amount=amount,
            address=wallet_address,
            tag=None,
            params=params
        )

        logger.success(f'{cex} withdraw {amount} {token} success => {wallet_address}')

    except Exception as error:
        logger.error(f'{cex} withdraw {token} error: {str(error)}')


def okx_get_withdrawal_info(token):
    ccxt_account = get_ccxt_account(CEX_DEFAULT)
    currencies = ccxt_account.fetch_currencies()
    networks = []
    network_data = {}

    if currencies is not None:
        for currency_code, currency in currencies.items():
            if currency_code == token.upper():
                networks_info = currency.get('networks')
                if networks_info is not None:
                    for network, network_info in networks_info.items():

                        fee = network_info.get('fee')
                        if fee is not None:
                            fee = float(fee)

                        min_withdrawal = network_info.get('limits', {}).get('withdraw', {}).get('min')
                        if min_withdrawal is not None:
                            min_withdrawal = float(min_withdrawal)

                        _id = network_info.get('id')
                        is_withdraw_enabled = network_info.get('withdraw', False)

                        if is_withdraw_enabled:
                            network_data[network] = (_id, fee, min_withdrawal)
                            networks.append(network)
                else:
                    print(f"\n>>>  Currency {currency_code} doesn't contain 'networks' attribute")
    else:
        print("\n>>>  Currencies not found")

    return networks, network_data


def get_wd_info(token):
    if CEX_DEFAULT == 'okx':
        return okx_get_withdrawal_info(token)
    else:
        raise Exception(f"Unknown exchange {CEX_DEFAULT}")


def find_starknet_network(token, print_networks=True):
    network = ''
    (list_tokens, networks) = get_wd_info(token)

    for index, (name, value) in enumerate(networks.items()):
        if 'starknet' in name.lower():
            network = name
            min_amount = "{:.5f}".format(value[2])
            if print_networks:
                logger.info(f'{name} (fee:{value[1]} | min:{min_amount})')

    if network == '':
        raise Exception('No StarkNet network withdraw enabled, check exchange withdraw info')

    return network


def get_ccxt_account(cex):
    if not CEX_KEYS[cex]['api_key'] or not CEX_KEYS[cex]['api_secret']:
        logger.error(f"Please set {cex.upper()}_API_KEY and {cex.upper()}_API_SECRET in config/.env")
        raise Exception(f"Configuration error for {cex}")

    dict_ = {
        'apiKey': CEX_KEYS[cex]['api_key'],
        'secret': CEX_KEYS[cex]['api_secret'],
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot'
        }
    }

    if cex in ['kucoin', 'okx', 'bitget']:
        dict_['password'] = CEX_KEYS[cex]['password']

    return ccxt.__dict__[cex](dict_)
