from typing import Union

from loguru import logger
from config import BUNGEE_ABI, BUNGEE_CONTRACT
from utils.helpers import retry, sleep
from .account import Account
from utils.bungee_data import get_bungee_data

async def get_bungee_limits() -> Union[dict, bool]:
    bungee_data = await get_bungee_data()

    try:
        limits = [chain_data for chain_data in bungee_data if chain_data["name"] == "BSC"][0]["limits"]

        return limits
    except:
        return False

class Bungee(Account):
    def __init__(self, account_id: int, private_key: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain="bsc")

        self.contract = self.get_contract(BUNGEE_CONTRACT, BUNGEE_ABI)
        self.chain_ids = {
            "GNOSIS": 100,
            "POLYGON": 137,
        }

    @retry
    async def refuel(self, to_chain: str, amount: int):
        logger.info(f"[{self.account_id}][{self.address}] Bungee refuel {round(amount, 4)} BNB -> {to_chain.title()}")

        amount_wei = self.w3.to_wei(amount, 'ether')

        limits = await get_bungee_limits()

        to_chain_limits = [
            chain for chain in limits if chain["chainId"] == self.chain_ids[to_chain] and chain["isEnabled"]
        ]

        if to_chain_limits:
            tx_data = await self.get_tx_data(amount_wei)

            transaction = self.contract.functions.depositNativeToken(
                self.chain_ids[to_chain],
                self.address
            )

            transaction = await transaction.build_transaction(tx_data)
            
            signed_txn = await self.sign(transaction)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Bungee refuel destination chain inactive!")

        await sleep(5, 10)