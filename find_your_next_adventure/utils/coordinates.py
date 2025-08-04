"""Utility functions for coordinate operations."""

import math
from typing import Tuple, List

from find_your_next_adventure.models import Coordinates


def calculate_distance(coord1: Coordinates, coord2: Coordinates) -> float:
    """
    Calculate the great circle distance between two coordinates using the Haversine formula.
    
    Args:
        coord1: First coordinate point
        coord2: Second coordinate point
        
    Returns:
        Distance in kilometers
    """
    # Convert to radians
    lat1 = math.radians(coord1.latitude)
    lon1 = math.radians(coord1.longitude)
    lat2 = math.radians(coord2.latitude)
    lon2 = math.radians(coord2.longitude)
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth's radius in kilometers
    earth_radius = 6371.0
    
    return earth_radius * c


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validate that coordinates are within valid ranges.
    
    Args:
        latitude: Latitude value to validate
        longitude: Longitude value to validate
        
    Returns:
        True if coordinates are valid, False otherwise
    """
    return -90.0 <= latitude <= 90.0 and -180.0 <= longitude <= 180.0


def format_coordinates(coord: Coordinates, format_type: str = "decimal") -> str:
    """
    Format coordinates for display.
    
    Args:
        coord: Coordinates to format
        format_type: Format type ("decimal", "dms" for degrees/minutes/seconds)
        
    Returns:
        Formatted coordinate string
    """
    if format_type == "decimal":
        return f"{coord.latitude:.6f}°{coord.latitudeDirection}, {coord.longitude:.6f}°{coord.longitudeDirection}"
    elif format_type == "dms":
        lat_dms = decimal_to_dms(abs(coord.latitude))
        lon_dms = decimal_to_dms(abs(coord.longitude))
        return f"{lat_dms[0]}°{lat_dms[1]}'{lat_dms[2]:.2f}\"{coord.latitudeDirection}, {lon_dms[0]}°{lon_dms[1]}'{lon_dms[2]:.2f}\"{coord.longitudeDirection}"
    else:
        raise ValueError(f"Unknown format type: {format_type}")


def decimal_to_dms(decimal_degrees: float) -> Tuple[int, int, float]:
    """
    Convert decimal degrees to degrees, minutes, seconds.
    
    Args:
        decimal_degrees: Decimal degrees value
        
    Returns:
        Tuple of (degrees, minutes, seconds)
    """
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = ((decimal_degrees - degrees) * 60 - minutes) * 60
    return degrees, minutes, seconds


def get_coordinate_bounds(coordinates: List[Coordinates]) -> dict:
    """
    Get the bounding box for a list of coordinates.
    
    Args:
        coordinates: List of coordinate objects
        
    Returns:
        Dictionary with min/max lat/lon values
    """
    if not coordinates:
        return {}
    
    lats = [coord.latitude for coord in coordinates]
    lons = [coord.longitude for coord in coordinates]
    
    return {
        "min_latitude": min(lats),
        "max_latitude": max(lats),
        "min_longitude": min(lons),
        "max_longitude": max(lons),
        "center_latitude": sum(lats) / len(lats),
        "center_longitude": sum(lons) / len(lons)
    }
