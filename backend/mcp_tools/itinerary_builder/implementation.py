"""
Itinerary Builder MCP Implementation
Builds structured day-wise itineraries from POIs
"""
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict
from geopy.distance import geodesic

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mcp_tools.itinerary_builder.schema import (
    ItineraryBuilderInput, ItineraryBuilderOutput,
    TimeWindow, Day, TimeBlock, POIBlock, Reasoning, Decision, Itinerary
)

class ItineraryBuilderMCP:
    """
    Itinerary Builder MCP Tool
    Builds structured day-wise itineraries from candidate POIs
    """
    
    def __init__(self):
        pass
    
    def build(
        self,
        input_data: ItineraryBuilderInput
    ) -> ItineraryBuilderOutput:
        """
        Build itinerary from POIs and time windows
        
        Args:
            input_data: ItineraryBuilderInput with POIs, time windows, constraints
        
        Returns:
            ItineraryBuilderOutput with structured itinerary
        """
        pois = input_data.pois
        time_windows = input_data.timeWindows
        constraints = input_data.constraints
        
        pace = constraints.get('pace', 'moderate')
        max_travel_time = constraints.get('maxTravelTimePerDay', 120)  # minutes
        
        # Build itinerary days
        days = []
        decisions = []
        warnings = []
        
        poi_index = 0
        total_pois = len(pois)
        
        print(f"   📍 Building itinerary with {total_pois} POIs for {len(time_windows)} days")
        
        for time_window in time_windows:
            day_num = time_window.day
            
            # Calculate available time for each block
            morning_start = datetime.fromisoformat(time_window.morning['start'])
            morning_end = datetime.fromisoformat(time_window.morning['end'])
            afternoon_start = datetime.fromisoformat(time_window.afternoon['start'])
            afternoon_end = datetime.fromisoformat(time_window.afternoon['end'])
            evening_start = datetime.fromisoformat(time_window.evening['start'])
            evening_end = datetime.fromisoformat(time_window.evening['end'])
            
            morning_duration = (morning_end - morning_start).total_seconds() / 60
            afternoon_duration = (afternoon_end - afternoon_start).total_seconds() / 60
            evening_duration = (evening_end - evening_start).total_seconds() / 60
            
            # Build blocks
            blocks = []
            total_travel_time = 0
            current_time = morning_start
            
            # Morning block
            morning_pois = self._assign_pois_to_block(
                pois[poi_index:],
                current_time,
                morning_duration,
                pace,
                max_travel_time
            )
            poi_index += len(morning_pois['pois'])
            blocks.append(morning_pois['block'])
            total_travel_time += morning_pois['travel_time']
            current_time = morning_pois['end_time']
            
            # Afternoon block
            afternoon_pois = self._assign_pois_to_block(
                pois[poi_index:],
                current_time,
                afternoon_duration,
                pace,
                max_travel_time - total_travel_time
            )
            poi_index += len(afternoon_pois['pois'])
            blocks.append(afternoon_pois['block'])
            total_travel_time += afternoon_pois['travel_time']
            current_time = afternoon_pois['end_time']
            
            # Evening block
            evening_pois = self._assign_pois_to_block(
                pois[poi_index:],
                current_time,
                evening_duration,
                pace,
                max_travel_time - total_travel_time
            )
            poi_index += len(evening_pois['pois'])
            blocks.append(evening_pois['block'])
            total_travel_time += evening_pois['travel_time']
            
            # Calculate feasibility score
            feasibility_score = self._calculate_feasibility_score(
                blocks, total_travel_time, max_travel_time
            )
            
            if feasibility_score < 0.7:
                warnings.append(f"Day {day_num} has high travel time ratio")
            
            # Create day
            day = Day(
                day=day_num,
                date=time_window.morning['start'].split('T')[0],
                blocks=blocks,
                totalTravelTime=int(total_travel_time),
                feasibilityScore=feasibility_score
            )
            days.append(day)
            
            # Log day creation
            total_pois_in_day = sum(len(block.pois) for block in blocks)
            print(f"   ✅ Day {day_num}: {total_pois_in_day} POIs, {len(blocks)} blocks, {poi_index}/{total_pois} POIs used")
            
            # Warn if running low on POIs
            if poi_index >= total_pois and day_num < len(time_windows):
                print(f"   ⚠️  Warning: Running out of POIs! Only {total_pois} POIs for {len(time_windows)} days")
            
            # Add decisions
            for block in blocks:
                for poi_block in block.pois:
                    decisions.append(Decision(
                        poiId=poi_block.poiId,
                        reason=f"Included in {block.type} block based on interests and constraints",
                        source="osm"
                    ))
        
        # Create itinerary
        itinerary = Itinerary(days=days)
        
        # Create reasoning
        reasoning = Reasoning(
            decisions=decisions,
            warnings=warnings
        )
        
        return ItineraryBuilderOutput(
            itinerary=itinerary,
            reasoning=reasoning
        )
    
    def _assign_pois_to_block(
        self,
        available_pois: List[Dict],
        start_time: datetime,
        block_duration: float,
        pace: str,
        max_travel_time: float
    ) -> Dict:
        """Assign POIs to a time block"""
        block_pois = []
        current_time = start_time
        total_travel_time = 0
        
        # Adjust POI count based on pace
        if pace == 'relaxed':
            max_pois = 1
        elif pace == 'moderate':
            max_pois = 2
        else:  # fast
            max_pois = 3
        
        prev_coords = None
        
        for poi in available_pois[:max_pois]:
            # Calculate travel time
            travel_time = 0
            if prev_coords:
                poi_coords = (
                    poi['coordinates']['lat'],
                    poi['coordinates']['lon']
                )
                distance_km = geodesic(prev_coords, poi_coords).kilometers
                travel_time = int(distance_km * 2)  # ~2 min per km (heuristic)
            
            if total_travel_time + travel_time > max_travel_time:
                break
            
            # POI duration
            poi_duration = poi.get('estimatedDuration', 60)
            
            # Check if fits in block
            if (current_time - start_time).total_seconds() / 60 + travel_time + poi_duration > block_duration:
                break
            
            # Add POI
            arrival = current_time + timedelta(minutes=travel_time)
            departure = arrival + timedelta(minutes=poi_duration)
            
            block_pois.append(POIBlock(
                poiId=poi['id'],
                name=poi.get('name', 'Unknown'),
                category=poi.get('category', ''),
                arrivalTime=arrival.isoformat(),
                departureTime=departure.isoformat(),
                duration=poi_duration
            ))
            
            current_time = departure
            total_travel_time += travel_time
            prev_coords = (poi['coordinates']['lat'], poi['coordinates']['lon'])
        
        # Determine block type from start time
        hour = start_time.hour
        if hour < 12:
            block_type = 'morning'
        elif hour < 17:
            block_type = 'afternoon'
        else:
            block_type = 'evening'
        
        block = TimeBlock(
            time={
                'start': start_time.isoformat(),
                'end': current_time.isoformat()
            },
            type=block_type,
            pois=block_pois,
            travelTime=int(total_travel_time),
            totalDuration=int((current_time - start_time).total_seconds() / 60)
        )
        
        return {
            'block': block,
            'pois': block_pois,
            'travel_time': total_travel_time,
            'end_time': current_time
        }
    
    def _calculate_feasibility_score(
        self,
        blocks: List[TimeBlock],
        total_travel_time: float,
        max_travel_time: float
    ) -> float:
        """Calculate feasibility score (0-1)"""
        # Base score
        score = 1.0
        
        # Penalize if travel time exceeds limit
        if total_travel_time > max_travel_time:
            score -= 0.3
        
        # Penalize if travel time is > 40% of total time
        total_duration = sum(block.totalDuration for block in blocks)
        if total_duration > 0:
            travel_ratio = total_travel_time / total_duration
            if travel_ratio > 0.4:
                score -= 0.2
        
        return max(0.0, min(1.0, score))


