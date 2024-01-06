from loguru import logger
from config import MERKLY_REFUEL_ABI, MERKLY_REFUEL_CONTRACTS, LAYERZERO_CHAINS_IDS, MERKLY_OFT_CONTRACTS, MERKLY_OFT_ABI, TOKEN_CONTRACTS
from utils.helpers import retry
from .account import Account
from utils.sleeping import sleep

class Merkly(Account):
    def __init__(self, account_id: int, private_key: str, from_chain: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain=from_chain)

    async def estimate_bridge_fee(self, contract, to_chain_id, amount):
        try:
            fee = await contract.functions.estimateSendFee(
                to_chain_id,
                self.address,
                amount,
                False,
                b"",
            ).call()

            return fee[0]
        except Exception as error:
            logger.error(error)


    async def mint_merk_if_needed(self, merk_needed: int):
        balance = await self.get_balance(MERKLY_OFT_CONTRACTS[self.chain])
        balance_wei = balance['balance_wei']
        contract = self.get_contract(MERKLY_OFT_CONTRACTS[self.chain], MERKLY_OFT_ABI)

        if (balance_wei < merk_needed):
            logger.info(f"MERK balance is negative, going to mint $MERK")

            fee = await contract.functions.fee().call()
            amount = int(self.w3.from_wei(merk_needed - balance_wei, 'ether'))
            tx_data = await self.get_tx_data(fee * amount)

            transaction = await contract.functions.mint(
                self.address,
                amount
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())

            await sleep(10,20)

        else:
            logger.info(f"MERK balance is positive, continue to bridge")
        

    async def get_gas_refuel(self, from_chain: str, to_chain: str, amount: int, to_token: str):
        contract = self.get_contract(MERKLY_REFUEL_CONTRACTS[from_chain], MERKLY_REFUEL_ABI)
        
        adapter_params = await self.get_adapter_params(amount)
        fee = await contract.functions.estimateSendFee(LAYERZERO_CHAINS_IDS[to_chain], '0x', adapter_params).call()
        fee = int(fee[0] * 1.01)

        tx_data = await self.get_tx_data(fee)

        transaction = await contract.functions.bridgeGas(
            LAYERZERO_CHAINS_IDS[to_chain],
            self.address,
            adapter_params
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())


    @retry
    async def bridge(self, to_chain: str, amount: int):
        logger.info(f"[{self.account_id}][{self.address}] Merkly bridge $MERK -> {to_chain.title()}")

        contract = self.get_contract(MERKLY_OFT_CONTRACTS[self.chain], MERKLY_OFT_ABI)
        to_chain_id = LAYERZERO_CHAINS_IDS[to_chain]

        fee = await self.estimate_bridge_fee(contract, to_chain_id, amount)

        tx_data = await self.get_tx_data(fee)

        transaction = await contract.functions.sendFrom(
            self.address,
            to_chain_id,
            f"{self.address}",
            amount,
            "0x0000000000000000000000000000000000000000",
            "0x0000000000000000000000000000000000000000",
            b""
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

        await sleep(10, 20)


    @retry
    async def gas_refuel(
            self,
            from_chain: str,
            from_token: str,
            to_chain: str,
            to_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int,
            route: bool,
    ):
        
        amount_wei, amount, balance = await self.get_amount(
            from_chain,
            from_token,
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )
        
        logger.info(f"[{self.account_id}][{self.address}] Merkly refuel {round(amount, 4)} {from_token} -> {to_chain.title()}")
        
        initial_balance = await self.get_initial_balance(chain=to_chain)

        await self.get_gas_refuel(from_chain, to_chain, amount_wei, to_token)

        if route:
            await self.wait_for_balance_update(chain=to_chain, initial_balance=initial_balance)

        await sleep(5, 10)