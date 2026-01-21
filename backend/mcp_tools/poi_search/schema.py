"""
POI Search MCP Tool Schema
Strict input/output schemas for POI Search MCP
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class Budget(str, Enum):
    """Budget level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class POISearchInput(BaseModel):
    """Input schema for POI Search MCP"""
    city: str = Field(..., description="City name (e.g., 'Jaipur, India')")
    interests: List[str] = Field(..., max_items=10, description="List of interests (e.g., ['food', 'culture', 'history'])")
    constraints: Dict = Field(
        default_factory=dict,
        description="Constraints: maxDistance (km), accessibility (bool), budget (low/medium/high), indoorOnly (bool)"
    )
    timeWindow: Optional[Dict] = Field(
        None,
        description="Optional time window: {day: int, block: 'morning'|'afternoon'|'evening'}"
    )

class POI(BaseModel):
    """POI output schema"""
    id: str = Field(..., description="OSM ID (e.g., 'node/123456' or 'way/123456')")
    name: str = Field(..., description="POI name")
    category: str = Field(..., description="Category (e.g., 'tourism', 'amenity')")
    coordinates: Dict = Field(..., description="Coordinates: {lat: float, lon: float}")
    estimatedDuration: int = Field(..., description="Estimated visit duration in minutes")
    openingHours: Optional[str] = Field(None, description="Opening hours if available")
    source: str = Field(..., description="Source: 'osm' or 'wikivoyage'")
    metadata: Dict = Field(default_factory=dict, description="Additional metadata")

class POISearchOutput(BaseModel):
    """Output schema for POI Search MCP"""
    pois: List[POI] = Field(..., description="List of POIs")
    totalFound: int = Field(..., description="Total number of POIs found")
    queryTime: str = Field(..., description="Query timestamp in ISO8601 format")