# Test function
if __name__ == "__main__":
    from mcp_tools.poi_search.implementation import POISearchMCP
    from mcp_tools.poi_search.schema import POISearchInput
    
    print("🔍 Testing Itinerary Builder MCP...")
    
    # First, get some POIs
    poi_search = POISearchMCP(use_mock=True)
    poi_input = POISearchInput(
        city="Jaipur, India",
        interests=["culture", "history"],
        constraints={}
    )
    poi_results = poi_search.search(poi_input)
    
    print(f"✅ Got {len(poi_results.pois)} POIs from POI Search")
    
    # Convert POIs to dict format (use model_dump for Pydantic v2)
    try:
        pois_dict = [poi.model_dump() for poi in poi_results.pois]
    except AttributeError:
        # Fallback for older Pydantic versions
        pois_dict = [poi.dict() for poi in poi_results.pois]
    
    # Create time windows (3 days)
    from datetime import datetime, timedelta
    base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    time_windows = []
    for day in range(1, 4):
        day_date = base_date + timedelta(days=day-1)
        time_windows.append(TimeWindow(
            day=day,
            morning={
                'start': (day_date.replace(hour=9)).isoformat(),
                'end': (day_date.replace(hour=12)).isoformat()
            },
            afternoon={
                'start': (day_date.replace(hour=13)).isoformat(),
                'end': (day_date.replace(hour=17)).isoformat()
            },
            evening={
                'start': (day_date.replace(hour=18)).isoformat(),
                'end': (day_date.replace(hour=21)).isoformat()
            }
        ))
    
    # Build itinerary
    builder = ItineraryBuilderMCP()
    itinerary_input = ItineraryBuilderInput(
        pois=pois_dict,
        timeWindows=time_windows,
        constraints={
            'maxTravelTimePerDay': 120,
            'pace': 'moderate',
            'preferences': {}
        }
    )
    
    result = builder.build(itinerary_input)
    
    print(f"\n✅ Built itinerary with {len(result.itinerary.days)} days")
    print(f"📋 Decisions: {len(result.reasoning.decisions)}")
    print(f"⚠️  Warnings: {len(result.reasoning.warnings)}")
    
    for day in result.itinerary.days:
        print(f"\n📅 Day {day.day} ({day.date})")
        print(f"   Feasibility: {day.feasibilityScore:.2f}")
        print(f"   Travel time: {day.totalTravelTime} minutes")
        for block in day.blocks:
            print(f"   {block.type.capitalize()}: {len(block.pois)} POIs, {block.totalDuration} min")
