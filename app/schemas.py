from pydantic import BaseModel, Field
from typing import Annotated, Optional
from random import randint
from enum import Enum

def random():
    return randint(1111, 1170)

class ShipmentStatus(str, Enum):
    placed=  "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class BaseShipment(BaseModel):
    content: Annotated[str, Field(min_length=3, max_length=25)]
    weight: float = Field(description="the weight of the item", le=25, ge=1)
    destination: Optional[int] = Field(default_factory=random)

class ShipmentRead(BaseShipment):
    status: ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    content: Optional[str] = Field(default=None)
    weight: Optional[float] = Field(le=25, default=None) 
    destination: Optional[int] = Field(default=None)
    status: ShipmentStatus


