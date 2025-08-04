#!/usr/bin/env python3
"""
Find Your Next Adventure - PDF to JSON Parser
=============================================

A simple tool to extract adventure destinations from PDF files and convert them to JSON format.

Usage:
    # Parse your own PDF
    python run.py "my_adventure_guide.pdf" "./output/"
    
    # Run with sample PDF (no arguments)
    python run.py
"""

import sys
import json
import logging
from pathlib import Path
from find_your_next_adventure.parsers.adventure_guide_parser import AdventureGuideParser
from find_your_next_adventure.utils.logging_config import setup_logging, log_session_start, log_session_end

logger = logging.getLogger(__name__)

def main():
    """Main function for parsing PDF adventure guides."""
    
    # Set up centralized logging
    setup_logging()
    
    # Check if arguments provided
    if len(sys.argv) == 3:
        # Command line mode: parse user's PDF
        pdf_file = Path(sys.argv[1])
        output_dir = Path(sys.argv[2])
        mode = "custom"
    elif len(sys.argv) == 1:
        # Example mode: use sample PDF
        pdf_file = Path("FindYourNextAdventure.pdf")
        output_dir = Path("output")
        mode = "example"
    else:
        logger.error(__doc__)
        logger.error("\nError: Please provide PDF file and output directory, or run without arguments for example.")
        logger.error("Examples:")
        logger.error("  python run.py 'my_guide.pdf' './output/'")
        logger.error("  python run.py")
        sys.exit(1)
    
    # Validate inputs
    if not pdf_file.exists():
        logger.error(f"❌ Error: PDF file not found: {pdf_file}")
        sys.exit(1)
    
    if not pdf_file.suffix.lower() == '.pdf':
        logger.error(f"❌ Error: File must be a PDF: {pdf_file}")
        sys.exit(1)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Show mode
    if mode == "example":
        logger.info("🔍 Example Mode: Using sample PDF")
    else:
        logger.info("🚀 Custom Mode: Parsing your PDF")
    
    logger.info("=" * 50)
    logger.info(f"📄 PDF file: {pdf_file}")
    logger.info(f"📁 Output directory: {output_dir}")
    logger.info("")
    
    # Log session start
    session_info = {
        "Mode": mode,
        "PDF File": str(pdf_file),
        "Output Directory": str(output_dir),
        "Arguments": sys.argv[1:] if len(sys.argv) > 1 else []
    }
    log_session_start(session_info)
    
    try:
        # Initialize parser
        parser = AdventureGuideParser()
        
        # Parse the PDF
        logger.info("🔄 Parsing PDF...")
        parser.process_pdf(pdf_file, output_dir)
        
        # Get statistics
        stats = parser.get_stats()
        
        logger.info("\n✅ Parsing completed successfully!")
        logger.info("=" * 50)
        logger.info(f"📊 Parser Statistics:")
        logger.info(f"   • Successful destinations: {stats['successful']}")
        logger.info(f"   • Failed parsing attempts: {stats['failed']}")
        logger.info(f"   • Unknown countries: {stats['unknown_countries']}")
        
        # Print Ollama statistics
        parser.ollama_generator.print_final_stats()
        
        # List generated files
        json_files = list(output_dir.glob("*.json"))
        if json_files:
            logger.info(f"\n📁 Generated files:")
            for file in sorted(json_files):
                logger.info(f"   • {file.name}")
        
        logger.info(f"\n🎉 All done! Check the '{output_dir}' directory for your JSON files.")
        
        # Log session end with statistics
        final_stats = {
            "Successful destinations": stats['successful'],
            "Failed parsing attempts": stats['failed'],
            "Unknown countries": stats['unknown_countries'],
            "Generated files": len(json_files) if json_files else 0,
            "Output directory": str(output_dir)
        }
        log_session_end(final_stats)
        
    except Exception as e:
        logger.error(f"❌ Error during parsing: {e}")
        # Log error and session end
        log_session_end({"Error": str(e), "Status": "Failed"})
        sys.exit(1)

if __name__ == "__main__":
    main() 