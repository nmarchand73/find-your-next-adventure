"""Tests for data models."""

from dataclasses import asdict

import pytest

from find_your_next_adventure.models import Chapter, Coordinates, Destination


class TestCoordinates:
    """Test cases for Coordinates model."""

    def test_coordinates_creation(self, sample_coordinates):
        """Test basic coordinates creation."""
        assert sample_coordinates.latitude == 59.9139
        assert sample_coordinates.longitude == 10.7522
        assert sample_coordinates.latitudeDirection == "N"
        assert sample_coordinates.longitudeDirection == "E"

    def test_coordinates_to_dict(self, sample_coordinates):
        """Test coordinates serialization."""
        coord_dict = asdict(sample_coordinates)
        expected = {
            "latitude": 59.9139,
            "longitude": 10.7522,
            "latitudeDirection": "N",
            "longitudeDirection": "E",
        }
        assert coord_dict == expected


class TestDestination:
    """Test cases for Destination model."""

    def test_destination_creation(self, sample_destination):
        """Test basic destination creation."""
        assert sample_destination.id == 1
        assert sample_destination.location == "Oslo, Norway"
        assert sample_destination.country == "Norway"
        assert sample_destination.region == "Scandinavia"
        assert isinstance(sample_destination.coordinates, Coordinates)

    def test_destination_to_dict(self, sample_destination):
        """Test destination serialization."""
        dest_dict = asdict(sample_destination)
        assert dest_dict["id"] == 1
        assert dest_dict["location"] == "Oslo, Norway"
        assert dest_dict["country"] == "Norway"
        assert dest_dict["region"] == "Scandinavia"
        assert "coordinates" in dest_dict
        assert isinstance(dest_dict["coordinates"], dict)


class TestChapter:
    """Test cases for Chapter model."""

    def test_chapter_creation(self, sample_chapter):
        """Test basic chapter creation."""
        assert sample_chapter.title == "Test Chapter"
        assert sample_chapter.description == "A test chapter"
        assert sample_chapter.totalDestinations == 1
        assert len(sample_chapter.destinations) == 1
        assert isinstance(sample_chapter.destinations[0], Destination)

    def test_chapter_to_dict(self, sample_chapter):
        """Test chapter serialization."""
        chapter_dict = asdict(sample_chapter)
        assert chapter_dict["title"] == "Test Chapter"
        assert chapter_dict["totalDestinations"] == 1
        assert len(chapter_dict["destinations"]) == 1
        assert "metadata" in chapter_dict
