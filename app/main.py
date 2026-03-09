from fastapi import FastAPI, HTTPException, status, Depends
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from sqlmodel import Session
from contextlib import asynccontextmanager
from .schemas import BaseShipment, ShipmentRead, ShipmentCreate, ShipmentUpdate
from enum import Enum
from app.databases.session import get_session, create_db_and_tables
from app.databases import crud
from app.databases.models import Shipment

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: cleanup if needed

app = FastAPI(lifespan=lifespan)

# shipments = {
#     12701: {"weight": 1, "content": "rubber ducks", "status": "placed"},
#     12702: {"weight": 2.3, "content": "magic wands", "status": "in_transit"},
#     12703: {"weight": 1.1, "content": "unicorn horns", "status": "delivered"},
#     12704: {"weight": 3.5, "content": "dragon eggs", "status": "in_transit"},
#     12705: {"weight": 1.9, "content": "wizard hats", "status": "out_for_delivery"},
# }

#get all the shipments.
@app.get("/", response_model=list[Shipment])
def get_all_shipments(session: Session = Depends(get_session)):
    return crud.get_all_shipments(session)

#get one shipment by ID.
@app.get("/shipment/{shipment_id}", response_model=Shipment)
def get_shipment(shipment_id: int, session: Session = Depends(get_session)) -> Shipment:
    shipment = crud.get_shipment_by_id(session, shipment_id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shipment with id {shipment_id} was not found.")
    return shipment

#post shipment using post method.
@app.post("/shipment", response_model=Shipment, status_code=status.HTTP_201_CREATED)
def submit_shipment(shipment: ShipmentCreate, session: Session = Depends(get_session)) -> Shipment:
    new_shipment = crud.create_shipment(session, shipment)
    return new_shipment

#update the shipment fields.
@app.patch("/shipment/{shipment_id}", response_model=Shipment)
def update_shipment(shipment_id: int, shipment: ShipmentUpdate, session: Session = Depends(get_session)):
    updated_shipment = crud.update_shipment(session, shipment_id, shipment)
    if updated_shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shipment with id {shipment_id} was not found.")
    return updated_shipment

#deleting the shipment with the help of shipment id.
@app.delete("/shipment/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment(shipment_id: int, session: Session = Depends(get_session)):
    deleted = crud.delete_shipment(session, shipment_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shipment with id {shipment_id} was not found.")
    return None


#scalar API documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API"
    )


