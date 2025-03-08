#!/usr/bin/env python
"""
Script for converting IsisCB citation data to JSON-LD format.

Usage:
    python cb_to_json.py input_file.csv output_file.json
"""

import sys
import os
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('isiscb_conversion')

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from the correct module path
from src.isiscb.pipeline.citation_pipeline import CitationConverterPipeline

def main():
    """Main function to run the conversion process."""
    # Check command line arguments
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input_file.csv output_file.json")
        sys.exit(1)
    
    # Get input and output paths from command line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Validate input file exists
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Initialize the converter pipeline
    pipeline = CitationConverterPipeline()
    
    # Convert the citations
    print(f"Converting citations from '{input_file}'...")
    jsonld_docs = pipeline.convert_csv_file(input_file, output_file)
    
    print(f"Converted {len(jsonld_docs)} citation records to JSON-LD")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    main()