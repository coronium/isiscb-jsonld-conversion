#!/usr/bin/env python
"""
Script to validate JSON-LD files against IsisCB schemas.

Usage:
    python validate_jsonld.py input_file.json [output_report.json]
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add project root to path
def get_project_root():
    """Return the absolute path to the project root directory."""
    current_path = Path(os.path.abspath(__file__))
    # Navigate up to project root: scripts -> src -> project_root
    return str(current_path.parents[1])

# Add project root to Python path if not already there
project_root = get_project_root()
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import from the project
from src.isiscb.validators.json_ld_validator import JSONLDValidator
from src.isiscb.utils.paths import ensure_project_in_path, find_data_file

# Ensure the project is in path
ensure_project_in_path()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('isiscb_validation')

def validate_file(input_file: str, output_file: str = None) -> bool:
    """
    Validate a JSON-LD file against schemas.
    
    Args:
        input_file: Path to JSON-LD file to validate
        output_file: Optional path to save validation report
        
    Returns:
        True if validation passed, False otherwise
    """
    # Initialize validator with schemas directory
    schemas_dir = os.path.join(project_root, 'src', 'isiscb', 'schemas')
    validator = JSONLDValidator(schemas_dir)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        return False
    
    # Load JSON-LD file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both single document and array of documents
        documents = data if isinstance(data, list) else [data]
        logger.info(f"Loaded {len(documents)} document(s) from {input_file}")
        
        # Validate documents
        results = validator.validate_documents(documents)
        
        # Display validation summary
        logger.info(f"Validation results for {input_file}:")
        logger.info(f"  Total documents: {results['total']}")
        logger.info(f"  Valid documents: {results['valid']}")
        logger.info(f"  Invalid documents: {results['invalid']}")
        
        # Save validation report if output file specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            logger.info(f"Validation report saved to {output_file}")
        
        # Display details of validation errors
        if results['invalid'] > 0:
            logger.info("Validation errors:")
            for doc_id, errors in results['errors'].items():
                logger.info(f"  Document: {doc_id}")
                for error in errors:
                    logger.info(f"    - {error}")
        
        return results['invalid'] == 0
        
    except Exception as e:
        logger.error(f"Error validating file: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def main():
    """Main function to run validation."""
    # Check command line arguments
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} input_file.json [output_report.json]")
        sys.exit(1)
    
    # Get input and output paths
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # If input file is not an absolute path, try to find it
    if not os.path.isabs(input_file):
        found_file = find_data_file(input_file)
        if found_file:
            input_file = found_file
    
    # Validate the file
    success = validate_file(input_file, output_file)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()