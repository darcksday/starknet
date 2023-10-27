import json

with open('abi/zklend/abi.json') as file:
    ZKLEND_ABI = json.load(file)

ZKLEND_CONCTRACTS = {
    "router": 0x04c0a5193d58f74fbace4b74dcf65481e734ed1714121bdc571da345540efa05,
    "ETH": 0x01b5bd713e72fdc5d63ffd83762f81297f6175a5e0a4771cdadbc1dd5fe72cb1,
    "USDC": 0x047ad51726d891f972e74e4ad858a261b43869f7126ce7436ee0b2529a98f486,
    "DAI": 0x062fa7afe1ca2992f8d8015385a279f49fad36299754fb1e9866f4f052289376,
    "USDT": 0x00811d8da5dc8a2206ea7fd0b28627c2d77280a515126e62baa4d78e22714c4a
}

ZKLEND_MAX_BORROW = {
    # "ETH": 0.75,
    "USDC": 0.65,
    "DAI": 0.6,
    "USDT": 0.6
}
