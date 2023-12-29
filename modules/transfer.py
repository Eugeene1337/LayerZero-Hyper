from loguru import logger
from utils.helpers import retry, sleep
from .account import Account

from config import (
    TOKEN_CONTRACTS,
    USDT_ABI
)


class Transfer(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="bsc")

        self.usdt_contract = self.get_contract(TOKEN_CONTRACTS["bsc"]["USDT"], USDT_ABI)


    async def transfer(self, address: str, amount: int):
        tx_data = await self.get_tx_data()

        transaction = await self.usdt_contract.functions.transfer(
            self.w3.to_checksum_address(address),
            amount
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    async def transfer_usdt(
            self,
            address: str,
            min_amount: float,
            max_amount: float,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = await self.get_amount(
            "bsc",
            "USDT",
            min_amount,
            max_amount,
            18,
            all_amount,
            min_percent,
            max_percent
        )

        logger.info(
            f"[{self.account_id}][{self.address}] Transfer {amount} USDT -> {address}"
        )

        await self.transfer(address, amount_wei)

        await sleep(15,30)
