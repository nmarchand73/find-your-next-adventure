#!/usr/bin/env python3
"""
Ollama text generation utilities for the adventure guide parser.
"""

import datetime
import logging
import re
from typing import Dict, List, Tuple

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
        self.stats = {
            'total_calls': 0,
            'successful_calls': 0,
            'error_calls': 0,
            'start_time': None
        }

    def _create_session_header(self):
        """Create a session header for the log file."""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.stats['start_time'] = datetime.datetime.now()
            
            session_header = f"""=== OLLAMA SESSION STARTED: {timestamp} ===
Model: {self.model} | Temp: {self.options.get('temperature', 'N/A')} | Max Tokens: {self.options.get('max_tokens', 'N/A')}
"""
            
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(session_header)
                
            print(f"🚀 Ollama session started | Model: {self.model} | Temp: {self.options.get('temperature', 'N/A')}")
            logger.info(f"📋 Session started: {self.model}")
            self.session_started = True
            
        except Exception as e:
            logger.error(f"❌ Failed to create session header: {e}")

    def _append_to_log(self, location: str, prompt: str, response: str, en_result: str, fr_result: str):
        """
        Append concise Ollama generation details to the log file and display on console.
        
        Args:
            location: The location being processed
            prompt: The prompt sent to Ollama
            response: The raw response from Ollama
            en_result: The extracted English result
            fr_result: The extracted French result
        """
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            # Update stats
            self.stats['total_calls'] += 1
            self.stats['successful_calls'] += 1
            
            # Truncate long responses for readability
            en_preview = en_result[:80] + "..." if len(en_result) > 80 else en_result
            fr_preview = fr_result[:80] + "..." if len(fr_result) > 80 else fr_result
            
            # Console output with progress
            elapsed = (datetime.datetime.now() - self.stats['start_time']).total_seconds() if self.stats['start_time'] else 0
            success_rate = (self.stats['successful_calls'] / self.stats['total_calls'] * 100) if self.stats['total_calls'] > 0 else 0
            
            print(f"✅ [{timestamp}] {location} | EN: {en_preview}")
            print(f"   📊 Progress: {self.stats['total_calls']} calls | {success_rate:.1f}% success | {elapsed:.1f}s elapsed")
            
            # Log file entry (concise)
            log_entry = f"""[{timestamp}] {location} | EN: {en_preview} | FR: {fr_preview}
"""
            
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
                
            logger.info(f"✅ {location}: {en_preview}")
            
        except Exception as e:
            logger.error(f"❌ Failed to append to log file: {e}")

    def _append_error_to_log(self, location: str, error: Exception, fallback_en: str, fallback_fr: str):
        """
        Append concise error details to the log file and display on console.
        
        Args:
            location: The location being processed
            error: The exception that occurred
            fallback_en: The fallback English description
            fallback_fr: The fallback French description
        """
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            # Update stats
            self.stats['total_calls'] += 1
            self.stats['error_calls'] += 1
            
            # Truncate fallback responses
            en_preview = fallback_en[:80] + "..." if len(fallback_en) > 80 else fallback_en
            fr_preview = fallback_fr[:80] + "..." if len(fallback_fr) > 80 else fallback_fr
            
            # Console output with error details
            elapsed = (datetime.datetime.now() - self.stats['start_time']).total_seconds() if self.stats['start_time'] else 0
            success_rate = (self.stats['successful_calls'] / self.stats['total_calls'] * 100) if self.stats['total_calls'] > 0 else 0
            
            print(f"❌ [{timestamp}] {location} | ERROR: {type(error).__name__} | FALLBACK: {en_preview}")
            print(f"   📊 Progress: {self.stats['total_calls']} calls | {success_rate:.1f}% success | {elapsed:.1f}s elapsed")
            
            # Log file entry (concise)
            log_entry = f"""[{timestamp}] {location} | ERROR: {type(error).__name__} | FALLBACK EN: {en_preview} | FALLBACK FR: {fr_preview}
"""
            
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
                
            logger.warning(f"⚠️  {location}: Error - {type(error).__name__}")
            
        except Exception as e:
            logger.error(f"❌ Failed to append error to log file: {e}")

    def get_stats(self) -> dict:
        """
        Get current generation statistics.
        
        Returns:
            Dictionary with generation statistics
        """
        if self.stats['start_time']:
            elapsed = (datetime.datetime.now() - self.stats['start_time']).total_seconds()
            avg_time = elapsed / self.stats['total_calls'] if self.stats['total_calls'] > 0 else 0
            success_rate = (self.stats['successful_calls'] / self.stats['total_calls'] * 100) if self.stats['total_calls'] > 0 else 0
            
            return {
                'total_calls': self.stats['total_calls'],
                'successful_calls': self.stats['successful_calls'],
                'error_calls': self.stats['error_calls'],
                'success_rate': success_rate,
                'elapsed_time': elapsed,
                'avg_time_per_call': avg_time
            }
        return self.stats

    def print_final_stats(self):
        """Print final generation statistics to console."""
        stats = self.get_stats()
        
        print("\n" + "="*60)
        print("📊 OLLAMA GENERATION STATISTICS")
        print("="*60)
        print(f"🎯 Total Calls: {stats['total_calls']}")
        print(f"✅ Successful: {stats['successful_calls']}")
        print(f"❌ Errors: {stats['error_calls']}")
        print(f"📈 Success Rate: {stats['success_rate']:.1f}%")
        print(f"⏱️  Total Time: {stats['elapsed_time']:.1f}s")
        print(f"⚡ Avg Time/Call: {stats['avg_time_per_call']:.2f}s")
        print(f"📁 Log File: {self.log_file}")
        print("="*60)

    def generate_attractions(self, location: str, country: str, region: str) -> Tuple[str, str]:
        """
        Generate main attractions in English and French for a location.
        This method now supports batching - it will queue the request and return immediately.
        Use process_batch() to actually generate the attractions.
        
        Args:
            location: The location name
            country: The country name
            region: The region name
            
        Returns:
            Tuple of (mainAttractionEn, mainAttractionFr) - will be placeholders until batch is processed
        """
        # Add to batch queue
        self._add_to_batch(location, country, region)
        
        # Return placeholder values - will be replaced after batch processing
        return f"Processing {location}...", f"Traitement de {location}..."
    
    def _add_to_batch(self, location: str, country: str, region: str):
        """Add a location to the current batch."""
        if not hasattr(self, 'batch_queue'):
            self.batch_queue = []
            
        self.batch_queue.append({
            'location': location,
            'country': country,
            'region': region
        })
        
        # Process batch if it reaches the size limit
        if len(self.batch_queue) >= 50:
            self.process_batch()
    
    def process_batch(self, force: bool = False):
        """
        Process the current batch of locations.
        
        Args:
            force: If True, process the batch even if it's not full
        """
        if not hasattr(self, 'batch_queue') or not self.batch_queue:
            return
            
        if not force and len(self.batch_queue) < 50:
            return
            
        if not self.session_started:
            self._create_session_header()
        
        batch = self.batch_queue[:50]  # Process up to 50 items
        self.batch_queue = self.batch_queue[50:]  # Remove processed items
        
        print(f"🔄 Processing {len(batch)} locations in single prompt...")
        
        try:
            # Create a single prompt for the entire batch
            batch_prompt = self._create_batch_prompt(batch)
            
            # Call Ollama once for the entire batch
            print(f"   📤 Sending single prompt with {len(batch)} locations to Ollama...")
            response = ollama.generate(
                model=self.model,
                prompt=batch_prompt,
                options=self.options
            )
            
            # Parse the batch response
            results = self._parse_batch_response(response['response'], batch)
            
            # Log the batch generation
            self._append_batch_to_log(batch, batch_prompt, response['response'], results)
            
            # Store results for retrieval
            if not hasattr(self, 'batch_results'):
                self.batch_results = {}
            
            for location, (en_result, fr_result) in results.items():
                self.batch_results[location] = (en_result, fr_result)
            
            print(f"   ✅ Successfully processed {len(results)} locations in single API call")
                
        except Exception as e:
            logger.error(f"Batch Ollama generation error: {e}")
            print(f"❌ Batch processing error: {e}")
            
            # Create fallback results for the entire batch
            for item in batch:
                location = item['location']
                country = item['country']
                fallback_en = f"Discover the unique charm and attractions of {location} in {country}."
                fallback_fr = f"Découvrez le charme unique et les attractions de {location} en {country}."
                
                if not hasattr(self, 'batch_results'):
                    self.batch_results = {}
                self.batch_results[location] = (fallback_en, fallback_fr)
                
                self._append_error_to_log(location, e, fallback_en, fallback_fr)
    
    def _create_batch_prompt(self, batch: List[dict]) -> str:
        """Create a prompt for processing multiple locations at once."""
        locations_text = "\n".join([
            f"- {item['location']} ({item['country']}, {item['region']})"
            for item in batch
        ])
        
        return f"""Generate brief, engaging descriptions of the main attractions for these travel destinations.

Locations:
{locations_text}

For each location, provide the response in this exact format:
[Location Name]: English: [Brief description in English] | French: [Brief description in French]

Keep each description concise (1-2 sentences) and focus on what makes each destination unique and appealing to travelers.

Please provide exactly {len(batch)} responses, one for each location listed above.

Example format:
Paris: English: Discover the iconic Eiffel Tower and charming cafes along the Seine River | French: Découvrez la tour Eiffel emblématique et les charmants cafés le long de la Seine
Tokyo: English: Experience the blend of ancient temples and cutting-edge technology in this vibrant metropolis | French: Vivez le mélange de temples anciens et de technologie de pointe dans cette métropole vibrante"""
    
    def _parse_batch_response(self, response: str, batch: List[dict]) -> Dict[str, Tuple[str, str]]:
        """Parse the batch response to extract individual location results."""
        results = {}
        
        # Split response into lines and process each line
        lines = response.strip().split('\n')
        
        for item in batch:
            location = item['location']
            country = item['country']
            
            # Look for the location in the response lines
            found = False
            for line in lines:
                line = line.strip()
                if line.startswith(f"{location}:"):
                    # Parse the line: "Location: English: ... | French: ..."
                    parts = line.split("English:", 1)
                    if len(parts) == 2:
                        french_part = parts[1].split("| French:", 1)
                        if len(french_part) == 2:
                            en_result = french_part[0].strip()
                            fr_result = french_part[1].strip()
                            results[location] = (en_result, fr_result)
                            found = True
                            break
            
            if not found:
                # Fallback if parsing fails
                en_result = f"Discover the unique charm and attractions of {location} in {country}."
                fr_result = f"Découvrez le charme unique et les attractions de {location} en {country}."
                results[location] = (en_result, fr_result)
        
        return results
    
    def _append_batch_to_log(self, batch: List[dict], prompt: str, response: str, results: Dict[str, Tuple[str, str]]):
        """Log batch generation results."""
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            # Update stats
            self.stats['total_calls'] += 1
            self.stats['successful_calls'] += 1
            
            # Console output with more details
            print(f"✅ [{timestamp}] Batch processed: {len(batch)} locations in single prompt")
            
            # Show sample results
            sample_locations = list(results.keys())[:3]
            for location in sample_locations:
                en_result, fr_result = results[location]
                en_preview = en_result[:60] + "..." if len(en_result) > 60 else en_result
                print(f"   📍 {location}: {en_preview}")
            
            if len(results) > 3:
                print(f"   ... and {len(results) - 3} more locations")
            
            # Log file entry
            log_entry = f"[{timestamp}] BATCH: {len(batch)} locations processed in single prompt\n"
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
                
            logger.info(f"✅ Batch processed: {len(batch)} locations in single prompt")
            
        except Exception as e:
            logger.error(f"Failed to append batch to log file: {e}")
    
    def get_attraction_result(self, location: str) -> Tuple[str, str]:
        """
        Get the actual attraction result for a location after batch processing.
        
        Args:
            location: The location name
            
        Returns:
            Tuple of (mainAttractionEn, mainAttractionFr)
        """
        if hasattr(self, 'batch_results') and location in self.batch_results:
            return self.batch_results[location]
        
        # Fallback if result not found
        return f"Discover the unique charm and attractions of {location}.", f"Découvrez le charme unique et les attractions de {location}."

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