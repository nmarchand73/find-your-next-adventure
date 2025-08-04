"""Utility functions for generating map links."""

import re
import urllib.parse
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple, Union

from find_your_next_adventure.models.coordinates import Coordinates


class ImageSize(Enum):
    """Standard image sizes for various services"""

    SMALL = "400x400"
    MEDIUM = "640x640"
    LARGE = "800x800"
    XLARGE = "1024x1024"


class MapType(Enum):
    """Map types for different services"""

    ROADMAP = "roadmap"
    SATELLITE = "satellite"
    HYBRID = "hybrid"
    TERRAIN = "terrain"


def clean_location_name(location: str) -> str:
    """
    Clean and normalize location name for better search results

    Args:
        location: Raw location string

    Returns:
        Cleaned location string
    """
    # Remove common prefixes and suffixes
    location = re.sub(
        r"^(START IN|START AT|START WITH|NEAR|ALL OVER|ACROSS|INCLUDES)\s+",
        "",
        location,
        flags=re.IGNORECASE,
    )
    location = re.sub(
        r",?\s+(US|UK|USA|UNITED STATES|UNITED KINGDOM)$",
        "",
        location,
        flags=re.IGNORECASE,
    )

    # Clean up extra spaces and punctuation
    location = re.sub(r"\s+", " ", location)
    location = re.sub(r"[,;]+", ",", location)
    location = location.strip(" ,.-")

    return location


def generate_google_maps_link(location: str, coordinates: Coordinates) -> str:
    """
    Generate a Google Maps link for a given location and coordinates.

    Args:
        location: The location name
        coordinates: The Coordinates object with latitude and longitude

    Returns:
        A Google Maps URL string
    """
    # Use coordinates for precise location, with location name as query
    base_url = "https://www.google.com/maps/search/"

    # Create a search query that includes both location name and coordinates
    # This provides the best user experience - readable location name with precise coordinates
    query = f"{location}/@{coordinates.latitude},{coordinates.longitude}"
    encoded_query = urllib.parse.quote(query)

    # Add zoom level for better initial view (15 is good for city/landmark level)
    return f"{base_url}{encoded_query},15z"


def generate_openstreetmap_link(location: str, coordinates: Coordinates) -> str:
    """
    Generate an OpenStreetMap link for a given location and coordinates.

    Args:
        location: The location name
        coordinates: The Coordinates object with latitude and longitude

    Returns:
        An OpenStreetMap URL string
    """
    # OpenStreetMap format: https://www.openstreetmap.org/#map=zoom/lat/lon
    return f"https://www.openstreetmap.org/#map=15/{coordinates.latitude}/{coordinates.longitude}"


def generate_apple_maps_link(location: str, coordinates: Coordinates) -> str:
    """
    Generate an Apple Maps link for a given location and coordinates.

    Args:
        location: The location name
        coordinates: The Coordinates object with latitude and longitude

    Returns:
        An Apple Maps URL string
    """
    # Apple Maps format
    query = urllib.parse.quote(location)
    return f"https://maps.apple.com/?q={query}&ll={coordinates.latitude},{coordinates.longitude}"


def generate_google_street_view_link(
    location: str,
    coordinates: Coordinates,
    heading: int = 0,
    pitch: int = 0,
    fov: int = 90,
) -> str:
    """
    Generate Google Street View web link (no API key required)

    Args:
        location: Location name
        coordinates: Coordinates object
        heading: Camera heading (0-360 degrees)
        pitch: Camera pitch (-90 to 90 degrees)
        fov: Field of view (10-120 degrees)

    Returns:
        Google Street View web URL
    """
    lat, lng = coordinates.latitude, coordinates.longitude

    # Use Google Maps Street View web interface (no API key required)
    # Format: https://www.google.com/maps/@lat,lng,zoom,heading,tilt,fov
    zoom = "3a"  # Street View zoom level
    heading = heading % 360
    pitch = max(-90, min(90, pitch))
    fov = max(10, min(120, fov))

    return f"https://www.google.com/maps/@{lat},{lng},{zoom},{heading}y,{pitch}h,{fov}t/data=!3m1!1e3"


def generate_google_places_photo_link(location: str, coordinates: Coordinates) -> str:
    """
    Generate Google Places photo search link

    Args:
        location: Location name
        coordinates: Coordinates object

    Returns:
        Google Images search URL for the location
    """
    clean_location = clean_location_name(location)
    search_query = f"{clean_location} travel destination photography"
    encoded_query = urllib.parse.quote_plus(search_query)

    return f"https://www.google.com/search?q={encoded_query}&tbm=isch&tbs=sur:fmc"


