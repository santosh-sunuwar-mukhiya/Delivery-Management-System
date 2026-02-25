from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from .schemas import Shipment

app = FastAPI()

shipments = {
    12701: {"weight": 0.6, "content": "rubber ducks", "status": "placed"},
    12702: {"weight": 2.3, "content": "magic wands", "status": "shipped"},
    12703: {"weight": 1.1, "content": "unicorn horns", "status": "delivered"},
    12704: {"weight": 3.5, "content": "dragon eggs", "status": "in transit"},
    12705: {"weight": 0.9, "content": "wizard hats", "status": "returned"},
}

#get all the post.
@app.get("/")
def get_all_shipments():
    return shipments

#get one shipment with ID and field using query parameter and path parameter.
@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with {id} was not found.")
    return {
        field: shipments[id][field]
    }

#post shipment with Id using post method.
@app.post("/shipment")
def submit_shipment(shipment: Shipment) -> dict[str, Any]:
    if shipment.weight > 25:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The must be less than 25 Kg")
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "weight": shipment.weight,
        "content": shipment.content,
        "status":"placed"
    }

    return {"new data": new_id}

#update the field of shipment.
@app.patch("/shipment")
def update_shipment(id: int, body: dict[str, Any]) -> dict[str, Any]:
    shipments[id].update(body)
    return shipments[id]

#deleting the shipment with the help of shipment id.
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)
    return {"data": f"shipment with id {id} is deleted."}


#scalar API documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )


