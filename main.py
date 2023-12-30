import asyncio
import random
import time
import sys
import questionary
from concurrent.futures import ThreadPoolExecutor

from loguru import logger
from termcolor import cprint

from questionary import Choice
from utils.titles import TITLE, TITLE_COLOR
from config import ACCOUNTS, DEPOSIT_ADDRESSES
from modules_settings import *
from settings import (
    RANDOM_WALLET,
    QUANTITY_THREADS,
    THREAD_SLEEP_FROM,
    THREAD_SLEEP_TO
)

def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("1) Маршрут Hyper Hyper by Krajekis", "route"),
            Choice("2) Прогрев (Merkly gas refuel Polygon -> Celo)", "warmup"),
            Choice("3) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        sys.exit()
    return result


def get_wallets(module: str):
    if module == "route":
        account_with_deposit_address = dict(zip(ACCOUNTS, DEPOSIT_ADDRESSES))

        if len(DEPOSIT_ADDRESSES) == 0:
            logger.error("deposit_addresses.txt is empty!")
            return
        
        if len(ACCOUNTS) == 0:
            logger.error("accounts.txt is empty!")
        
        wallets = [
            {
                "id": _id,
                "key": key,
                "deposit_address": account_with_deposit_address[key],
            } for _id, key in enumerate(account_with_deposit_address, start=1)
        ]
    else:
        wallets = [
            {
                "id": _id,
                "key": key,
            } for _id, key in enumerate(ACCOUNTS, start=1)
        ]

    return wallets


def _async_run_route(account_id, key, deposit_address):
    asyncio.run(run_route(account_id, key, deposit_address))

def _async_run_warmup(account_id, key, deposit_address):
    asyncio.run(run_warmup(account_id, key))


async def run_route(account_id, key, deposit_address):
    try:
        await bungee_refuel(account_id, key)
        await pancake_swap_bnb_usdt(account_id, key)
        await stargate_bridge(account_id, key)
        await merkly_gas_refuel(account_id, key)
        await transfer_usdt(account_id, key, deposit_address)
        await pancake_swap_usdt_ageur(account_id, key)
        await angle_bridge(account_id, key)
        await sushi_swap_aguer_to_matic(account_id, key)
        await merkly_bridge(account_id, key)
        logger.success(f"[{account_id}] Account {account_id} ТРАХНУТ")
    except Exception as e:
        logger.error(e)


async def run_warmup(account_id, key):
    try:
        await merkly_gas_refuel_warmup(account_id, key)
        logger.success(f"[{account_id}] Account {account_id} ПРОГРЕТ! АХ ТЫ ЕБУН!!")
    except Exception as e:
        pass


def main():
    module = get_module()
    module_function = _async_run_route if module =="route" else _async_run_warmup

    wallets = get_wallets(module)

    if RANDOM_WALLET:
        random.shuffle(wallets)

    with ThreadPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        for _, account in enumerate(wallets, start=1):
            executor.submit(
                module_function,
                account.get("id"),
                account.get("key"),
                account.get("deposit_address", None)
            )
            time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))



if __name__ == '__main__':
    cprint(TITLE, TITLE_COLOR)
    logger.add("logging.log")
    main()
    logger.success("ШАЙТАН МАШИНА ОТРАБОТАЛА УСПЕШНО. ДИ ПИТЬ КОФЕ")