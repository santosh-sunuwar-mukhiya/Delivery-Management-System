from enum import Enum
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class ShipmentStatus(str, Enum):
    placed=  "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class Shipment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content : str 
    weight: float = Field(lt=25)
    destination: Optional[int] = None
    status: ShipmentStatus
    estimated_delivery: Optional[datetime] = None