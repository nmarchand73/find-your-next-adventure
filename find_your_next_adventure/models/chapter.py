from dataclasses import dataclass
from typing import Dict, List
from .destination import Destination

@dataclass
class Chapter:
    title: str
    description: str
    latitudeRange: Dict[str, str]
    totalDestinations: int
    destinations: List[Destination]
    metadata: Dict[str, str]
