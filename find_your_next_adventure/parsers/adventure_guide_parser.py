import json
import logging
import re
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import fitz  # PyMuPDF

from find_your_next_adventure.models.chapter import Chapter
from find_your_next_adventure.models.coordinates import Coordinates
from find_your_next_adventure.models.destination import Destination, ExtendedLinks
from find_your_next_adventure.utils.maps import (
    generate_extended_links,
    generate_google_maps_link,
)
from find_your_next_adventure.utils.ollama_generator import OllamaGenerator

logger = logging.getLogger(__name__)


class AdventureGuideParser:

    COUNTRY_MAPPING = {
        # Europe
        "NORWAY": {"country": "Norway", "region": "Scandinavia"},
        "SWEDEN": {"country": "Sweden", "region": "Scandinavia"},
        "FINLAND": {"country": "Finland", "region": "Scandinavia"},
        "DENMARK": {"country": "Denmark", "region": "Scandinavia"},
        "ICELAND": {"country": "Iceland", "region": "Nordic"},
        "ESTONIA": {"country": "Estonia", "region": "Baltic States"},
        "LATVIA": {"country": "Latvia", "region": "Baltic States"},
        "LITHUANIA": {"country": "Lithuania", "region": "Baltic States"},
        "UK": {"country": "United Kingdom", "region": "British Isles"},
        "ENGLAND": {"country": "United Kingdom", "region": "British Isles"},
        "SCOTLAND": {"country": "United Kingdom", "region": "British Isles"},
        "WALES": {"country": "United Kingdom", "region": "British Isles"},
        "NORTHERN IRELAND": {"country": "United Kingdom", "region": "British Isles"},
        "IRELAND": {"country": "Ireland", "region": "British Isles"},
        "FRANCE": {"country": "France", "region": "Western Europe"},
        "NETHERLANDS": {"country": "Netherlands", "region": "Western Europe"},
        "BELGIUM": {"country": "Belgium", "region": "Western Europe"},
        "GERMANY": {"country": "Germany", "region": "Central Europe"},
        "SWITZERLAND": {"country": "Switzerland", "region": "Central Europe"},
        "AUSTRIA": {"country": "Austria", "region": "Central Europe"},
        "CZECH": {"country": "Czech Republic", "region": "Central Europe"},
        "SLOVAKIA": {"country": "Slovakia", "region": "Central Europe"},
        "HUNGARY": {"country": "Hungary", "region": "Central Europe"},
        "POLAND": {"country": "Poland", "region": "Eastern Europe"},
        "RUSSIA": {"country": "Russia", "region": "Russia"},
        "UKRAINE": {"country": "Ukraine", "region": "Eastern Europe"},
        "ROMANIA": {"country": "Romania", "region": "Eastern Europe"},
        "BULGARIA": {"country": "Bulgaria", "region": "Eastern Europe"},
        "ITALY": {"country": "Italy", "region": "Southern Europe"},
        "SPAIN": {"country": "Spain", "region": "Southern Europe"},
        "PORTUGAL": {"country": "Portugal", "region": "Southern Europe"},
        "GREECE": {"country": "Greece", "region": "Southern Europe"},
        "CROATIA": {"country": "Croatia", "region": "Southern Europe"},
        "SLOVENIA": {"country": "Slovenia", "region": "Southern Europe"},
        "MONACO": {"country": "Monaco", "region": "Western Europe"},
        # Americas
        "CANADA": {"country": "Canada", "region": "North America"},
        "US": {"country": "United States", "region": "North America"},
        "USA": {"country": "United States", "region": "North America"},
        "ALASKA": {"country": "United States", "region": "Alaska"},
        "HAWAII": {"country": "United States", "region": "Pacific"},
        "GREENLAND": {"country": "Greenland", "region": "Arctic"},
        "MEXICO": {"country": "Mexico", "region": "North America"},
        "PUERTO RICO": {"country": "Puerto Rico", "region": "Caribbean"},
        "GUATEMALA": {"country": "Guatemala", "region": "Central America"},
        "BELIZE": {"country": "Belize", "region": "Central America"},
        "HONDURAS": {"country": "Honduras", "region": "Central America"},
        "NICARAGUA": {"country": "Nicaragua", "region": "Central America"},
        "COSTA RICA": {"country": "Costa Rica", "region": "Central America"},
        "PANAMA": {"country": "Panama", "region": "Central America"},
        "CUBA": {"country": "Cuba", "region": "Caribbean"},
        "JAMAICA": {"country": "Jamaica", "region": "Caribbean"},
        "BAHAMAS": {"country": "Bahamas", "region": "Caribbean"},
        "CAYMAN ISLANDS": {"country": "Cayman Islands", "region": "Caribbean"},
        "COLOMBIA": {"country": "Colombia", "region": "South America"},
        "VENEZUELA": {"country": "Venezuela", "region": "South America"},
        "GUYANA": {"country": "Guyana", "region": "South America"},
        "BRAZIL": {"country": "Brazil", "region": "South America"},
        "ECUADOR": {"country": "Ecuador", "region": "South America"},
        "PERU": {"country": "Peru", "region": "South America"},
        "BOLIVIA": {"country": "Bolivia", "region": "South America"},
        "CHILE": {"country": "Chile", "region": "South America"},
        "ARGENTINA": {"country": "Argentina", "region": "South America"},
        # Asia
        "CHINA": {"country": "China", "region": "East Asia"},
        "JAPAN": {"country": "Japan", "region": "East Asia"},
        "SOUTH KOREA": {"country": "South Korea", "region": "East Asia"},
        "KOREA": {"country": "South Korea", "region": "East Asia"},
        "MONGOLIA": {"country": "Mongolia", "region": "Central Asia"},
        "KAZAKHSTAN": {"country": "Kazakhstan", "region": "Central Asia"},
        "KYRGYZSTAN": {"country": "Kyrgyzstan", "region": "Central Asia"},
        "TAJIKISTAN": {"country": "Tajikistan", "region": "Central Asia"},
        "UZBEKISTAN": {"country": "Uzbekistan", "region": "Central Asia"},
        "TURKMENISTAN": {"country": "Turkmenistan", "region": "Central Asia"},
        "INDIA": {"country": "India", "region": "South Asia"},
        "NEPAL": {"country": "Nepal", "region": "South Asia"},
        "BHUTAN": {"country": "Bhutan", "region": "South Asia"},
        "BANGLADESH": {"country": "Bangladesh", "region": "South Asia"},
        "SRI LANKA": {"country": "Sri Lanka", "region": "South Asia"},
        "THAILAND": {"country": "Thailand", "region": "Southeast Asia"},
        "VIETNAM": {"country": "Vietnam", "region": "Southeast Asia"},
        "CAMBODIA": {"country": "Cambodia", "region": "Southeast Asia"},
        "LAOS": {"country": "Laos", "region": "Southeast Asia"},
        "MYANMAR": {"country": "Myanmar", "region": "Southeast Asia"},
        "MALAYSIA": {"country": "Malaysia", "region": "Southeast Asia"},
        "SINGAPORE": {"country": "Singapore", "region": "Southeast Asia"},
        "INDONESIA": {"country": "Indonesia", "region": "Southeast Asia"},
        "BRUNEI": {"country": "Brunei", "region": "Southeast Asia"},
        "PHILIPPINES": {"country": "Philippines", "region": "Southeast Asia"},
        # Middle East
        "TURKEY": {"country": "Turkey", "region": "Middle East"},
        "IRAN": {"country": "Iran", "region": "Middle East"},
        "IRAQ": {"country": "Iraq", "region": "Middle East"},
        "ISRAEL": {"country": "Israel", "region": "Middle East"},
        "PALESTINE": {"country": "Palestine", "region": "Middle East"},
        "LEBANON": {"country": "Lebanon", "region": "Middle East"},
        "JORDAN": {"country": "Jordan", "region": "Middle East"},
        "SAUDI ARABIA": {"country": "Saudi Arabia", "region": "Middle East"},
        "UAE": {"country": "United Arab Emirates", "region": "Middle East"},
        "OMAN": {"country": "Oman", "region": "Middle East"},
        "YEMEN": {"country": "Yemen", "region": "Middle East"},
        "BAHRAIN": {"country": "Bahrain", "region": "Middle East"},
        "AZERBAIJAN": {"country": "Azerbaijan", "region": "Caucasus"},
        # Africa
        "MOROCCO": {"country": "Morocco", "region": "North Africa"},
        "ALGERIA": {"country": "Algeria", "region": "North Africa"},
        "TUNISIA": {"country": "Tunisia", "region": "North Africa"},
        "EGYPT": {"country": "Egypt", "region": "North Africa"},
        "SENEGAL": {"country": "Senegal", "region": "West Africa"},
        "MALI": {"country": "Mali", "region": "West Africa"},
        "BURKINA FASO": {"country": "Burkina Faso", "region": "West Africa"},
        "NIGERIA": {"country": "Nigeria", "region": "West Africa"},
        "ETHIOPIA": {"country": "Ethiopia", "region": "East Africa"},
        "KENYA": {"country": "Kenya", "region": "East Africa"},
        "TANZANIA": {"country": "Tanzania", "region": "East Africa"},
        "CONGO": {
            "country": "Democratic Republic of Congo",
            "region": "Central Africa",
        },
        "ANGOLA": {"country": "Angola", "region": "Central Africa"},
        "EQUATORIAL GUINEA": {
            "country": "Equatorial Guinea",
            "region": "Central Africa",
        },
        "SOUTH AFRICA": {"country": "South Africa", "region": "Southern Africa"},
        "NAMIBIA": {"country": "Namibia", "region": "Southern Africa"},
        "BOTSWANA": {"country": "Botswana", "region": "Southern Africa"},
        "ZAMBIA": {"country": "Zambia", "region": "Southern Africa"},
        "MALAWI": {"country": "Malawi", "region": "Southern Africa"},
        "MADAGASCAR": {"country": "Madagascar", "region": "Indian Ocean"},
        # Oceania
        "AUSTRALIA": {"country": "Australia", "region": "Oceania"},
        "NEW ZEALAND": {"country": "New Zealand", "region": "Oceania"},
        "FIJI": {"country": "Fiji", "region": "Pacific Islands"},
        "SAMOA": {"country": "Samoa", "region": "Pacific Islands"},
        "COOK ISLANDS": {"country": "Cook Islands", "region": "Pacific Islands"},
        "FRENCH POLYNESIA": {
            "country": "French Polynesia",
            "region": "Pacific Islands",
        },
        "MICRONESIA": {"country": "Micronesia", "region": "Pacific Islands"},
        "PAPUA NEW GUINEA": {"country": "Papua New Guinea", "region": "Oceania"},
        "MALDIVES": {"country": "Maldives", "region": "Indian Ocean"},
        "MAURITIUS": {"country": "Mauritius", "region": "Indian Ocean"},
        # Special regions
        "ANTARCTICA": {"country": "Antarctica", "region": "Antarctica"},
        "ARCTIC": {"country": "Arctic", "region": "Arctic"},
        "GALAPAGOS": {"country": "Ecuador", "region": "South America"},
        "BALEARIC": {"country": "Spain", "region": "Southern Europe"},
        "CANARY": {"country": "Spain", "region": "Atlantic Islands"},
    }

    SPECIAL_CASES = {
        "GEOGRAPHICAL NORTH POLE": {"country": "Arctic", "region": "North Pole"},
        "BOTH POLES": {"country": "Multiple", "region": "Global"},
        "WORLDWIDE": {"country": "Multiple", "region": "Global"},
        "ALL OVER": {"country": "Multiple", "region": "Multiple"},
        "ACROSS": {"country": "Multiple", "region": "Multiple"},
        "NEW YORK, TOKYO": {"country": "Multiple", "region": "Global Cities"},
        "LONDON, NEW YORK, TOKYO": {"country": "Multiple", "region": "Global Cities"},
        "NEW YORK, PARIS, OR LONDON": {
            "country": "Multiple",
            "region": "Global Cities",
        },
        "RED SEA": {"country": "Multiple", "region": "Red Sea"},
        "CASPIAN SEA": {"country": "Multiple", "region": "Caspian Region"},
        "EMPTY QUARTER": {"country": "Saudi Arabia", "region": "Middle East"},
        "SAHARA DESERT": {"country": "Multiple", "region": "Sahara Desert"},
        "TIERRA DEL FUEGO": {"country": "Multiple", "region": "South America"},
        "PATAGONIA": {"country": "Multiple", "region": "South America"},
        "FRENCH RIVIERA": {"country": "France", "region": "Western Europe"},
    }

    CHAPTERS = {
        1: {
            "title": "From 90° North to 60° North",
            "range": {"from": "90° North", "to": "60° North"},
            "ids": (1, 44),
        },
        2: {
            "title": "From 60° North to 45° North",
            "range": {"from": "60° North", "to": "45° North"},
            "ids": (45, 265),
        },
        3: {
            "title": "From 45° North to 30° North",
            "range": {"from": "45° North", "to": "30° North"},
            "ids": (266, 560),
        },
        4: {
            "title": "From 30° North to 15° North",
            "range": {"from": "30° North", "to": "15° North"},
            "ids": (561, 711),
        },
        5: {
            "title": "From 15° North to 0° North",
            "range": {"from": "15° North", "to": "0° North"},
            "ids": (712, 808),
        },
        6: {
            "title": "From 0° South to 15° South",
            "range": {"from": "0° South", "to": "15° South"},
            "ids": (809, 861),
        },
        7: {
            "title": "From 15° South to 30° South",
            "range": {"from": "15° South", "to": "30° South"},
            "ids": (862, 929),
        },
        8: {
            "title": "From 30° South to 90° South",
            "range": {"from": "30° South", "to": "90° South"},
            "ids": (930, 1000),
        },
    }

    def __init__(self):
        self.pattern = re.compile(
            r"(\d+)\.\s+(.+?)\s+-\s+Latitude:\s*([\d.-]+)\s*([NS])\s+Longitude:\s*([\d.-]+)\s*([EW])?"
        )
        self.stats = {
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "unknown_countries": 0,
        }
        self.failed_lines = []  # Track failed lines for debugging
        
        # Initialize Ollama generator
        self.ollama_generator = OllamaGenerator()

    def generate_main_attractions(self, location: str, country: str, region: str) -> Tuple[str, str]:
        """
        Generate main attractions in English and French using the dedicated Ollama generator.
        
        Args:
            location: The location name
            country: The country name
            region: The region name
            
        Returns:
            Tuple of (mainAttractionEn, mainAttractionFr)
        """
        return self.ollama_generator.generate_attractions(location, country, region)

    def parse_line(self, line: str) -> Optional[Destination]:
        self.stats["processed"] += 1

        line = line.strip()
        if not line:
            return None

        match = self.pattern.match(line)
        if not match:
            self.stats["failed"] += 1
            self.failed_lines.append(line)  # Store failed line
            return None

        try:
            id_str, location, lat, lat_dir, lng, lng_dir = match.groups()

            location = self.clean_location(location)
            coordinates = self.parse_coordinates(lat, lat_dir, lng, lng_dir)

            if not (
                -90 <= coordinates.latitude <= 90
                and -180 <= coordinates.longitude <= 180
            ):
                self.stats["failed"] += 1
                self.failed_lines.append(f"Invalid coords: {line}")
                return None

            country, region = self.identify_country_region(location)

            if country == "Unknown":
                self.stats["unknown_countries"] += 1

            # Generate Google Maps link
            google_maps_link = generate_google_maps_link(location, coordinates)

            # Generate extended links
            extended_links_dict = generate_extended_links(location, coordinates)
            extended_links = ExtendedLinks(**extended_links_dict)

            # Generate main attractions using Ollama
            main_attraction_en, main_attraction_fr = self.generate_main_attractions(location, country, region)

            destination = Destination(
                id=int(id_str),
                location=location,
                coordinates=coordinates,
                country=country,
                region=region,
                mainAttractionEn=main_attraction_en,
                mainAttractionFr=main_attraction_fr,
                googleMapsLink=google_maps_link,
                extendedLinks=extended_links,
            )

            self.stats["successful"] += 1
            return destination

        except (ValueError, TypeError) as e:
            logger.error(f"Parse error: {line} - {e}")
            self.stats["failed"] += 1
            self.failed_lines.append(f"Error: {line}")
            return None

    def save_debug_report(self, output_dir: Path) -> None:
        """Save debug report with failed lines analysis"""
        if not self.failed_lines:
            return

        debug_report = {
            "summary": self.stats,
            "success_rate": f"{(self.stats['successful'] / max(1, self.stats['processed'])) * 100:.1f}%",
            "failed_lines_sample": self.failed_lines[:50],  # First 50 failed lines
            "total_failed_lines": len(self.failed_lines),
        }

        debug_file = output_dir / "debug_report.json"
        try:
            with open(debug_file, "w", encoding="utf-8") as f:
                json.dump(debug_report, f, ensure_ascii=False, indent=2)
            logger.info(f"Debug report saved: {debug_file}")
            print(f"   💾 Saved: {debug_file.name}")
        except Exception as e:
            logger.error(f"Debug report error: {e}")
            print(f"   ❌ Debug report error: {e}")

    def clean_location(self, location: str) -> str:
        location = re.sub(r"\s+", " ", location.strip())
        corrections = {
            "SOLVENIA": "SLOVENIA",
            "PAPAU NEW GUINEA": "PAPUA NEW GUINEA",
            "TAJIKSTAN": "TAJIKISTAN",
        }
        for error, correction in corrections.items():
            location = location.replace(error, correction)
        return location

    def parse_coordinates(
        self, lat: str, lat_dir: str, lng: str, lng_dir: str
    ) -> Coordinates:
        latitude = float(lat)
        longitude = float(lng)

        if lat_dir == "S":
            latitude = -latitude
        if lng_dir == "W":
            longitude = -longitude

        return Coordinates(
            latitude=latitude,
            longitude=longitude,
            latitudeDirection=lat_dir,
            longitudeDirection=lng_dir or "E",
        )

    def identify_country_region(self, location: str) -> Tuple[str, str]:
        location_upper = location.upper().strip()

        for special_key, info in self.SPECIAL_CASES.items():
            if special_key in location_upper:
                return info["country"], info["region"]

        for keyword, info in self.COUNTRY_MAPPING.items():
            if keyword in location_upper:
                return info["country"], info["region"]

        patterns = [
            (r"\b(ISLAND|ISLANDS|ARCHIPELAGO)\b", "Multiple", "Islands"),
            (r"\b(DESERT|SEA|OCEAN|BAY|GULF)\b", "Multiple", "Maritime Region"),
            (r"\b(MOUNTAINS?|ALPS|HIMALAYAS?)\b", "Multiple", "Mountain Region"),
            (r"\b(RIVER|LAKE|FALLS)\b", "Multiple", "Water Feature"),
            (r"\b(NATIONAL PARK|RESERVE|PARK)\b", "Multiple", "Protected Area"),
        ]

        for pattern, country, region in patterns:
            if re.search(pattern, location_upper):
                return country, region

        if "," in location_upper:
            parts = [part.strip() for part in location_upper.split(",")]
            potential_country = parts[-1]
            potential_country = re.sub(
                r"\b(PROVINCE|REGION|STATE|TERRITORY|GOVERNORATE)\b",
                "",
                potential_country,
            ).strip()

            for keyword, info in self.COUNTRY_MAPPING.items():
                if keyword in potential_country:
                    return info["country"], info["region"]

        if any(word in location_upper for word in ["MULTIPLE", "VARIOUS", "WORLDWIDE"]):
            return "Multiple", "Multiple"

        return "Unknown", "Unknown"

    def parse_pdf_content(self, content: str) -> Dict[int, List[Destination]]:
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        chapters_data = {i: [] for i in range(1, 9)}

        self.stats = {
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "unknown_countries": 0,
        }
        self.failed_lines = []  # Reset failed lines

        total_lines = len(lines)
        print(f"📖 Processing {total_lines} lines of content...")

        for i, line in enumerate(lines):
            if i % 100 == 0 and i > 0:
                print(f"   📊 Progress: {i}/{total_lines} lines ({i/total_lines*100:.1f}%)")

            destination = self.parse_line(line)
            if destination:
                for chapter_num, chapter_info in self.CHAPTERS.items():
                    start_id, end_id = chapter_info["ids"]
                    if start_id <= destination.id <= end_id:
                        chapters_data[chapter_num].append(destination)
                        break

        success_rate = (
            self.stats["successful"] / max(1, self.stats["processed"])
        ) * 100
        logger.info(
            f"Processed: {self.stats['processed']}, Successful: {self.stats['successful']}, "
            f"Failed: {self.stats['failed']}, Unknown countries: {self.stats['unknown_countries']}"
        )
        logger.info(f"Success rate: {success_rate:.1f}%")

        print(f"✅ Content processing complete: {self.stats['processed']} lines processed")
        print(f"📊 Success rate: {success_rate:.1f}% ({self.stats['successful']}/{self.stats['processed']})")

        if self.failed_lines:
            logger.info("Failed lines sample (first 5):")
            for line in self.failed_lines[:5]:
                logger.info(f"  {line}")

        return chapters_data

    def load_pdf(self, pdf_path: Path) -> str:
        try:
            doc = fitz.open(pdf_path)
            content = ""
            total_pages = len(doc)
            print(f"   📄 Loading {total_pages} pages...")
            
            for page_num, page in enumerate(doc):
                if page_num % 10 == 0 and page_num > 0:
                    print(f"      📊 Page progress: {page_num}/{total_pages} ({page_num/total_pages*100:.1f}%)")
                content += page.get_text() + "\n"
            
            doc.close()
            print(f"   ✅ PDF loaded successfully: {len(content)} characters")
            return content
        except Exception as e:
            logger.error(f"Failed to load PDF: {e}")
            print(f"   ❌ Failed to load PDF: {e}")
            return ""

    def create_chapter_json(
        self, chapter_num: int, destinations: List[Destination]
    ) -> Chapter:
        chapter_info = self.CHAPTERS[chapter_num]

        return Chapter(
            title=f"Find Your Next Adventure - Chapter {chapter_num}: {chapter_info['title']}",
            description=f"Adventure destinations {chapter_info['title'].lower()}",
            latitudeRange=chapter_info["range"],
            totalDestinations=len(destinations),
            destinations=destinations,
            metadata={
                "source": "Find Your Next Adventure Travel Guide",
                "chapter": str(chapter_num),
                "generatedDate": "2025-07-31",
                "coordinateSystem": "WGS84",
                "format": "Decimal Degrees",
            },
        )

    def save_json(self, data: Chapter, output_path: Path) -> None:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(asdict(data), f, ensure_ascii=False, indent=2)
            logger.info(f"Saved: {output_path}")
            print(f"   💾 Saved: {output_path.name}")
        except Exception as e:
            logger.error(f"Save error: {e}")
            print(f"   ❌ Save error: {e}")

    def create_combined_json(
        self, chapters_data: Dict[int, List[Destination]], output_dir: Path
    ) -> None:
        combined_data = {
            "title": "Find Your Next Adventure - Complete Guide",
            "description": "Complete adventure destinations guide from 90° North to 90° South",
            "totalChapters": 8,
            "totalDestinations": sum(
                len(destinations) for destinations in chapters_data.values()
            ),
            "chapters": {},
            "metadata": {
                "source": "Find Your Next Adventure Travel Guide",
                "generatedDate": "2025-07-31",
                "coordinateSystem": "WGS84",
                "format": "Decimal Degrees",
            },
        }

        for chapter_num, destinations in chapters_data.items():
            if destinations:
                chapter_info = self.CHAPTERS[chapter_num]
                combined_data["chapters"][f"chapter_{chapter_num}"] = {
                    "title": chapter_info["title"],
                    "latitudeRange": chapter_info["range"],
                    "destinationCount": len(destinations),
                    "destinations": [asdict(dest) for dest in destinations],
                }

        output_file = output_dir / "complete_adventure_guide.json"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(combined_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Complete guide saved: {output_file}")
            print(f"   💾 Saved: {output_file.name}")
        except Exception as e:
            logger.error(f"Combined JSON error: {e}")
            print(f"   ❌ Combined JSON error: {e}")

    def process_pdf(self, pdf_path: Path, output_dir: Path) -> None:
        try:
            print(f"📄 Loading PDF: {pdf_path}")
            logger.info(f"Processing: {pdf_path}")

            content = self.load_pdf(pdf_path)
            if not content:
                logger.error("Failed to load PDF content")
                print("❌ Failed to load PDF content")
                return

            print(f"🔍 Parsing PDF content...")
            chapters_data = self.parse_pdf_content(content)
            total_destinations = sum(len(destinations) for destinations in chapters_data.values())
            print(f"✅ Found {total_destinations} destinations across {len(chapters_data)} chapters")

            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"📁 Output directory: {output_dir}")

            print(f"💾 Saving chapter files...")
            for chapter_num, destinations in chapters_data.items():
                if destinations:
                    chapter_json = self.create_chapter_json(chapter_num, destinations)
                    output_file = (
                        output_dir / f"chapter_{chapter_num}_destinations.json"
                    )
                    self.save_json(chapter_json, output_file)
                    print(f"   📄 Chapter {chapter_num}: {len(destinations)} destinations")

            print(f"🔗 Creating combined JSON file...")
            self.create_combined_json(chapters_data, output_dir)
            print(f"✅ Combined JSON file created")

            if self.failed_lines:
                print(f"🐛 Saving debug report ({len(self.failed_lines)} failed lines)...")
                self.save_debug_report(output_dir)
                print(f"✅ Debug report saved")

            print(f"🎉 Processing complete! Total destinations: {total_destinations}")
            logger.info(
                f"Processing complete! Total destinations: {total_destinations}"
            )
            logger.info(f"Files saved to: {output_dir.absolute()}")

        except Exception as e:
            logger.error(f"Processing error: {e}")
            print(f"❌ Error processing PDF: {e}")
            raise

    def get_stats(self) -> dict:
        """
        Get parsing statistics.

        Returns:
            Dictionary containing parsing statistics.
        """
        return self.stats.copy()
