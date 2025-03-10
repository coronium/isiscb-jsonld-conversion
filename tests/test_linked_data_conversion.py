#!/usr/bin/env python
"""
Test script for the LinkedDataConverter.

This script tests the functionality of the LinkedDataConverter.
"""

import os
import sys
import json
import logging
import pandas as pd
from pathlib import Path

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('isiscb_conversion')

def test_linked_data_converter():
    """Test function for the LinkedDataConverter."""
    # Import here to ensure paths are set up
    from src.isiscb.converters.common.linked_data import LinkedDataConverter
    
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
    
    # Test case 4: Input with malformed entry
    test_input_4 = "LinkedData_ID LED544064469 || Status Active || Type DNB URN http://d-nb.info/gnd/133578771/about/html || ResourceName Deutsche Nationalbibliothek GND"
    result_4 = converter.convert(test_input_4, "CBA000004")
    
    print("\nTest Case 4 Result (Malformed Entry):")
    print(json.dumps(result_4, indent=2))
    
    # Test case 5: Real data from documentation
    test_input_5 = "LinkedData_ID LED544064469 || Status Active || Type DNB || URN http://d-nb.info/gnd/133578771/about/html || ResourceName Deutsche Nationalbibliothek GND Authority file || URL , LinkedData_ID LED257502971 || Status Active || Type VIAF || URN http://viaf.org/viaf/18147423004844880849 || ResourceName VIAF || URL , LinkedData_ID LED652197398 || Status Active || Type VIAF || URN http://viaf.org/viaf/1327145857114622922132 || ResourceName VIAF || URL"
    result_5 = converter.convert(test_input_5, "CBA000005")
    
    print("\nTest Case 5 Result (Real Data):")
    print(json.dumps(result_5, indent=2))

if __name__ == "__main__":
    print("Testing LinkedDataConverter...")
    test_linked_data_converter()
    print("\nTesting complete!")