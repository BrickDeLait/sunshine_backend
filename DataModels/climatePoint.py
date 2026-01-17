from dataclasses import dataclass
from typing import List

@dataclass
class ClimateNormal:
    date: str
    temperature: float
    precipitation: float
    sunshine_duration: float

@dataclass
class ClimatePoint:
    latitude: float
    longitude: float
    climate_normals: List[ClimateNormal]