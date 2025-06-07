from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from crypto import CryptoClient

app = FastAPI()

# CORS
origins = [settings.APP_URL]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup and shutdown
@app.on_event("startup")
async def startup_event():
    cmc_client = CryptoClient(
        base_url=settings.BASE_URL,
        api_key=settings.SECRET_KEY
    )
    await cmc_client.init()
    app.state.cmc_client = cmc_client

@app.on_event("shutdown")
async def shutdown_event():
    client = app.state.cmc_client
    if client:
        await client.close()

# Routes
@app.get("/cryptocurrencies")
async def get_list(request: Request):
    cmc_client = request.app.state.cmc_client
    return await cmc_client.get_all_data()

@app.get("/cryptocurrencies/{id}")
async def get_id(id: int, request: Request):
    cmc_client = request.app.state.cmc_client
    return await cmc_client.get_id_data(id)
