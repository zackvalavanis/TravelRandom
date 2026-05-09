from fastapi import FastAPI
from app.database import Base, engine
from app.routers.users import router as user_router
from app.routers.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS
from app.routers.trips import router as trips_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(trips_router)