def generate_static_map_alternatives(
    location: str, coordinates: Coordinates, zoom: int = 15
) -> Dict[str, str]:
    """
    Generate static map alternatives without API keys

    Args:
        location: Location name
        coordinates: Coordinates object
        zoom: Zoom level

    Returns:
        Dictionary of static map URLs from different providers
    """
    lat, lng = coordinates.latitude, coordinates.longitude

    return {
        "openstreetmap": f"https://www.openstreetmap.org/export/embed.html?bbox={lng-0.01},{lat-0.01},{lng+0.01},{lat+0.01}&layer=mapnik&marker={lat},{lng}",
        "mapquest": f"https://www.mapquest.com/latlng/{lat},{lng}?zoom={zoom}",
        "here_maps": f"https://wego.here.com/?map={lat},{lng},{zoom}",
        "yandex_maps": f"https://yandex.com/maps/?ll={lng},{lat}&z={zoom}&pt={lng},{lat}",
    }


def generate_google_earth_link(location: str, coordinates: Coordinates) -> str:
    """
    Generate Google Earth web link

    Args:
        location: Location name
        coordinates: Coordinates object

    Returns:
        Google Earth web URL
    """
    lat, lng = coordinates.latitude, coordinates.longitude

    # Google Earth web format
    return f"https://earth.google.com/web/@{lat},{lng},1000a,35y,0h,0t,0r"


def generate_satellite_view_links(
    location: str, coordinates: Coordinates
) -> Dict[str, str]:
    """
    Generate multiple satellite view links from different providers (no API keys)

    Args:
        location: Location name
        coordinates: Coordinates object

    Returns:
        Dictionary of satellite view URLs from different providers
    """
    lat, lng = coordinates.latitude, coordinates.longitude

    return {
        "google_satellite": f"https://www.google.com/maps/@{lat},{lng},1000m/data=!3m1!1e3",
        "google_earth_web": f"https://earth.google.com/web/@{lat},{lng},1000a,35y,0h,0t,0r",
        "bing_satellite": f"https://www.bing.com/maps?cp={lat}~{lng}&lvl=15&style=a",
        "yandex_satellite": f"https://yandex.com/maps/?ll={lng},{lat}&z=15&l=sat",
        "here_satellite": f"https://wego.here.com/?map={lat},{lng},15,satellite",
        "arcgis_satellite": f"https://www.arcgis.com/home/webmap/viewer.html?center={lng},{lat}&level=15&basemapId=World_Imagery",
        "nasa_worldview": f"https://worldview.earthdata.nasa.gov/?v={lng-1},{lat-1},{lng+1},{lat+1}&l=MODIS_Aqua_CorrectedReflectance_TrueColor",
    }


def generate_alternative_image_sources(
    location: str, coordinates: Coordinates
) -> Dict[str, str]:
    """
    Generate alternative image sources for the location

    Args:
        location: Location name
        coordinates: Coordinates object

    Returns:
        Dictionary of alternative image source URLs
    """
    clean_location = clean_location_name(location)
    encoded_location = urllib.parse.quote_plus(clean_location)

    return {
        "unsplash": f"https://unsplash.com/s/photos/{encoded_location}",
        "pixabay": f"https://pixabay.com/images/search/{encoded_location}/",
        "pexels": f"https://www.pexels.com/search/{encoded_location}/",
        "flickr": f"https://www.flickr.com/search/?text={encoded_location}",
        "wikimedia": f"https://commons.wikimedia.org/w/index.php?search={encoded_location}&title=Special:MediaSearch&go=Go&type=image",
        "getty_images": f"https://www.gettyimages.com/photos/{encoded_location}",
        "shutterstock": f"https://www.shutterstock.com/search/{encoded_location}",
    }


def generate_panoramic_links(location: str, coordinates: Coordinates) -> Dict[str, str]:
    """
    Generate panoramic and 360° view links (no API keys required)

    Args:
        location: Location name
        coordinates: Coordinates object

    Returns:
        Dictionary of panoramic view URLs
    """
    lat, lng = coordinates.latitude, coordinates.longitude
    clean_location = clean_location_name(location)
    encoded_location = urllib.parse.quote_plus(clean_location)

    return {
        "google_street_view": generate_google_street_view_link(
            location, coordinates, fov=120
        ),
        "mapillary": f"https://www.mapillary.com/app/?lat={lat}&lng={lng}&z=17",
        "round_me": f"https://round.me/search?q={encoded_location}",
        "street_view_360": f"https://www.google.com/maps/@{lat},{lng},3a,75y,0h,90t/data=!3m7!1e1!3m5!1s-!2e0!6s%2F%2Fgeo0.ggpht.com",
        "instant_street_view": f"https://www.instantstreetview.com/@{lat},{lng},0h,5p,1z",
    }


