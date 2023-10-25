# Wallet settings
# CAIRO_VERSION: 0 for Braavos and OLD ArgentX wallets (created till Sep 2023) or 1 for new ArgentX wallets.
CAIRO_VERSION = 0
TYPE_WALLET = "braavos"  # argent/braavos
CUSTOM_RPC = ''

# Gwei limit - allow to wait for a lower gas price
CHECK_GWEI = True
MAX_GWEI = 20

# Multiply web3 gas - used in Orbiter Bridge
WEB3_FEE_MULTIPLIER = 1.2

# Shuffle allow to randomize wallets order
USE_SHUFFLE = True
USE_REF = True

# Scheduler allow to run script at specific time.
# False or "2023-08-15 22:36" format
SCHEDULE_TIME = False

# Based on StarkNet "speed" we recommend to use at least 30 seconds for sleep time
MIN_SLEEP = 30
MAX_SLEEP = 40

# Swaps module settings
SLIPPAGE_PCT = 1

# Minimal wallet balance (stay when we chose to swap all)
MIN_BALANCE_ETH = 0.0007

# Volume module settings
# How much ETH we want to swap (almost all ETH you have on OKX minus some ETH for fees)
ETH_VOLUME_AMOUNT_PER_ACC = 2.5
# How many swap repeats [from, to] we want to do per account
VOLUME_SWAP_REPEATS = [3, 4]
# How many ETH we want to leave on wallet from ETH_VOLUME_AMOUNT_PER_ACC
# funds need to pay fees & left some amount on wallet to look like a real user
ETH_VOLUME_LEFT_ON_WALLET = 0.003

# CEX to be used for withdraw
CEX_DEFAULT = 'okx'
