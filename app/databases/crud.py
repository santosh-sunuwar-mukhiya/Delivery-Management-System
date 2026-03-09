from sqlmodel import Session, select
from typing import Optional
from .models import Shipment, ShipmentStatus
from ..schemas import ShipmentCreate, ShipmentUpdate
from datetime import datetime, timedelta

def create_shipment(session: Session, shipment: ShipmentCreate) -> Shipment:
    """Create a new shipment"""
    # Calculate estimated delivery (e.g., 5 days from now)
    estimated_delivery = datetime.now() + timedelta(days=5)
    
    db_shipment = Shipment(
        content=shipment.content,
        weight=shipment.weight,
        destination=shipment.destination,
        status=ShipmentStatus.placed,
        estimated_delivery=estimated_delivery
    )
    session.add(db_shipment)
    session.commit()
    session.refresh(db_shipment)
    return db_shipment

def get_shipment_by_id(session: Session, shipment_id: int) -> Optional[Shipment]:
    """Get a shipment by ID"""
    return session.get(Shipment, shipment_id)

def get_all_shipments(session: Session) -> list[Shipment]:
    """Get all shipments"""
    statement = select(Shipment)
    results = session.exec(statement).all()
    return list(results)

def update_shipment(session: Session, shipment_id: int, shipment_update: ShipmentUpdate) -> Optional[Shipment]:
    """Update a shipment"""
    db_shipment = session.get(Shipment, shipment_id)
    if not db_shipment:
        return None
    
    update_data = shipment_update.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(db_shipment, key, value)
    
    session.add(db_shipment)
    session.commit()
    session.refresh(db_shipment)
    return db_shipment

def delete_shipment(session: Session, shipment_id: int) -> bool:
    """Delete a shipment"""
    db_shipment = session.get(Shipment, shipment_id)
    if not db_shipment:
        return False
    
    session.delete(db_shipment)
    session.commit()
    return True
