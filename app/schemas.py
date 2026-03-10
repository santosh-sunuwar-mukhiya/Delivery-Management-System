from pydantic import BaseModel, Field
from datetime import datetime
from app.databases.models import ShipmentStatus
from typing import Optional



class BaseShipment(BaseModel):
    content:str
    weight: float = Field(description="the weight of the item", le=25, ge=1)
    destination: int 

class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime 

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: Optional[ShipmentStatus]= Field(default=None)
    estimated_delivery: Optional[datetime] = Field(default=None)


