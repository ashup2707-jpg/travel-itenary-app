"""
Itinerary Builder MCP Tool Schema
Strict input/output schemas for Itinerary Builder MCP
"""
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class TimeWindow(BaseModel):
    """Time window for a day"""
    day: int = Field(..., description="Day number (1, 2, 3, etc.)")
    morning: Dict = Field(..., description="Morning time window: {start: ISO8601, end: ISO8601}")
    afternoon: Dict = Field(..., description="Afternoon time window: {start: ISO8601, end: ISO8601}")
    evening: Dict = Field(..., description="Evening time window: {start: ISO8601, end: ISO8601}")

class ItineraryBuilderInput(BaseModel):
    """Input schema for Itinerary Builder MCP"""
    pois: List[Dict] = Field(..., description="List of POIs from POI Search MCP")
    timeWindows: List[TimeWindow] = Field(..., description="Time windows for each day")
    constraints: Dict = Field(
        ...,
        description="Constraints: maxTravelTimePerDay (minutes), pace (relaxed/moderate/fast), preferences (dict)"
    )

class POIBlock(BaseModel):
    """POI in a time block"""
    poiId: str = Field(..., description="POI ID from POI Search MCP")
    name: str = Field(default="", description="POI name")
    category: str = Field(default="", description="POI category")
    arrivalTime: str = Field(..., description="Arrival time (ISO8601)")
    departureTime: str = Field(..., description="Departure time (ISO8601)")
    duration: int = Field(..., description="Duration in minutes")

class TimeBlock(BaseModel):
    """Time block (morning/afternoon/evening)"""
    time: Dict = Field(..., description="Time window: {start: ISO8601, end: ISO8601}")
    type: str = Field(..., description="Block type: 'morning', 'afternoon', or 'evening'")
    pois: List[POIBlock] = Field(..., description="POIs in this block")
    travelTime: int = Field(..., description="Total travel time in minutes")
    totalDuration: int = Field(..., description="Total duration of block in minutes")

class Day(BaseModel):
    """Day in itinerary"""
    day: int = Field(..., description="Day number")
    date: str = Field(..., description="Date (ISO8601)")
    blocks: List[TimeBlock] = Field(..., description="Time blocks for the day")
    totalTravelTime: int = Field(..., description="Total travel time for the day in minutes")
    feasibilityScore: float = Field(..., ge=0, le=1, description="Feasibility score (0-1)")

class Decision(BaseModel):
    """Reasoning for a decision"""
    poiId: str = Field(..., description="POI ID")
    reason: str = Field(..., description="Reason for including this POI")
    source: str = Field(..., description="Source citation URL")

class Reasoning(BaseModel):
    """Reasoning for itinerary"""
    decisions: List[Decision] = Field(..., description="Decisions made")
    warnings: List[str] = Field(default_factory=list, description="Warnings about the itinerary")

class Itinerary(BaseModel):
    """Itinerary structure"""
    days: List[Day] = Field(..., description="Days in the itinerary")

class ItineraryBuilderOutput(BaseModel):
    """Output schema for Itinerary Builder MCP"""
    itinerary: Itinerary = Field(..., description="Structured itinerary")
    reasoning: Reasoning = Field(..., description="Reasoning for decisions")
