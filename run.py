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
from pathlib import Path
from find_your_next_adventure.parsers.adventure_guide_parser import AdventureGuideParser
from find_your_next_adventure.utils.logging_config import setup_logging, log_session_start, log_session_end

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
        print(__doc__)
        print("\nError: Please provide PDF file and output directory, or run without arguments for example.")
        print("Examples:")
        print("  python run.py 'my_guide.pdf' './output/'")
        print("  python run.py")
        sys.exit(1)
    
    # Validate inputs
    if not pdf_file.exists():
        print(f"❌ Error: PDF file not found: {pdf_file}")
        sys.exit(1)
    
    if not pdf_file.suffix.lower() == '.pdf':
        print(f"❌ Error: File must be a PDF: {pdf_file}")
        sys.exit(1)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Show mode
    if mode == "example":
        print("🔍 Example Mode: Using sample PDF")
    else:
        print("🚀 Custom Mode: Parsing your PDF")
    
    print("=" * 50)
    print(f"📄 PDF file: {pdf_file}")
    print(f"📁 Output directory: {output_dir}")
    print()
    
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
        print("🔄 Parsing PDF...")
        parser.process_pdf(pdf_file, output_dir)
        
        # Get statistics
        stats = parser.get_stats()
        
        print("\n✅ Parsing completed successfully!")
        print("=" * 50)
        print(f"📊 Parser Statistics:")
        print(f"   • Successful destinations: {stats['successful']}")
        print(f"   • Failed parsing attempts: {stats['failed']}")
        print(f"   • Unknown countries: {stats['unknown_countries']}")
        
        # Print Ollama statistics
        parser.ollama_generator.print_final_stats()
        
        # List generated files
        json_files = list(output_dir.glob("*.json"))
        if json_files:
            print(f"\n📁 Generated files:")
            for file in sorted(json_files):
                print(f"   • {file.name}")
        
        print(f"\n🎉 All done! Check the '{output_dir}' directory for your JSON files.")
        
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
        print(f"❌ Error during parsing: {e}")
        # Log error and session end
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error during parsing: {e}")
        log_session_end({"Error": str(e), "Status": "Failed"})
        sys.exit(1)

if __name__ == "__main__":
    main() 