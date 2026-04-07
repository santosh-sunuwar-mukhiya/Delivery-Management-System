from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.base import BaseService


class ShipmentEventService(BaseService):
    def __init__(self, session):
        super().__init__(ShipmentEvent, session)  # type: ignore

    async def add(
        self,
        shipment: Shipment,
        location: int = None,  # type: ignore
        status: ShipmentStatus = None,  # type: ignore
        description: str = None,  # type: ignore
    ) -> ShipmentEvent:

        if not location or not status:
            last_event = await self.get_latest_event(shipment)
            location = location if location else last_event.location
            status = status if status else last_event.status

        new_event = ShipmentEvent(
            location=location,
            status=status,
            description=(
                description
                if description
                else self._generate_description(status, location)
            ),
            shipment_id=shipment.id,
        )  # type: ignore

        return await self._add(new_event)  # type: ignore

    async def get_latest_event(self, shipment: Shipment):
        timeline = shipment.timeline
        timeline.sort(key=lambda event: event.created_at)
        return timeline[-1]

    def _generate_description(self, status: ShipmentStatus, location: int):
        match status:
            case ShipmentStatus.placed:
                return "Assigned delivery partner."
            case ShipmentStatus.out_for_delivery:
                return "Shipment out for delivery."
            case ShipmentStatus.delivered:
                return "Successfully Delivered."
            case _:  # location in_transit
                return f"scanned at {location}"
