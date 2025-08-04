"""Tests for the adventure guide parser."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from find_your_next_adventure.models import Coordinates, Destination
from find_your_next_adventure.parsers import AdventureGuideParser


class TestAdventureGuideParser:
    """Test cases for AdventureGuideParser."""

    def test_parser_initialization(self):
        """Test parser initialization."""
        parser = AdventureGuideParser()
        assert parser.stats["processed"] == 0
        assert parser.stats["successful"] == 0
        assert parser.stats["failed"] == 0
        assert parser.stats["unknown_countries"] == 0
        assert parser.failed_lines == []

    def test_clean_location(self):
        """Test location cleaning functionality."""
        parser = AdventureGuideParser()

        # Test basic cleaning
        assert parser.clean_location("  OSLO,  NORWAY  ") == "OSLO, NORWAY"

        # Test corrections
        assert parser.clean_location("SOLVENIA") == "SLOVENIA"
        assert parser.clean_location("PAPAU NEW GUINEA") == "PAPUA NEW GUINEA"
        assert parser.clean_location("TAJIKSTAN") == "TAJIKISTAN"

    def test_parse_coordinates(self):
        """Test coordinate parsing."""
        parser = AdventureGuideParser()

        # Test positive coordinates
        coords = parser.parse_coordinates("59.9139", "N", "10.7522", "E")
        assert coords.latitude == 59.9139
        assert coords.longitude == 10.7522
        assert coords.latitudeDirection == "N"
        assert coords.longitudeDirection == "E"

        # Test negative coordinates
        coords = parser.parse_coordinates("33.4484", "S", "70.6693", "W")
        assert coords.latitude == -33.4484
        assert coords.longitude == -70.6693
        assert coords.latitudeDirection == "S"
        assert coords.longitudeDirection == "W"

    def test_identify_country_region(self):
        """Test country and region identification."""
        parser = AdventureGuideParser()

        # Test known countries
        country, region = parser.identify_country_region("OSLO, NORWAY")
        assert country == "Norway"
        assert region == "Scandinavia"

        # Test special cases
        country, region = parser.identify_country_region("GEOGRAPHICAL NORTH POLE")
        assert country == "Arctic"
        assert region == "North Pole"

        # Test unknown location
        country, region = parser.identify_country_region("UNKNOWN PLACE")
        assert country == "Unknown"
        assert region == "Unknown"

    def test_parse_line_success(self):
        """Test successful line parsing."""
        parser = AdventureGuideParser()
        line = "1. Oslo, Norway - Latitude: 59.9139 N Longitude: 10.7522 E"

        destination = parser.parse_line(line)

        assert destination is not None
        assert destination.id == 1
        assert destination.location == "Oslo, Norway"
        assert destination.country == "Norway"
        assert destination.region == "Scandinavia"
        assert destination.coordinates.latitude == 59.9139
        assert destination.coordinates.longitude == 10.7522

    def test_parse_line_failure(self):
        """Test line parsing failure cases."""
        parser = AdventureGuideParser()

        # Test invalid format
        destination = parser.parse_line("Invalid line format")
        assert destination is None
        assert parser.stats["failed"] == 1

        # Test invalid coordinates
        destination = parser.parse_line("1. Test - Latitude: 999.0 N Longitude: 10.0 E")
        assert destination is None
        assert parser.stats["failed"] == 2

    @patch("find_your_next_adventure.parsers.adventure_guide_parser.fitz")
    def test_load_pdf_success(self, mock_fitz):
        """Test successful PDF loading."""
        # Mock fitz document
        mock_doc = Mock()
        mock_page = Mock()
        mock_page.get_text.return_value = "Sample text"
        mock_doc.__iter__ = Mock(return_value=iter([mock_page]))
        mock_doc.close = Mock()
        mock_fitz.open.return_value = mock_doc

        parser = AdventureGuideParser()
        content = parser.load_pdf(Path("test.pdf"))

        assert content == "Sample text\n"
        mock_fitz.open.assert_called_once_with(Path("test.pdf"))
        mock_doc.close.assert_called_once()

    @patch("find_your_next_adventure.parsers.adventure_guide_parser.fitz")
    def test_load_pdf_failure(self, mock_fitz):
        """Test PDF loading failure."""
        mock_fitz.open.side_effect = Exception("File not found")

        parser = AdventureGuideParser()
        content = parser.load_pdf(Path("nonexistent.pdf"))

        assert content == ""

    def test_parse_pdf_content(self, sample_pdf_content):
        """Test PDF content parsing."""
        parser = AdventureGuideParser()
        chapters_data = parser.parse_pdf_content(sample_pdf_content)

        # Should have 8 chapters
        assert len(chapters_data) == 8

        # Check that destinations were assigned to correct chapters
        total_destinations = sum(
            len(destinations) for destinations in chapters_data.values()
        )
        assert total_destinations == 3  # Based on sample content

        # Verify stats
        assert parser.stats["successful"] == 3
        assert parser.stats["processed"] == 3
