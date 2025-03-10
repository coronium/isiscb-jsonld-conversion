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

# Determine the project root and add it to the Python path
script_path = os.path.abspath(__file__)
scripts_dir = os.path.dirname(script_path)
src_dir = os.path.dirname(scripts_dir)  # src directory
project_root = os.path.dirname(src_dir)  # project root

# Print paths for debugging
print(f"Script path: {script_path}")
print(f"Project root: {project_root}")

# Add the project root and src directory to the system path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import directly from the source directory
try:
    # First try importing with full path
    from src.isiscb.pipeline.citation_pipeline import CitationConverterPipeline
    print("Successfully imported CitationConverterPipeline")
except ImportError as e:
    print(f"Import error: {e}")
    # Try alternative import paths
    try:
        # Add src to path explicitly
        sys.path.append(src_dir)
        from isiscb.pipeline.citation_pipeline import CitationConverterPipeline
        print("Successfully imported CitationConverterPipeline using alternative path")
    except ImportError as e:
        print(f"Alternative import failed: {e}")
        
        # One more try with a direct absolute import
        try:
            sys.path.append(os.path.join(project_root, 'src', 'isiscb'))
            from pipeline.citation_pipeline import CitationConverterPipeline
            print("Successfully imported CitationConverterPipeline using direct path")
        except ImportError as e:
            print(f"Direct import failed: {e}")
            # Show the system path for debugging
            print("\nCurrent sys.path:")
            for p in sys.path:
                print(f"  {p}")
            sys.exit(1)

def main():
    """Main function to run the conversion process."""
    # Check command line arguments
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input_file.csv output_file.json")
        sys.exit(1)
    
    # Get input and output paths from command line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Convert relative paths to absolute paths
    if not os.path.isabs(input_file):
        input_file = os.path.abspath(os.path.join(os.getcwd(), input_file))
    if not os.path.isabs(output_file):
        output_file = os.path.abspath(os.path.join(os.getcwd(), output_file))
    
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