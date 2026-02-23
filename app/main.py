from fastapi import FastAPI
from . import shipment

app= FastAPI()

app.include_router(shipment.router)

@app.get("/")
def shipment():
    return {
        "title": "I am learning fastapi.",
        "content": "I am making a simple delivery app using fastapi."
    }