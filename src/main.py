from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Settings

settings = Settings()


app = FastAPI(
    title="25-1-KeYThon-2 API",
    description="This is just a simple API server for KeYThon.",
    version="0.1.0",
)

origins = [
    "https://localhost:8000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#app.include_router(content_router)


@app.get("/")
async def root():
    return {"message": "KeYThon 2조의 API 서버입니다."}
