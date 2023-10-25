import time


def get_deposit_amount(account, token: str = None, retry=0):
    try:
        zklend_contract = account.get_contract(token)
        amount_data = zklend_contract.functions["balanceOf"].call_sync(
            account.address
        )
        return amount_data.balance
    except Exception as error:
        if retry > 5:
            raise Exception(f"Error: {error}. max retry reached")

        time.sleep(10)
        return get_deposit_amount(account, token, retry + 1)
