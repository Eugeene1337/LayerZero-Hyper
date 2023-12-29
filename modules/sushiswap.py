import requests
import json

from loguru import logger
from utils.helpers import retry, sleep
from .account import Account

from config import (
    SUSHI_ROUTE_PROCESSOR_ABI,
    SUSHISWAP_CONTRACT,
    TOKEN_CONTRACTS,
)

class Sushiswap(Account):
    def __init__(self, account_id: int, private_key: str, chain: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain=chain)

        self.contract = self.get_contract(SUSHISWAP_CONTRACT, SUSHI_ROUTE_PROCESSOR_ABI)


    async def swap_tokens(self, chain: str, from_token: str, to_token: str, amount_wei: int):
        await self.approve(amount_wei, TOKEN_CONTRACTS[chain][from_token], SUSHISWAP_CONTRACT)

        tx_data = await self.get_tx_data()

        address = self.address.replace("0x", "")
        transaction = await self.contract.functions.processRoute(
            TOKEN_CONTRACTS[chain][from_token],
            amount_wei,
            TOKEN_CONTRACTS[chain][to_token],
            0,
            self.address,
            f"0x02e0b52e49357fd4daf2c15e02058dce6bc0057db401ffff0082a54e66c05fcd555adae593848a4257c9e51ad900019011032a7ac3a87ee885b6c08467ac46ad11cd042791bca1f2de4661ed88a30c99a7a9449aa8417400019011032a7ac3a87ee885b6c08467ac46ad11cd00e7eb31f23a5befeeff76dbd2ed6adc822568a5d2010d500b1d8e8ef31e21c99d1db9a6444d3adf127001ffff0200{address}"
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())


    @retry
    async def swap(
            self,
            chain: str,
            from_token: str,
            to_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = await self.get_amount(
            chain,
            from_token,
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        if amount > 10:
            amount_wei, amount, balance = await self.get_amount(
                chain,
                from_token,
                2,
                2,
                decimal,
                False,
                min_percent,
                max_percent
            )

        logger.info(
            f"[{self.account_id}][{self.address}] Sushiswap {round(amount, 3)} {from_token} -> {to_token} | {chain.title()} chain"
        )
        
        await self.swap_tokens(chain, from_token, to_token, amount_wei)

        await sleep(15,30)
