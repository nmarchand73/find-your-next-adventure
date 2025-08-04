from dataclasses import dataclass
from typing import Dict
from .coordinates import Coordinates

@dataclass
class ExtendedLinks:
    streetView: str = ""
    googleEarth: str = ""
    satelliteView: str = ""
    googleImages: str = ""
    openStreetMap: str = ""
    appleMaps: str = ""

@dataclass
class Destination:
    id: int
    location: str
    coordinates: Coordinates
    country: str
    region: str
    mainAttractionEn: str = ""
    mainAttractionFr: str = ""
    googleMapsLink: str = ""
    extendedLinks: ExtendedLinks = None
    
    def __post_init__(self):
        if self.extendedLinks is None:
            self.extendedLinks = ExtendedLinks()
