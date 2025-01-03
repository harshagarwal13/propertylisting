from typing import List, Dict
from .property_manager import Property


class PropertySearch:
    def __init__(self, properties: Dict[str, Property]):
        self.properties = properties

    def search_properties(self, criteria: dict) -> List[Property]:
        filtered = [
            prop for prop in self.properties.values()
            if (criteria.get("min_price") is None or prop.details["price"] >= criteria["min_price"])
               and (criteria.get("max_price") is None or prop.details["price"] <= criteria["max_price"])
               and (criteria.get("location") is None or prop.details["location"] == criteria["location"])
               and (criteria.get("property_type") is None or prop.details["property_type"] == criteria["property_type"])
               and prop.status == "available"
        ]
        return sorted(filtered, key=lambda x: x.timestamp, reverse=True)

    def shortlist_property(self, user_id: str, property_id: str, shortlist: Dict[str, List[str]]) -> bool:
        if property_id not in self.properties:
            return False

        if user_id not in shortlist:
            shortlist[user_id] = []

        if property_id in shortlist[user_id]:
            return False

        shortlist[user_id].append(property_id)
        return True

    def get_shortlisted(self, user_id: str, shortlist: Dict[str, List[str]]) -> List[Property]:
        property_ids = shortlist.get(user_id, [])
        shortlisted_properties = [self.properties[prop_id] for prop_id in property_ids if
                                  self.properties[prop_id].status == "available"]
        return sorted(shortlisted_properties, key=lambda x: x.timestamp, reverse=True)
