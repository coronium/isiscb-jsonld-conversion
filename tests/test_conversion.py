#!/usr/bin/env python
"""
Test script for the IsisCB conversion pipeline.

This script tests the conversion pipeline with sample data to verify it's working properly.
"""

import os
import sys
import logging
import json
from pathlib import Path

# Properly add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import from the correct module paths - utils is inside isiscb
from src.isiscb.pipeline.citation_pipeline import CitationConverterPipeline
from src.isiscb.utils.data_loader import load_citation_data, get_paths

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('isiscb_conversion')

def test_single_record_conversion():
    """Test converting a single record and print the result."""
    # Load sample data
    try:
        df = load_citation_data()
        if df.empty:
            print("Error: Sample data is empty")
            return
        
        # Get the first record for testing
        sample_record = df.iloc[0]
        record_id = sample_record.get('Record ID', 'unknown')
        
        print(f"Testing conversion of record: {record_id}")
        
        # Initialize the converter pipeline
        pipeline = CitationConverterPipeline()
        
        # Convert the single record
        result = pipeline.convert_row(sample_record)
        
        # Pretty print the result
        print("\nConverted JSON-LD:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("\nConversion test completed successfully!")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

def test_file_conversion():
    """Test converting a file and saving the output."""
    try:
        # Get paths
        paths = get_paths()
        
        # Print debugging information
        print(f"Current working directory: {os.getcwd()}")
        print(f"Paths from config: {paths}")
        
        # Set up input and output paths using absolute paths
        sample_filename = "citation_sample_133.csv"  # Your actual filename
        
        # Try multiple places to find the file
        possible_locations = [
            os.path.join(project_root, "data", "raw", "samples", sample_filename),
            os.path.join(project_root, "data", "raw", sample_filename),
            os.path.join(paths['raw'], sample_filename)
        ]
        
        # Add more possible locations
        if 'raw' in paths:
            if not os.path.isabs(paths['raw']):
                # If it's a relative path, make it absolute
                possible_locations.append(os.path.join(project_root, paths['raw'], sample_filename))
                possible_locations.append(os.path.abspath(os.path.join(paths['raw'], sample_filename)))
        
        # List available files in common directories
        print("\nSearching for input files:")
        for dir_to_check in ["data/raw/samples", "data/raw", paths.get('raw', '')]:
            if os.path.exists(dir_to_check):
                print(f"Files in {dir_to_check}:")
                for f in os.listdir(dir_to_check):
                    print(f"  - {f}")
            else:
                print(f"Directory {dir_to_check} does not exist")
        
        # Find the first existing file
        input_file = None
        for loc in possible_locations:
            print(f"Checking location: {loc}")
            if os.path.exists(loc):
                input_file = loc
                print(f"Found file at: {input_file}")
                break
                
        if not input_file:
            print("Error: Could not find input file in any expected location")
            print("Please specify the full path to your CSV file")
            
            # Ask user for file path (optional)
            user_path = input("Enter the full path to your CSV file: ").strip()
            if os.path.exists(user_path):
                input_file = user_path
            else:
                return
            
        # Set up output path
        output_dir = os.path.join(project_root, "data", "processed")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        output_file = os.path.join(output_dir, "test_output.json")
        
        print(f"\nTesting file conversion from {input_file} to {output_file}")
        
        # Initialize the converter pipeline
        pipeline = CitationConverterPipeline()
        
        # Convert the file
        results = pipeline.convert_csv_file(str(input_file), str(output_file))
        
        print(f"Converted {len(results)} records")
        print(f"Output saved to: {output_file}")
        print("\nFile conversion test completed successfully!")
        
    except Exception as e:
        print(f"Error during file test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Running IsisCB conversion tests...\n")
    print("Project root:", project_root)
    
    print("\n=== Single Record Conversion Test ===")
    test_single_record_conversion()
    
    print("\n=== File Conversion Test ===")
    test_file_conversion()