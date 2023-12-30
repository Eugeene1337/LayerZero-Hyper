import time
from loguru import logger

from utils.helpers import retry, sleep
from .account import Account

from config import (
    PANCAKE_ROUTER_ABI,
    PANCAKE_QUOTER_ABI,
    PANCAKE_CONTRACTS,
    TOKEN_CONTRACTS
)

class Pancake(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="bsc")

        self.swap_contract = self.get_contract(PANCAKE_CONTRACTS["router"], PANCAKE_ROUTER_ABI)
    

    async def get_min_amount_out(self, from_token: str, to_token: str, amount: int, slippage: float):
        quoter = self.get_contract(PANCAKE_CONTRACTS["quoter"], PANCAKE_QUOTER_ABI)

        quoter_data = await quoter.functions.quoteExactInputSingle((
            self.w3.to_checksum_address(TOKEN_CONTRACTS["bsc"][from_token]),
            self.w3.to_checksum_address(TOKEN_CONTRACTS["bsc"][to_token]),
            amount,
            500,
            0
        )).call()

        return int(quoter_data[0] - (quoter_data[0] / 100 * slippage))
    

    async def swap_to_token(self, from_token: str, to_token: str, amount: int, slippage: int):
        if from_token != "BNB":
            await self.approve(amount, TOKEN_CONTRACTS["bsc"][from_token], PANCAKE_CONTRACTS["router"])

        tx_data_amount = amount if from_token == "BNB" else 0

        tx_data = await self.get_tx_data(tx_data_amount)
        tx_data["gasPrice"] = 3000000000
        
        deadline = int(time.time()) + 1000000

        min_amount_out = await self.get_min_amount_out(from_token, to_token, amount, slippage)

        transaction_data = self.swap_contract.encodeABI(
            fn_name="exactInputSingle",
            args=[(
                self.w3.to_checksum_address(TOKEN_CONTRACTS["bsc"][from_token]),
                self.w3.to_checksum_address(TOKEN_CONTRACTS["bsc"][to_token]),
                500,
                self.address,
                amount,
                min_amount_out,
                0
            )]
        )

        contract_txn = await self.swap_contract.functions.multicall(
            deadline, [transaction_data]
        ).build_transaction(tx_data)

        signed_txn = await self.sign(contract_txn)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())


    @retry
    async def swap(
        self,
        from_token: str,
        to_token: str,
        min_amount: float,
        max_amount: float,
        decimal: int,
        slippage: int,
        all_amount: bool,
        min_percent: int,
        max_percent: int
    ):
        amount_wei, amount, balance = await self.get_amount(
            "bsc",
            from_token,
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        logger.info(
            f"[{self.account_id}][{self.address}] Pancakeswap {round(amount, 4)} {from_token} -> {to_token} | BNB chain"
        )

        await self.swap_to_token(from_token, to_token, amount_wei, slippage)

        await self.wait_for_balance_change(TOKEN_CONTRACTS["bsc"][to_token], balance)

        await sleep(15,30)
