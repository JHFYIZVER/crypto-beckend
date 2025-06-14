from aiohttp import ClientSession

class HTTPClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self._session = None

    async def init(self):
        self._session = ClientSession(
            base_url=self.base_url,
            headers={
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': self.api_key,
            }
        )

    async def close(self):
        if self._session:
            await self._session.close()

class CryptoClient(HTTPClient):
    async def get_all_data(self):
        async with self._session.get("/v1/cryptocurrency/listings/latest") as response:
            data = await response.json()
            return [
                {"id": coin["id"], "name": coin["name"]}
                for coin in data["data"]
            ]

    async def get_id_data(self, id: int):
        async with self._session.get("/v2/cryptocurrency/quotes/latest", params={"id": id}) as response:
            data = await response.json()
            coin_data = data["data"][str(id)]
            return {
                "id": coin_data["id"],
                "name": coin_data["name"],
                "symbol": coin_data["symbol"],
                "price": coin_data["quote"]["USD"]["price"],
                "market_cap": coin_data["quote"]["USD"]["market_cap"],
                "percent_change_24h": coin_data["quote"]["USD"]["percent_change_24h"]
            }
