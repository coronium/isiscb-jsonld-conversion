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

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Now import from the proper module paths
from src.isiscb.pipeline.citation_pipeline import CitationConverterPipeline
from src.isiscb.pipeline.authority_pipeline import AuthorityConverterPipeline
from src.isiscb.utils.data_loader import load_citation_data, load_authorities_data, get_paths
from src.isiscb.converters.common.linked_data import LinkedDataConverter

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('isiscb_conversion')

def test_single_citation_conversion():
    """Test converting a single citation record and print the result."""
    # Load sample data
    try:
        # Pass the absolute path to config.yml to data_loader functions
        config_path = os.path.abspath(os.path.join(project_root, 'config.yml'))
        df = load_citation_data(config_path=config_path)
        if df.empty:
            print("Error: Sample citation data is empty")
            return
        
        # Get the first record for testing
        sample_record = df.iloc[0]
        record_id = sample_record.get('Record ID', 'unknown')
        
        print(f"Testing conversion of citation record: {record_id}")
        
        # Initialize the converter pipeline
        pipeline = CitationConverterPipeline()
        
        # Convert the single record
        result = pipeline.convert_row(sample_record)
        
        # Pretty print the result
        print("\nConverted JSON-LD:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("\nCitation conversion test completed successfully!")
        
    except Exception as e:
        print(f"Error during citation test: {str(e)}")
        import traceback
        traceback.print_exc()

def test_single_authority_conversion():
    """Test converting a single authority record and print the result."""
    # Load sample data
    try:
        # Pass the absolute path to config.yml to data_loader functions
        config_path = os.path.abspath(os.path.join(project_root, 'config.yml'))
        df = load_authorities_data(config_path=config_path)
        if df.empty:
            print("Error: Sample authority data is empty")
            return
        
        # Get the first record for testing
        sample_record = df.iloc[0]
        record_id = sample_record.get('Record ID', 'unknown')
        
        print(f"Testing conversion of authority record: {record_id}")
        
        # Initialize the converter pipeline
        pipeline = AuthorityConverterPipeline()
        
        # Convert the single record
        result = pipeline.convert_row(sample_record)
        
        # Pretty print the result
        print("\nConverted JSON-LD:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("\nAuthority conversion test completed successfully!")
        
    except Exception as e:
        print(f"Error during authority test: {str(e)}")
        import traceback
        traceback.print_exc()

def test_citation_file_conversion():
    """Test converting a citation file and saving the output."""
    try:
        # Get paths using absolute path to config.yml
        config_path = os.path.abspath(os.path.join(project_root, 'config.yml'))
        paths = get_paths(config_path)
        
        # Print debugging information
        print(f"Current working directory: {os.getcwd()}")
        print(f"Project root: {project_root}")
        print(f"Paths from config: {paths}")
        
        # Sample filenames to check
        sample_filenames = [
            # "IsisCB citation sample.csv", 
            "IsisCB authorities sample 1000.csv",
            # "explore 500 sample.csv"
        ]
        
        # Look for first available sample file
        input_file = find_sample_file(sample_filenames, paths)
        
        if not input_file:
            # Ask user for file path
            user_path = input("Enter the full path to your CSV citation file: ").strip()
            if os.path.exists(user_path):
                input_file = user_path
            else:
                print(f"File not found: {user_path}")
                return
            
        # Set up output path
        output_dir = os.path.join(project_root, "data", "processed")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "test_citation_output.json")
        
        print(f"\nTesting citation file conversion from {input_file} to {output_file}")
        
        # Initialize the converter pipeline
        pipeline = CitationConverterPipeline()
        
        # Convert the file
        results, validation = pipeline.convert_csv_file(str(input_file), str(output_file))
        
        print(f"Converted {len(results)} citation records")
        print(f"Output saved to: {output_file}")
        print("\nCitation file conversion test completed successfully!")
        
    except Exception as e:
        print(f"Error during citation file test: {str(e)}")
        import traceback
        traceback.print_exc()

def test_authority_file_conversion():
    """Test converting an authority file and saving the output."""
    try:
        # Get paths using absolute path to config.yml
        config_path = os.path.abspath(os.path.join(project_root, 'config.yml'))
        paths = get_paths(config_path)
        
        # Print debugging information
        print(f"Current working directory: {os.getcwd()}")
        print(f"Project root: {project_root}")
        print(f"Paths from config: {paths}")
        
        # Authority Sample filenames to check
        sample_filenames = [
            "IsisCB authorities sample 1000.csv",
            "authorities_sample.csv"
        ]
        
        # Look for first available sample file
        input_file = find_sample_file(sample_filenames, paths)
        
        if not input_file:
            # Ask user for file path
            user_path = input("Enter the full path to your CSV authority file: ").strip()
            if os.path.exists(user_path):
                input_file = user_path
            else:
                print(f"File not found: {user_path}")
                return
            
        # Set up output path
        output_dir = os.path.join(project_root, "data", "processed")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "test_authority_output.json")
        
        print(f"\nTesting authority file conversion from {input_file} to {output_file}")
        
        # Initialize the converter pipeline
        pipeline = AuthorityConverterPipeline()
        
        # Convert the file
        results, validation = pipeline.convert_csv_file(str(input_file), str(output_file))
        
        print(f"Converted {len(results)} authority records")
        print(f"Output saved to: {output_file}")
        print("\nAuthority file conversion test completed successfully!")
        
    except Exception as e:
        print(f"Error during authority file test: {str(e)}")
        import traceback
        traceback.print_exc()