def generate_location_image_links(
    location: str,
    coordinates: Coordinates,
    custom_zoom: int = 15,
    detailed_view: bool = True,
) -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Generate comprehensive image-related links for a location (no API keys required).

    Args:
        location: The location name
        coordinates: The Coordinates object with latitude and longitude
        custom_zoom: Custom zoom level for maps
        detailed_view: Whether to include detailed alternative sources

    Returns:
        Dictionary containing various image links categorized by type
    """
    # Validate inputs
    if not location or not location.strip():
        raise ValueError("Location cannot be empty")

    if not isinstance(coordinates, Coordinates):
        raise TypeError("Coordinates must be a Coordinates object")

    lat, lng = coordinates.latitude, coordinates.longitude

    # Generate all link categories
    result = {
        # Primary map and street view links (no API keys)
        "primary": {
            "street_view": generate_google_street_view_link(location, coordinates),
            "google_maps": f"https://maps.google.com/?q={lat},{lng}&z={custom_zoom}",
            "google_earth": generate_google_earth_link(location, coordinates),
            "satellite_view": f"https://www.google.com/maps/@{lat},{lng},1000m/data=!3m1!1e3",
        },
        # Multiple satellite providers (no API keys)
        "satellite_views": generate_satellite_view_links(location, coordinates),
        # Static map alternatives (no API keys)
        "static_maps": generate_static_map_alternatives(
            location, coordinates, custom_zoom
        ),
        # Photo search engines
        "photo_search": {
            "google_images": generate_google_places_photo_link(location, coordinates),
        },
        # Interactive maps from different providers
        "interactive_maps": {
            "google_maps": f"https://maps.google.com/?q={lat},{lng}&z={custom_zoom}",
            "openstreetmap": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lng}&zoom={custom_zoom}",
            "apple_maps": f"https://maps.apple.com/?ll={lat},{lng}&z={custom_zoom}",
            "bing_maps": f"https://www.bing.com/maps?cp={lat}~{lng}&lvl={custom_zoom}",
            "yandex_maps": f"https://yandex.com/maps/?ll={lng},{lat}&z={custom_zoom}",
            "here_maps": f"https://wego.here.com/?map={lat},{lng},{custom_zoom}",
        },
        # Metadata
        "metadata": {
            "location_cleaned": clean_location_name(location),
            "coordinates_dms": f"{abs(coordinates.latitude):.4f}°{coordinates.latitudeDirection}, {abs(coordinates.longitude):.4f}°{coordinates.longitudeDirection}",
            "coordinates_decimal": (coordinates.latitude, coordinates.longitude),
            "generation_timestamp": __import__("datetime").datetime.now().isoformat(),
        },
    }

    # Add detailed sources if requested
    if detailed_view:
        result.update(
            {
                # Alternative image sources
                "stock_photos": generate_alternative_image_sources(
                    location, coordinates
                ),
                # Panoramic and 360° views
                "panoramic": generate_panoramic_links(location, coordinates),
            }
        )

    return result


def generate_extended_links(location: str, coordinates: Coordinates) -> Dict[str, str]:
    """
    Generate extended links for a destination including street view, satellite view,
    Google Earth, Google Images, OpenStreetMap, and Apple Maps.

    Args:
        location: The location name
        coordinates: The Coordinates object with latitude and longitude

    Returns:
        Dictionary with all extended links
    """
    lat, lng = coordinates.latitude, coordinates.longitude
    clean_location = clean_location_name(location)

    return {
        "streetView": generate_google_street_view_link(location, coordinates),
        "googleEarth": f"https://earth.google.com/web/@{lat},{lng},1000a,35y,0h,0t,0r",
        "satelliteView": f"https://www.google.com/maps/@{lat},{lng},1000m/data=!3m1!1e3",
        "googleImages": generate_google_places_photo_link(location, coordinates),
        "openStreetMap": generate_openstreetmap_link(location, coordinates),
        "appleMaps": generate_apple_maps_link(location, coordinates),
    }
