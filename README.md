# StarkNet: All In One

This script is your ultimate companion for navigating the Starknet network effortlessly.
It offers a range of features that make working with Starknet a breeze, simplifies farm management,
and enables various network operations.

Documentation: https://starknet-aio.gitbook.io/starknet-aio/

### Features:

- Check balances.
- Check transactions count.
- Exchange withdraw ETH.
- Transfer ETH to exchange.
- Orbiter bridge.
- Dmail: send random email.
- Swaps:
    - AVNU
    - JediSwap
    - MySwap
    - 10kSwap
    - SithSwap
    - Protoss
    - RANDOM SWAP: ETH > Random Token > ETH / Random Dex
- NFT:
    - StarknetId
    - Starkverse
    - Pyramid
    - Unframed
    - RANDOM: Call random NFT function
- ZkLend:
    - Deposit (supply)
    - Withdraw
    - Enable collateral
    - Disable collateral
    - Borrow
    - Repay
    - ROUTE: Deposit ETH > Enable collateral > Borrow random token > Repay token > Withdraw ETH
- MULTIPLE Functions: make one or multiple random transactions.
- VOLUME: increase wallet tx volumes. Process step-by-step:
  Script withdraw ETH from OKX to your StarkNet wallet, then use zkLend to provide ETH as collateral and borrow USDC,
  proceed to execute multiple USDC/USDT swaps on AVNU/SithSwap (the number of swaps can be configured in config/settings.py),
  then repay the borrowed USDC and withdraw the locked ETH from zkLend. The final step is to return the ETH to OKX,
  you can use OKX sub-accounts, script automatically move ETH to your main account and repeat this process for next wallet.
  Note: before each swap step there is 50% chance to call one of functions from config/routes.py file to build unique route.

**IMPORTANT: Use OKX sub-accounts for volume and transfers to OKX, don't mix your wallets!**

## Requirements

```
1. Python 3.10+
2. Registered and activated starknet wallets.
```

You can use Braavos or ArgentX wallets.

## Installation

```
python -m venv venv
source venv/bin/activate
pip3 install wheel
pip3 install -r requirements.txt
```

## Run

```
source venv/bin/activate
python main.py
```

## Configuration

1. Copy or rename "config_sample" directory to "config".
2. Edit config/.env file to configure work with OKX.
3. Edit config/settings.py file to suit your preferences.
4. To manage your wallet addresses and private keys, edit the config/wallets.csv file.
   We recommend using a Modern CSV editor: https://www.moderncsv.com/
5. Add proxy to config/proxies.txt file, format: http://login:password@ip:port
6. Optionally, you can customize routes by editing the config/routes.py file.

#### OKX Deposit (transfer from starkNet to OKX)

To facilitate deposits, create separate deposit wallets for each of your StarkNet wallets.
Make sure to include these deposit wallet addresses in the "okx_address" column of the config/wallets.csv file.

#### OKX Withdraw

For withdrawals from OKX, ensure that your wallets are included in the StarkNet channel's withdraw whitelist.
Add the relevant wallet addresses to the "starknet_address" column in the config/wallets.csv file.

#### Transactions Volume

To manage transaction volumes effectively, consider using OKX sub-accounts.
Our script supports this feature and can transfer funds to your main account.
To enable this feature, you need to include your sub-accounts' API information in the config/.env file.

#### Orbiter Bridge

If you need to transfer ETH from web3 (Arbitrum, Optimism, etc.) to StarkNet,
add your wallet's private key to the config/wallets.csv file under the "web3_private_key" column.
