from modules import *


async def pancake_swap_bnb_usdt(account_id, key):
    from_token = "BNB"
    to_token = "USDT"

    all_amount = True
    min_percent = 95
    max_percent = 96

    min_amount = 0
    max_amount = 0
    decimal = 18
    slippage = 2

    pancake = Pancake(account_id, key)
    await pancake.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


async def stargate_bridge(account_id, key):
    bridge_list = [
        {"from_chain": "bsc", "from_token": "USDT", "to_chain": "base", "to_token": "USDC", "gas_on_destionation": 0.0017},
        {"from_chain": "base", "from_token": "USDC", "to_chain": "bsc", "to_token": "USDT", "gas_on_destionation": 0},
        {"from_chain": "bsc", "from_token": "USDT", "to_chain": "base", "to_token": "USDC", "gas_on_destionation": 0},
        {"from_chain": "base", "from_token": "USDC", "to_chain": "bsc", "to_token": "USDT", "gas_on_destionation": 0},
        {"from_chain": "bsc", "from_token": "USDT", "to_chain": "base", "to_token": "USDC", "gas_on_destionation": 0},
        {"from_chain": "base", "from_token": "USDC", "to_chain": "bsc", "to_token": "USDT", "gas_on_destionation": 0},
    ]

    all_amount = True
    min_percent = 100
    max_percent = 100

    decimal = 6
    slippage = 1

    for item in bridge_list:
        from_chain = item['from_chain']
        from_token = item['from_token']
        to_chain = item['to_chain']
        to_token = item['to_token']
        gas_on_destionation = item['gas_on_destionation']

        stargate = Stargate(account_id, key, from_chain)
        await stargate.bridge(from_chain, from_token, to_chain, to_token, 0, 0, decimal, slippage, gas_on_destionation, all_amount, min_percent, max_percent)


async def transfer_usdt(account_id, key, address):
    
    min_amount = 1
    max_amount = 1

    all_amount = True

    min_percent = 99
    max_percent = 99

    transfer = Transfer(account_id, key)
    await transfer.transfer_usdt(
       address, min_amount, max_amount, all_amount, min_percent, max_percent
    )


async def pancake_swap_usdt_ageur(account_id, key):
    from_token = "USDT"
    to_token = "agEUR"

    all_amount = True
    min_percent = 100
    max_percent = 100
    
    min_amount = 1
    max_amount = 1
    decimal = 18
    slippage = 2

    pancake = Pancake(account_id, key)
    await pancake.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


async def angle_bridge(account_id, key):
    bridge_list = [
        {"from_chain": "bsc", "to_chain": "gnosis"},
        {"from_chain": "gnosis", "to_chain": "celo"},
        {"from_chain": "celo", "to_chain": "gnosis"},
        {"from_chain": "gnosis", "to_chain": "polygon"},
    ]

    all_amount = True
    min_percent = 100
    max_percent = 100

    for item in bridge_list:
        from_chain = item['from_chain']
        to_chain = item['to_chain']

        angle = Angle(account_id, key, from_chain)
        await angle.bridge_ageur(from_chain, to_chain, 0, 0, all_amount, min_percent, max_percent)


async def sushi_swap_aguer_to_matic(account_id, key):
    chain = "polygon"
    from_token = "agEUR"
    to_token = "MATIC"

    all_amount = True
    min_percent = 100
    max_percent = 100

    min_amount = 1
    max_amount = 1
    decimal = 6

    sushiswap = Sushiswap(account_id, key, chain)
    await sushiswap.swap(
        chain, from_token, to_token, min_amount, max_amount, decimal, all_amount, min_percent, max_percent
    )


async def merkly_bridge(account_id, key):
    merkly = Merkly(account_id, key, from_chain="polygon")

    chain_list = [
        {"name": "conflux", "amount": 1 * 10**18},
        {"name": "loot", "amount": 1 * 10**18},
        {"name": "dfk", "amount": 1 * 10**18},
        {"name": "kava", "amount": 1 * 10**18},
        {"name": "moonriver", "amount": 1 * 10**18},
        {"name": "moonbeam", "amount": 1 * 10**18},
        {"name": "harmony", "amount": 1 * 10**18},
        {"name": "tomo", "amount": 5 * 10**18},
        {"name": "core", "amount": 1 * 10**18},
        {"name": "opbnb", "amount": 1 * 10**18},
    ]

    max_merk_amount_needed = sum(item['amount'] for item in chain_list) + 3

    await merkly.mint_merk_if_needed(max_merk_amount_needed)

    for item in chain_list:
        chain = item['name']
        amount = item['amount']
        await merkly.bridge(chain, amount)


async def bungee_refuel(account_id, key):
    bungee = Bungee(account_id, key)
    chain_list = [
        {"name": "GNOSIS", "amount": 0.003},
        {"name": "POLYGON", "amount": 0.001}
    ]
    for item in chain_list:
        chain = item['name']
        in_amount = item['amount']

        await bungee.refuel(chain, in_amount)


async def merkly_gas_refuel(account_id, key):
    from_chain = "gnosis"
    from_token = "xDAI"
    to_chain = "celo"

    min_amount = 0.25
    max_amount = 0.3
    decimal = 18

    all_amount = False

    min_percent = 10
    max_percent = 10

    merkly = Merkly(account_id, key, from_chain)
    await merkly.gas_refuel(from_chain, from_token, to_chain, min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def merkly_gas_refuel_warmup(account_id, key):
    from_chain = "polygon"
    from_token = "MATIC"
    to_chain = "celo"

    min_amount = 0.03
    max_amount = 0.04

    decimal = 6
    all_amount = False
    min_percent = 1
    max_percent = 1

    merkly = Merkly(account_id, key, from_chain)
    await merkly.gas_refuel(from_chain, from_token, to_chain, min_amount, max_amount, decimal, all_amount, min_percent, max_percent)