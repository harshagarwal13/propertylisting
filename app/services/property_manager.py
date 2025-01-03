from datetime import datetime
from typing import List, Dict


class Property:
    def __init__(self, property_id: str, user_id: str, details: dict):
        self.property_id = property_id
        self.user_id = user_id
        self.details = details
        self.status = "available"   # We can use an enum for this but to keep it simple for now we are using hardcoded string
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        return {
            "property_id": self.property_id,
            "user_id": self.user_id,
            "details": self.details,
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
        }


class PropertyManager:
    def __init__(self):
        self.properties: Dict[str, Property] = {}
        self.user_portfolios: Dict[str, List[str]] = {}

    def add_property(self, user_id: str, property_details: dict) -> str:
        property_id = f"prop-{len(self.properties) + 1}"
        new_property = Property(property_id, user_id, property_details)
        self.properties[property_id] = new_property
        if user_id not in self.user_portfolios:
            self.user_portfolios[user_id] = []
        self.user_portfolios[user_id].append(property_id)

        return property_id

    def update_property_status(self, property_id: str, status: str, user_id: str) -> bool:
        if property_id not in self.properties:
            return False

        property_obj = self.properties[property_id]
        if property_obj.user_id != user_id:
            return False

        property_obj.status = status
        return True

    def get_user_properties(self, user_id: str) -> List[Property]:
        property_ids = self.user_portfolios.get(user_id, [])
        user_properties = [self.properties[prop_id] for prop_id in property_ids]
        return sorted(user_properties, key=lambda x: x.timestamp, reverse=True)