def find_sample_file(filenames, paths):
    """Helper function to find a sample file."""
    for filename in filenames:
        # Check in data/raw/samples directory
        potential_path = os.path.join(project_root, "data", "raw", "samples", filename)
        if os.path.exists(potential_path):
            return potential_path
                
        # Check in paths['raw'] directory
        if 'raw' in paths:
            raw_path = paths['raw']
            # If it's a relative path, make it absolute
            if not os.path.isabs(raw_path):
                raw_path = os.path.join(project_root, raw_path)
            potential_path = os.path.join(raw_path, filename)
            if os.path.exists(potential_path):
                return potential_path
    
    # If no sample file found, list available files to help debugging
    print("\nCould not find any sample files. Available files:")
    for dir_to_check in ["data/raw/samples", "data/raw", paths.get('raw', '')]:
        check_path = os.path.join(project_root, dir_to_check) if not os.path.isabs(dir_to_check) else dir_to_check
        if os.path.exists(check_path):
            print(f"Files in {check_path}:")
            for f in os.listdir(check_path):
                print(f"  - {f}")
        else:
            print(f"Directory {check_path} does not exist")
    
    return None

def test_linked_data_converter():
    """Test function for the LinkedDataConverter."""
    converter = LinkedDataConverter()
    
    # Test case 1: Simple linked data with one entry
    test_input_1 = "LinkedData_ID LED544064469 || Status Active || Type DNB || URN http://d-nb.info/gnd/133578771/about/html || ResourceName Deutsche Nationalbibliothek GND Authority file || URL"
    result_1 = converter.convert(test_input_1, "CBA000001")
    
    print("Test Case 1 Result:")
    print(json.dumps(result_1, indent=2))
    
    # Test case 2: Multiple linked data entries
    test_input_2 = "LinkedData_ID LED257502971 || Status Active || Type VIAF || URN http://viaf.org/viaf/18147423004844880849 || ResourceName VIAF || URL // LinkedData_ID LED652197398 || Status Active || Type VIAF || URN http://viaf.org/viaf/1327145857114622922132 || ResourceName VIAF || URL"
    result_2 = converter.convert(test_input_2, "CBA000002")
    
    print("\nTest Case 2 Result:")
    print(json.dumps(result_2, indent=2))
    
    # Test case 3: Empty input
    test_input_3 = ""
    result_3 = converter.convert(test_input_3, "CBA000003")
    
    print("\nTest Case 3 Result:")
    print(json.dumps(result_3, indent=2))

# Run the test if this file is executed directly
if __name__ == "__main__":
    print("Running IsisCB conversion tests...\n")
    
    # print("\n=== Citation Single Record Conversion Test ===")
    # test_single_citation_conversion()
    
    # print("\n=== Authority Single Record Conversion Test ===")
    # test_single_authority_conversion()
    
    # print("\n=== Citation File Conversion Test ===")
    # test_citation_file_conversion()
    
    print("\n=== Authority File Conversion Test ===")
    test_authority_file_conversion()