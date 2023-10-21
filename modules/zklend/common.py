def get_deposit_amount(account, token: str = None):
    zklend_contract = account.get_contract(token)
    amount_data = zklend_contract.functions["balanceOf"].call_sync(
        account.address
    )
    return amount_data.balance
