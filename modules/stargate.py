from loguru import logger
from config import STARGATE_CONTRACTS, STARGATE_ROUTER_ABI, TOKEN_CONTRACTS, LAYERZERO_CHAINS_IDS, STARGATE_POOL_IDS
from utils.helpers import retry, sleep
from .account import Account


class Stargate(Account):
    def __init__(self, account_id: int, private_key: str, from_chain: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, chain=from_chain)

        self.contract = self.get_contract(STARGATE_CONTRACTS[from_chain], STARGATE_ROUTER_ABI)

    async def get_l0_fee(self, to_chain: int, gas_on_destionation_params: any):
        
        
        fee = await self.contract.functions.quoteLayerZeroFee(
            LAYERZERO_CHAINS_IDS[to_chain],
            1,
            self.address,
            "0x",
            gas_on_destionation_params
        ).call()

        return int(fee[0] * 1.1)

    async def get_gas_on_destionation(self, gas_on_destination: int = 0):
        if(gas_on_destination != 0):
            return  {
                'dstGasForCall': 0,
                'dstNativeAmount': gas_on_destination,
                'dstNativeAddr': self.address
            }
        else:
            return  {
                'dstGasForCall': 0,
                'dstNativeAmount': 0,
                'dstNativeAddr': "0x"
            }


    async def bridge_token(self, from_chain: str, to_chain: str, from_token: str, to_token: str, amount: int, slippage: float, gas_on_destination: int):
        gas_on_destionation_params = await self.get_gas_on_destionation(gas_on_destination)

        l0_fee = await self.get_l0_fee(to_chain, gas_on_destionation_params)

        await self.approve(amount, TOKEN_CONTRACTS[from_chain][from_token], self.contract.address)

        tx_data = await self.get_tx_data(l0_fee)

        transaction = await self.contract.functions.swap(
            LAYERZERO_CHAINS_IDS[to_chain],
            STARGATE_POOL_IDS[from_chain][from_token],
            STARGATE_POOL_IDS[to_chain][to_token],
            self.address,
            amount,
            int(amount - (amount / 100 * slippage)),
            gas_on_destionation_params,
            self.address,
            "0x"
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())


    @retry
    async def bridge(
            self,
            from_chain: str,
            from_token: str,
            to_chain: str,
            to_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: int,
            gas_on_destination: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
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

        gas_on_destination = self.w3.to_wei(gas_on_destination, 'ether')
        logger.info(f"[{self.account_id}][{self.address}] Stargate bridge {round(amount, 3)} {from_chain.title()} {from_token} -> {to_chain.title()} {to_token}")

        await self.bridge_token(from_chain, to_chain, from_token, to_token, amount_wei, slippage, gas_on_destination)

        await sleep(90, 120)

        if(gas_on_destination != 0):
            await sleep(20, 40)


