"""Command-line interface for Find Your Next Adventure."""

import argparse
import sys
import logging
from pathlib import Path
from typing import Optional

from find_your_next_adventure.parsers import AdventureGuideParser

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract destinations from PDF and generate structured JSON files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "adventure_guide.pdf" "./output/"
  %(prog)s --verbose "guide.pdf" "/tmp/json_output/"
  %(prog)s --help
        """
    )
    
    parser.add_argument(
        "pdf_file",
        type=str,
        help="Path to the PDF file to process"
    )
    
    parser.add_argument(
        "output_directory",
        type=str,
        help="Directory where JSON files will be saved"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    return parser.parse_args()


def validate_inputs(pdf_path: Path, output_dir: Path) -> bool:
    """Validate input file and output directory."""
    if not pdf_path.exists():
        logger.error(f"PDF file not found: {pdf_path}")
        return False
        
    if not pdf_path.is_file():
        logger.error(f"Path is not a file: {pdf_path}")
        return False
        
    if not pdf_path.suffix.lower() == '.pdf':
        logger.error(f"File is not a PDF: {pdf_path}")
        return False
    
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Cannot create output directory {output_dir}: {e}")
        return False
        
    if not output_dir.is_dir():
        logger.error(f"Output path is not a directory: {output_dir}")
        return False
        
    return True


def main() -> Optional[int]:
    """Main entry point for the CLI."""
    args = None
    try:
        args = parse_arguments()
        setup_logging(args.verbose)
        
        logger.info("Find Your Next Adventure - PDF to JSON Parser")
        logger.info("=" * 50)
        
        pdf_path = Path(args.pdf_file).resolve()
        output_dir = Path(args.output_directory).resolve()
        
        logger.info(f"PDF file: {pdf_path}")
        logger.info(f"Output directory: {output_dir}")
        
        if not validate_inputs(pdf_path, output_dir):
            return 1
            
        # Initialize and run the parser
        parser = AdventureGuideParser()
        parser.process_pdf(pdf_path, output_dir)
        
        logger.info("=" * 50)
        logger.info("Processing completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        logger.info("\nProcessing interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args and args.verbose:
            logger.exception("Full traceback:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
