"""Test configuration and fixtures."""

import pytest
from pathlib import Path
from find_your_next_adventure.models import Coordinates, Destination, Chapter


@pytest.fixture
def sample_coordinates():
    """Sample coordinates for testing."""
    return Coordinates(
        latitude=59.9139,
        longitude=10.7522,
        latitudeDirection="N",
        longitudeDirection="E"
    )


@pytest.fixture
def sample_destination(sample_coordinates):
    """Sample destination for testing."""
    return Destination(
        id=1,
        location="Oslo, Norway",
        coordinates=sample_coordinates,
        country="Norway",
        region="Scandinavia"
    )


@pytest.fixture
def sample_chapter(sample_destination):
    """Sample chapter for testing."""
    return Chapter(
        title="Test Chapter",
        description="A test chapter",
        latitudeRange={"from": "60° North", "to": "45° North"},
        totalDestinations=1,
        destinations=[sample_destination],
        metadata={
            "source": "Test Guide",
            "chapter": "1",
            "generatedDate": "2025-08-01",
            "coordinateSystem": "WGS84",
            "format": "Decimal Degrees"
        }
    )


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory for testing."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


@pytest.fixture
def sample_pdf_content():
    """Sample PDF content for testing parser."""
    return """
1. Oslo, Norway - Latitude: 59.9139 N Longitude: 10.7522 E
2. Stockholm, Sweden - Latitude: 59.3293 N Longitude: 18.0686 E
3. Copenhagen, Denmark - Latitude: 55.6761 N Longitude: 12.5683 E
    """
