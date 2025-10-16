from fastapi import FastAPI
from pydantic import BaseModel
from threading import Lock

app = FastAPI(title="Abacus Service")

# simple shared sum variable and lock for thread safety
running_sum = 0
sum_lock = Lock()

class NumberInput(BaseModel):
    number: int

@app.post("/abacus/number")
def add_number(data: NumberInput):
    global running_sum
    with sum_lock:
        running_sum += data.number
        current = running_sum
    return {"sum": current}

@app.get("/abacus/sum")
def get_sum():
    return {"sum": running_sum}

@app.delete("/abacus/sum")
def reset_sum():
    global running_sum
    with sum_lock:
        running_sum = 0
    return {"message": "Sum reset", "sum": running_sum}
