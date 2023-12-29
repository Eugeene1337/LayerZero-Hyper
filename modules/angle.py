from loguru import logger
from config import ANGLE_BRIDGE_ABI, ANGLE_BRIDGE_CONTRACTS, LAYERZERO_CHAINS_IDS, TOKEN_CONTRACTS
from utils.helpers import retry, sleep
from .account import Account

class Angle(Account):
    def __init__(self, account_id: int, private_key: str, from_chain: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain=from_chain)

        self.bridge_contract = self.get_contract(ANGLE_BRIDGE_CONTRACTS[from_chain], ANGLE_BRIDGE_ABI)

    async def get_l0_fee(self, to_chain: int, amount: int):

        fee = await self.bridge_contract.functions.estimateSendFee(
            LAYERZERO_CHAINS_IDS[to_chain],
            self.address,
            amount,
            False,
            "0x00010000000000000000000000000000000000000000000000000000000000030d40"
        ).call()

        return int(fee[0])

    async def bridge(self, from_chain: str, to_chain: str, amount: int):
        l0_fee = await self.get_l0_fee(to_chain, amount)

        await self.approve(amount, TOKEN_CONTRACTS[from_chain]["agEUR"], self.bridge_contract.address)
        
        tx_data = await self.get_tx_data(l0_fee)
        if from_chain == "bsc":
            tx_data["gasPrice"] = 3000000000

        transaction = await self.bridge_contract.functions.send(
            LAYERZERO_CHAINS_IDS[to_chain],
            self.address,
            amount,
            self.address,
            "0x0000000000000000000000000000000000000000",
            "0x00010000000000000000000000000000000000000000000000000000000000030d40"
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())


    @retry
    async def bridge_ageur(
            self,
            from_chain: str,
            to_chain: str,
            min_amount: float,
            max_amount: float,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):

        amount_wei, amount, balance = await self.get_amount(
            from_chain,
            "agEUR",
            min_amount,
            max_amount,
            18,
            all_amount,
            min_percent,
            max_percent
        )
        logger.info(f"[{self.account_id}][{self.address}] Angle bridge {round(amount, 3)} agEUR {from_chain.title()} -> {to_chain.title()}")

        await self.bridge(from_chain, to_chain, amount_wei)

        await sleep(90, 120)