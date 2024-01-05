import json

with open("accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

with open("deposit_addresses.txt", "r") as file:
    DEPOSIT_ADDRESSES= [row.strip() for row in file]

with open("data/abi/pancake/router.json", "r") as file:
    PANCAKE_ROUTER_ABI = json.load(file)

with open("data/abi/pancake/quoter.json", "r") as file:
    PANCAKE_QUOTER_ABI = json.load(file)

with open("data/abi/sushi/route_processor.json", "r") as file:
    SUSHI_ROUTE_PROCESSOR_ABI = json.load(file)

with open("data/abi/stargate/router.json", "r") as file:
    STARGATE_ROUTER_ABI = json.load(file)

with open("data/abi/merkly/refuel.json", "r") as file:
    MERKLY_REFUEL_ABI = json.load(file)

with open("data/abi/merkly/oft.json", "r") as file:
    MERKLY_OFT_ABI = json.load(file)

with open("data/abi/angle/bridge.json", "r") as file:
    ANGLE_BRIDGE_ABI = json.load(file)

with open('data/rpc.json') as file:
    RPC = json.load(file)

with open('data/abi/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open('data/abi/usdt_abi.json') as file:
    USDT_ABI = json.load(file)

with open("data/abi/bungee/abi.json", "r") as file:
    BUNGEE_ABI = json.load(file)


PANCAKE_CONTRACTS = {
    "router": "0x13f4EA83D0bd40E75C8222255bc855a974568Dd4",
    "quoter": "0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997"
}

SUSHISWAP_CONTRACT = "0xE7eb31f23A5BefEEFf76dbD2ED6AdC822568a5d2"

TOKEN_CONTRACTS = {
    'bsc': {'BNB': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
            'USDT': '0x55d398326f99059ff775485246999027b3197955',
            'agEUR': '0x12f31B73D812C6Bb0d735a218c086d44D5fe5f89'},
    'polygon': {'MATIC': '0x0000000000000000000000000000000000001010',
                'agEUR': '0xE0B52e49357Fd4DAf2c15e02058DCE6BC0057db4'},
    'base': {'USDC': '0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA'},
    'gnosis': {'agEUR': '0x4b1E2c2762667331Bc91648052F646d1b0d35984'},
    'celo': {
        'agEUR': '0xC16B81Af351BA9e64C1a069E3Ab18c244A1E3049',
        'celo': '0x471EcE3750Da237f93B8E339c536989b8978a438'
    }
}

STARGATE_CONTRACTS = {
    "bsc": "0x4a364f8c717cAAD9A442737Eb7b8A55cc6cf18D8",
    "base": "0x45f1A95A4D3f3836523F5c83673c797f4d4d263B"
}

BUNGEE_CONTRACT = "0xBE51D38547992293c89CC589105784ab60b004A9"

LAYERZERO_CHAINS_IDS = {
    'bsc'       : 102,
    'avalanche' : 106,
    'aptos'     : 108,
    'polygon'   : 109,
    'arbitrum'  : 110,
    'optimism'  : 111,
    'fantom'    : 112,
    'harmony'   : 116,
    'celo'      : 125,
    'moonbeam'  : 126,
    'fuse'      : 138,
    'gnosis'    : 145,
    'klaytn'    : 150,
    'metis'     : 151,
    'core'      : 153,
    'zksync'    : 165,
    'moonriver' : 167,
    'tenet'     : 173,
    'nova'      : 175,
    'kava'      : 177,
    'meter'     : 176,
    "base"      : 184,
    'dfk'       : 115,
    'loot'      : 197,
    'opbnb'     : 202,
    'conflux'   : 212,
    'tomo'      : 196
}

STARGATE_POOL_IDS = {
    'bsc': { 'USDT': 2},
    'base': {'USDC': 1}
}

MERKLY_REFUEL_CONTRACTS = {
    'polygon': "0x0E1f20075C90Ab31FC2Dd91E536e6990262CF76d",
    'gnosis': "0x556F119C7433b2232294FB3De267747745A1dAb4",
}

ANGLE_BRIDGE_CONTRACTS = {
    "bsc": "0xe9f183FC656656f1F17af1F2b0dF79b8fF9ad8eD",
    "gnosis": "0xfa5ed56a203466cbbc2430a43c66b9d8723528e7",
    "celo": "0xf1ddcaca7d17f8030ab2eb54f2d9811365efe123"
}

MERKLY_OFT_CONTRACTS = {
    'polygon': "0x70ea00aB512d13dAc5001C968F8D2263d179e2D2"
}
