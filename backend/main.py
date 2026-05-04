from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import entities.user_account   # register models
import entities.user_profile    # register models
from boundaries.user_account_routes import router
from boundaries.user_profile_routes import router as profile_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="FundBridger API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://technical-debt-collector.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(profile_router)


@app.get("/")
def root():
    return {"message": "FundBridger API is running"}
