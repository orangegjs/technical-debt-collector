from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import entities.user_account   # register models
import entities.user_profile    # register models
import entities.fra_category    # register models
import entities.fra_activity    # register models
import entities.favourite       # register models
import entities.donation        # register models
import entities.report          # register models
from boundaries.user_account_routes import router
from boundaries.user_profile_routes import router as profile_router
from boundaries.fra_category_routes import router as category_router
from boundaries.fra_activity_routes import router as fra_router
from boundaries.favourite_routes import router as favourite_router
from boundaries.donation_routes  import router as donation_router
from boundaries.report_routes    import router as report_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="FundBridger API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://technical-debt-collector.vercel.app"],
    allow_origin_regex=r"https://technical-debt-collector.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(profile_router)
app.include_router(category_router)
app.include_router(fra_router)
app.include_router(favourite_router)
app.include_router(donation_router)
app.include_router(report_router)


@app.get("/")
def root():
    return {"message": "FundBridger API is running"}
