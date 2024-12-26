from fastapi import FastAPI, APIRouter
from databaseEndpoints import db_router
import uvicorn

app = FastAPI()

app.include_router(db_router, prefix="")

if __name__ == "__main__":
    uvicorn.run("mainRouter:app", host="127.0.0.1", port=8000, reload=True)
    