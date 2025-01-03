from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from .services.property_manager import PropertyManager
from .services.property_search import PropertySearch

app = FastAPI()

# Initialize services
property_manager = PropertyManager()
property_search = PropertySearch(property_manager.properties)


class PropertyCreate(BaseModel):
    location: str
    price: float
    property_type: str
    description: str
    amenities: List[str]


@app.post("/api/v1/properties")
async def create_property(
        property_data: PropertyCreate,
        current_user: str = Depends(lambda: "test_user")  # Mock user dependency
):
    try:
        # Validate and add the property
        property_id = property_manager.add_property(current_user, property_data.dict())
        if not property_id:
            raise HTTPException(status_code=400, detail="Property creation failed.")
        return {"property_id": property_id}
    # Added exception for HTTP and ValueError
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Handle validation errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/api/v1/properties/search")
async def search_properties(
        min_price: Optional[float] = Query(None, ge=0),
        max_price: Optional[float] = Query(None, ge=0),
        location: Optional[str] = None,
        property_type: Optional[str] = None,
        page: int = Query(1, ge=1), #Default value is page=1
        limit: int = Query(10, ge=1, le=100) #Added minimum value=1 and maximum value to 100
):
    try:
        criteria = {
            "min_price": min_price,
            "max_price": max_price,
            "location": location,
            "property_type": property_type,
        }

        # Call to the search service
        results = property_search.search_properties(criteria)
        if not results:
            raise HTTPException(status_code=404, detail="No properties found matching the criteria.")

        total_count = len(results)
        start = (page - 1) * limit
        end = start + limit
        paginated = results[start:end]

        return {
            "total_count": total_count,
            "properties": [prop.to_dict() for prop in paginated],
            "page": page,
            "limit": limit,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Handle validation errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
