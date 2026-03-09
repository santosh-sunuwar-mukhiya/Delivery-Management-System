from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from .schemas import BaseShipment, ShipmentRead, ShipmentCreate, ShipmentUpdate
from enum import Enum
from app.database import Database

app = FastAPI()

db = Database()

# shipments = {
#     12701: {"weight": 1, "content": "rubber ducks", "status": "placed"},
#     12702: {"weight": 2.3, "content": "magic wands", "status": "in_transit"},
#     12703: {"weight": 1.1, "content": "unicorn horns", "status": "delivered"},
#     12704: {"weight": 3.5, "content": "dragon eggs", "status": "in_transit"},
#     12705: {"weight": 1.9, "content": "wizard hats", "status": "out_for_delivery"},
# }

#get all the post.
@app.get("/", response_model=None)
def get_all_shipments():
    return db.get_all()

#get one shipment with ID and field using query parameter and path parameter.
@app.get("/shipment/{field}", response_model=dict[str, Any])
def get_shipment_field( id: int) -> dict[str, Any]:
    shipment = db.get_by_id(id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with {id} was not found.")
    return shipment

#post shipment with Id using post method.
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = db.create(shipment)
    return {"new data": new_id}

#update the field of shipment.
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate):
    print("#"*20)
    print(shipment)
    print("#"*20)
    updated_shipment = db.update(id, shipment)
    return updated_shipment

#deleting the shipment with the help of shipment id.
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete(id)
    return {"data": f"shipment with id {id} is deleted."}


#scalar API documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )


