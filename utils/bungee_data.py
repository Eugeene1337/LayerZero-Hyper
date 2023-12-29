import aiohttp

async def get_bungee_data():
    async with aiohttp.ClientSession() as session:
        url = "https://refuel.socket.tech/chains"
        response = await session.get(url)
        response_data = await response.json()
        if response.status == 200:
            data = response_data["result"]
            return data
        return False

async def get_quote(from_chain_id, to_chain_id, amount):
    async with aiohttp.ClientSession() as session:
        url = f"https://refuel.socket.tech/quote?fromChainId={from_chain_id}&toChainId={to_chain_id}&amount={amount}"
        response = await session.get(url)
        response_data = await response.json()
        if response.status == 200:
            data = response_data["result"]
            return data
        return False