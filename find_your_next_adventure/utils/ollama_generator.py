#!/usr/bin/env python3
"""
Ollama text generation utilities for the adventure guide parser.
"""

import logging
from typing import Tuple

import ollama

logger = logging.getLogger(__name__)


class OllamaGenerator:
    """Dedicated class for generating text using Ollama with phi4-mini model."""

    def __init__(self, model: str = "phi4-mini"):
        """
        Initialize the Ollama generator.
        
        Args:
            model: The Ollama model to use (default: phi4-mini)
        """
        self.model = model
        self.options = {
            'temperature': 0.7,
            'top_p': 0.9,
            'max_tokens': 200  # Increased for bilingual response
        }
        self.log_file = "ollama_generation.log"
        self.session_started = False

    def _create_session_header(self):
        """Create a session header for the log file."""
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            session_header = f"""
{'═'*80}
╔══════════════════════════════════════════════════════════════════════════════╗
║                        OLLAMA GENERATION SESSION                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

🚀 SESSION STARTED: {timestamp}
🤖 MODEL: {self.model}
📁 LOG FILE: {self.log_file}
⚙️  TEMPERATURE: {self.options.get('temperature', 'N/A')}
🎯 TOP_P: {self.options.get('top_p', 'N/A')}
📏 MAX_TOKENS: {self.options.get('max_tokens', 'N/A')}

{'═'*80}

"""
            
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(session_header)
                
            logger.info(f"📋 Created session header in {self.log_file}")
            self.session_started = True
            
        except Exception as e:
            logger.error(f"❌ Failed to create session header: {e}")

    def _append_to_log(self, location: str, prompt: str, response: str, en_result: str, fr_result: str):
        """
        Append the Ollama generation details to the log file with hierarchical structure.
        
        Args:
            location: The location being processed
            prompt: The prompt sent to Ollama
            response: The raw response from Ollama
            en_result: The extracted English result
            fr_result: The extracted French result
        """
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            log_entry = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           OLLAMA GENERATION LOG                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📅 TIMESTAMP: {timestamp}
📍 LOCATION: {location}
🤖 MODEL: {self.model}

┌──────────────────────────────────────────────────────────────────────────────┐
│                              INPUT PROMPT                                   │
└──────────────────────────────────────────────────────────────────────────────┘
{prompt}

┌──────────────────────────────────────────────────────────────────────────────┐
│                            RAW RESPONSE                                     │
└──────────────────────────────────────────────────────────────────────────────┘
{response}

┌──────────────────────────────────────────────────────────────────────────────┐
│                           PARSED RESULTS                                    │
└──────────────────────────────────────────────────────────────────────────────┘

🇬🇧 ENGLISH:
{en_result}

🇫🇷 FRENCH:
{fr_result}

┌──────────────────────────────────────────────────────────────────────────────┐
│                              SUMMARY                                        │
└──────────────────────────────────────────────────────────────────────────────┘
✅ Status: Success
📊 English Length: {len(en_result)} characters
📊 French Length: {len(fr_result)} characters
🎯 Location: {location}

