from pydantic import BaseModel, Field
from typing import Annotated

class Shipment(BaseModel):
    content: str = Field(min_length=3)
    weight: float = Field(lt=25)
    destination: int