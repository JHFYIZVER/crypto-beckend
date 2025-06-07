from config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crypto import CryptoClient

cmc_client = CryptoClient(
    base_url=settings.BASE_URL,
    api_key=settings.SECRET_KEY
)

app = FastAPI()

origins = [
    settings.APP_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/cryptocurrencies")
async def get_list():
    return await cmc_client.get_all_data()


@app.get("/cryptocurrencies/{id}")
async def get_id(id: int):
    return await cmc_client.get_id_data(id)