{'═'*80}
"""
            
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
                
            logger.info(f"📝 Appended hierarchical generation log for {location} to {self.log_file}")
            
        except Exception as e:
            logger.error(f"❌ Failed to append to log file: {e}")

    def _append_error_to_log(self, location: str, error: Exception, fallback_en: str, fallback_fr: str):
        """
        Append error details to the log file with hierarchical structure.
        
        Args:
            location: The location being processed
            error: The exception that occurred
            fallback_en: The fallback English description
            fallback_fr: The fallback French description
        """
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            log_entry = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        OLLAMA GENERATION ERROR LOG                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

📅 TIMESTAMP: {timestamp}
📍 LOCATION: {location}
🤖 MODEL: {self.model}
❌ ERROR TYPE: {type(error).__name__}

┌──────────────────────────────────────────────────────────────────────────────┐
│                              ERROR DETAILS                                  │
└──────────────────────────────────────────────────────────────────────────────┘
{str(error)}

┌──────────────────────────────────────────────────────────────────────────────┐
│                           FALLBACK RESULTS                                  │
└──────────────────────────────────────────────────────────────────────────────┘

🇬🇧 ENGLISH (FALLBACK):
{fallback_en}

🇫🇷 FRENCH (FALLBACK):
{fallback_fr}

┌──────────────────────────────────────────────────────────────────────────────┐
│                              SUMMARY                                        │
└──────────────────────────────────────────────────────────────────────────────┘
❌ Status: Error - Using Fallback
📊 English Length: {len(fallback_en)} characters
📊 French Length: {len(fallback_fr)} characters
🎯 Location: {location}
⚠️  Note: Generated content is fallback, not AI-generated

{'═'*80}
"""
            
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
                
            logger.info(f"📝 Appended error log for {location} to {self.log_file}")
            
        except Exception as e:
            logger.error(f"❌ Failed to append error to log file: {e}")

    def generate_attractions(self, location: str, country: str, region: str) -> Tuple[str, str]:
        """
        Generate main attractions in both English and French using a single prompt.
        
        Args:
            location: The location name
            country: The country name
            region: The region name
            
        Returns:
            Tuple of (mainAttractionEn, mainAttractionFr)
        """
        try:
            # Create session header if this is the first generation
            if not self.session_started:
                self._create_session_header()
            
            # Combined bilingual prompt
            prompt = f"""Generate a brief, engaging description of the main attraction or highlight for {location}, {country} in the {region} region.

Focus on what makes this place special for adventure travelers. Keep it concise (1-2 sentences) and appealing.

Location: {location}
Country: {country}
Region: {region}

Please provide the description in both English and French formats:

English:"""

            # Generate response
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options=self.options
            )
            
            # Parse the response to extract English and French parts
            response_text = response['response'].strip()
            
            # Split the response into English and French parts
            parts = self._parse_bilingual_response(response_text)
            
            if len(parts) >= 2:
                main_attraction_en = parts[0].strip()
                main_attraction_fr = parts[1].strip()
            else:
                # Fallback if parsing fails
                main_attraction_en = response_text
                main_attraction_fr = f"Découvrez les paysages uniques et les expériences culturelles de {location} en {country}."
            
            # Append to log file
            self._append_to_log(location, prompt, response_text, main_attraction_en, main_attraction_fr)
            
            logger.info(f"Generated attractions for {location}: EN='{main_attraction_en[:50]}...', FR='{main_attraction_fr[:50]}...'")
            
            return main_attraction_en, main_attraction_fr
            
        except Exception as e:
            logger.error(f"Failed to generate attractions for {location}: {e}")
            # Return fallback descriptions
            fallback_en = f"Explore the unique landscapes and cultural experiences of {location} in {country}."
            fallback_fr = f"Découvrez les paysages uniques et les expériences culturelles de {location} en {country}."
            
            # Log the error and fallback with error-specific formatting
            self._append_error_to_log(location, e, fallback_en, fallback_fr)
            
            return fallback_en, fallback_fr

    def _parse_bilingual_response(self, response_text: str) -> list:
        """
        Parse the bilingual response to extract English and French parts.
        
        Args:
            response_text: The raw response from Ollama
            
        Returns:
            List containing [english_text, french_text]
        """
        # Common patterns for bilingual responses
        patterns = [
            # Pattern: "English: ... French: ..."
            (r"English:\s*(.*?)(?=French:|$)", r"French:\s*(.*?)$"),
            # Pattern: "EN: ... FR: ..."
            (r"EN:\s*(.*?)(?=FR:|$)", r"FR:\s*(.*?)$"),
            # Pattern: "English: ... Français: ..."
            (r"English:\s*(.*?)(?=Français:|$)", r"Français:\s*(.*?)$"),
            # Pattern: "🇬🇧 ... 🇫🇷 ..."
            (r"🇬🇧\s*(.*?)(?=🇫🇷|$)", r"🇫🇷\s*(.*?)$"),
        ]
        
        for en_pattern, fr_pattern in patterns:
            import re
            en_match = re.search(en_pattern, response_text, re.DOTALL | re.IGNORECASE)
            fr_match = re.search(fr_pattern, response_text, re.DOTALL | re.IGNORECASE)
            
            if en_match and fr_match:
                return [en_match.group(1).strip(), fr_match.group(1).strip()]
        
        # If no pattern matches, try to split by common separators
        separators = ["\n\n", "---", "===", "|||"]
        for separator in separators:
            if separator in response_text:
                parts = response_text.split(separator, 1)
                if len(parts) == 2:
                    return [parts[0].strip(), parts[1].strip()]
        
        # If all else fails, return the entire response as English
        return [response_text, ""]

    def test_connection(self) -> bool:
        """
        Test the connection to Ollama and the model.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            response = ollama.generate(
                model=self.model,
                prompt="Hello, this is a test.",
                options={'max_tokens': 10}
            )
            logger.info(f"Ollama connection test successful with model: {self.model}")
            return True
        except Exception as e:
            logger.error(f"Ollama connection test failed: {e}")
            return False 