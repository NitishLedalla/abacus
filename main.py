from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import os


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

app = FastAPI(title="Abacus Service")

class NumberInput(BaseModel):
    number: int

@app.on_event("startup")
def init_sum():

    if not r.exists("running_sum"):
        r.set("running_sum", 0)

@app.post("/abacus/number")
def add_number(data: NumberInput):

    try:
        new_sum = r.incrby("running_sum", data.number)
        return {"sum": int(new_sum)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/abacus/sum")
def get_sum():

    try:
        value = r.get("running_sum")
        return {"sum": int(value) if value else 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/abacus/sum")
def reset_sum():

    try:
        r.set("running_sum", 0)
        return {"message": "Sum reset", "sum": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
