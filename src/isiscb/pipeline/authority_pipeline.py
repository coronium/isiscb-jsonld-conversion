"""
Authority conversion pipeline for IsisCB JSON-LD Conversion Project.

This module orchestrates the conversion of authority records from CSV to JSON-LD format.
"""

import pandas as pd
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# First ensure project root is in path
def get_project_root():
    """Return the absolute path to the project root directory."""
    current_path = Path(os.path.abspath(__file__))
    # Navigate up 3 levels: pipeline -> isiscb -> src -> project_root
    return str(current_path.parents[2])

# Add project root to Python path if not already there
project_root = get_project_root()
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import utility functions - these don't depend on schema_mappings
from src.isiscb.utils.paths import ensure_project_in_path, get_data_paths

# Ensure project is in path again to be extra safe
ensure_project_in_path()

# Import converters with correct relative paths
from ..converters.schema_mappings import get_base_context
from ..converters.common.identifier import RecordIdConverter, RedirectConverter
from ..converters.common.types import RecordTypeConverter, RecordNatureConverter
from ..converters.common.linked_data import LinkedDataConverter  
from ..converters.common.attributes import AttributesConverter
from ..converters.authority.name import NameConverter
from ..converters.authority.description import DescriptionConverter
from ..converters.authority.classification import ClassificationConverter
from ..converters.authority.metadata import AuthorityMetadataConverter
from ..converters.authority.related_authorities import AuthorityRelatedAuthoritiesConverter

# Import validator
from ..validators.json_ld_validator import JSONLDValidator, validate_json_ld

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('isiscb_conversion')

class AuthorityConverterPipeline:
    """Pipeline for converting IsisCB authority data to JSON-LD."""
    
    def __init__(self, validate: bool = True):
        """
        Initialize the authority converter pipeline.
        
        Args:
            validate: Whether to validate the output JSON-LD (default: True)
        """
        # Initialize converters
        self.converters = {
            'record_id': RecordIdConverter(entity_type='authority'),
            'record_type': RecordTypeConverter(),
            'record_nature': RecordNatureConverter(),
            'name': NameConverter(),
            'description': DescriptionConverter(),
            'classification': ClassificationConverter(),
            'linked_data': LinkedDataConverter(),
            'attributes': AttributesConverter(),
            'redirect': RedirectConverter(),
            'metadata': AuthorityMetadataConverter(),
            'related_authorities': AuthorityRelatedAuthoritiesConverter()
        }
        
        # Use the centralized context mapping
        self.base_context = get_base_context()
        
        # Store the data paths
        self.data_paths = get_data_paths()
        logger.info(f"Using data paths: {self.data_paths}")
        
        # Validator settings
        self.validate = validate
        if validate:
            # Try to load schemas from the schemas directory
            schemas_dir = os.path.join(get_project_root(), 'src', 'isiscb', 'schemas')
            self.validator = JSONLDValidator(schemas_dir)
    
    def convert_row(self, row: pd.Series) -> Dict:
        """
        Convert a single authority row to JSON-LD.
        
        Args:
            row: DataFrame row containing authority data
            
        Returns:
            Dict containing the JSON-LD representation
        """
        # Get record ID for logging and reference
        record_id = row.get('Record ID', 'unknown')
        
        # Initialize with context
        jsonld = {"@context": self.base_context}
        
        # Apply record ID converter first to establish the @id
        if 'Record ID' in row:
            jsonld.update(self.converters['record_id'].convert(row['Record ID'], record_id))
        
        # Apply type converter
        if 'Record Type' in row:
            jsonld.update(self.converters['record_type'].convert(row['Record Type'], record_id))
        
        # Apply Record Nature converter
        if 'Record Nature' in row:
            jsonld.update(self.converters['record_nature'].convert(row['Record Nature'], record_id))
        
        # Apply Redirect converter if applicable
        if 'Redirect' in row and row['Redirect'] and not pd.isna(row['Redirect']):
            jsonld.update(self.converters['redirect'].convert(row['Redirect'], record_id))
        
        # Apply name converter
        name_fields = {
            'Name': row.get('Name'),
            'Last Name': row.get('Last Name'),
            'First Name': row.get('First Name'),
            'Name Suffix': row.get('Name Suffix'),
            'Name Preferred': row.get('Name Preferred'),
            'Record Type': row.get('Record Type')  # Needed to determine handling
        }
        jsonld.update(self.converters['name'].convert(name_fields, record_id))
        
        # Apply description converter
        if 'Description' in row:
            jsonld.update(self.converters['description'].convert(row['Description'], record_id))
        
        # Apply classification converter
        classification_fields = {
            'Classification System': row.get('Classification System'),
            'Classification Code': row.get('Classification Code'),
            'Record Type': row.get('Record Type')  # Needed to determine handling
        }
        jsonld.update(self.converters['classification'].convert(classification_fields, record_id))
        
        # Apply linked data converter
        if 'Linked Data' in row:
            jsonld.update(self.converters['linked_data'].convert(row['Linked Data'], record_id))
        
        # Apply attributes converter
        if 'Attributes' in row:
            jsonld.update(self.converters['attributes'].convert(row['Attributes'], record_id))
        
        # Apply related authorities converter
        if 'Related Authorities' in row:
            jsonld.update(self.converters['related_authorities'].convert(row['Related Authorities'], record_id))
        
        # Apply metadata converter
        metadata_fields = {
            'Staff Notes': row.get('Staff Notes'),
            'Record History': row.get('Record History'),
            'Created Date': row.get('Created Date'),
            'Modified Date': row.get('Modified Date'),
            'Creator': row.get('Creator'),
            'Modifier': row.get('Modifier'),
            'Related Citations Count': row.get('Related Citations Count')
        }
        jsonld.update(self.converters['metadata'].convert(metadata_fields, record_id))
        
        # Validate the JSON-LD if enabled
        if self.validate:
            is_valid, errors = self.validator.validate_document(jsonld, 'authority')
            if not is_valid:
                logger.warning(f"Validation errors for record {record_id}:")
                for error in errors:
                    logger.warning(f"  - {error}")
        
        return jsonld
    
    def convert_dataframe(self, df: pd.DataFrame, output_file: Optional[str] = None) -> Tuple[List[Dict], Dict[str, Any]]:
        """
        Convert a DataFrame of authority records to JSON-LD.
        
        Args:
            df: DataFrame containing authority records
            output_file: Optional path to save the JSON-LD output
            
        Returns:
            Tuple of (json_ld_documents, validation_results)
        """
        jsonld_documents = []
        validation_results = {
            'total': 0,
            'valid': 0,
            'invalid': 0,
            'errors': {}
        }
        
        for _, row in df.iterrows():
            record_id = row.get('Record ID', 'unknown')
            validation_results['total'] += 1
            
            try:
                jsonld = self.convert_row(row)
                jsonld_documents.append(jsonld)
                
                # Validate if enabled
                if self.validate:
                    is_valid, errors = self.validator.validate_document(jsonld, 'authority')
                    if is_valid:
                        validation_results['valid'] += 1
                    else:
                        validation_results['invalid'] += 1
                        validation_results['errors'][record_id] = errors
                else:
                    validation_results['valid'] += 1  # Count as valid if validation is disabled
                
            except Exception as e:
                logger.error(f"Error converting record {record_id}: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                validation_results['invalid'] += 1
                validation_results['errors'][record_id] = [str(e)]
        
        if output_file:
            # Convert to absolute path if it's not already
            if not os.path.isabs(output_file):
                output_file = os.path.join(project_root, output_file)
                
            # Create directory if it doesn't exist
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(jsonld_documents, f, ensure_ascii=False, indent=2)
                logger.info(f"Saved {len(jsonld_documents)} JSON-LD documents to {output_file}")
                
                # Write validation report if validation is enabled
                if self.validate and validation_results['invalid'] > 0:
                    validation_file = os.path.splitext(output_file)[0] + '_validation.json'
                    with open(validation_file, 'w', encoding='utf-8') as f:
                        json.dump(validation_results, f, ensure_ascii=False, indent=2)
                    logger.info(f"Saved validation report to {validation_file}")
                    
            except Exception as e:
                logger.error(f"Error saving output file {output_file}: {str(e)}")
        
        return jsonld_documents, validation_results
    
    def convert_csv_file(self, input_file: str, output_file: Optional[str] = None) -> Tuple[List[Dict], Dict[str, Any]]:
        """
        Convert a CSV file of authority records to JSON-LD.
        
        Args:
            input_file: Path to the input CSV file
            output_file: Optional path to save the JSON-LD output
            
        Returns:
            Tuple of (json_ld_documents, validation_results)
        """
        try:
            # Convert to absolute path if it's not already
            if not os.path.isabs(input_file):
                # Try to locate the file if not an absolute path
                if os.path.exists(input_file):
                    input_file = os.path.abspath(input_file)
                elif os.path.exists(os.path.join(project_root, input_file)):
                    input_file = os.path.join(project_root, input_file)
                elif 'raw_samples' in self.data_paths and os.path.exists(os.path.join(self.data_paths['raw_samples'], os.path.basename(input_file))):
                    input_file = os.path.join(self.data_paths['raw_samples'], os.path.basename(input_file))
                elif 'raw' in self.data_paths and os.path.exists(os.path.join(self.data_paths['raw'], os.path.basename(input_file))):
                    input_file = os.path.join(self.data_paths['raw'], os.path.basename(input_file))
            
            # Check if the file exists
            if not os.path.exists(input_file):
                logger.error(f"Input file not found: {input_file}")
                return [], {'total': 0, 'valid': 0, 'invalid': 0, 'errors': {'file_error': 'File not found'}}
                
            logger.info(f"Reading input file: {input_file}")
            df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
            logger.info(f"Loaded {len(df)} records from {input_file}")
            
            # If output file is not specified, create one in the processed folder
            if not output_file and 'processed' in self.data_paths:
                input_basename = os.path.basename(input_file)
                output_file = os.path.join(
                    self.data_paths['processed'], 
                    os.path.splitext(input_basename)[0] + '.json'
                )
                logger.info(f"Auto-generated output file path: {output_file}")
            
            return self.convert_dataframe(df, output_file)
        except Exception as e:
            logger.error(f"Error processing file {input_file}: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return [], {'total': 0, 'valid': 0, 'invalid': 0, 'errors': {'file_error': str(e)}}


# If this module is run directly, perform a test conversion
if __name__ == "__main__":
    logger.info("Running authority pipeline directly for testing")
    
    # Ensure project is in path
    ensure_project_in_path()
    
    # Import utility for finding sample data
    from src.isiscb.utils.paths import find_data_file
    
    # Try to locate a sample file
    sample_files = [
        "CB Authoritiesall2024.10.16.sample_1000.csv",
        "authorities_sample.csv"
    ]
    
    input_file = None
    for sample_file in sample_files:
        found_file = find_data_file(sample_file)
        if found_file:
            input_file = found_file
            break
    
    if not input_file:
        logger.error("No sample authority files found. Exiting.")
        sys.exit(1)
    
    # Run the conversion with validation
    pipeline = AuthorityConverterPipeline(validate=True)
    logger.info(f"Converting sample file: {input_file}")
    
    # Output to a test file in the processed directory
    if 'processed' in pipeline.data_paths:
        output_file = os.path.join(
            pipeline.data_paths['processed'],
            'test_authority_with_validation.json'
        )
    else:
        output_file = 'test_authority_with_validation.json'
    
    results, validation = pipeline.convert_csv_file(input_file, output_file)
    
    # Print validation summary
    logger.info(f"Conversion completed: {len(results)} records processed")
    logger.info(f"Validation results: {validation['valid']} valid, {validation['invalid']} invalid")
    if validation['invalid'] > 0:
        logger.info(f"Validation errors were found. See {os.path.splitext(output_file)[0]}_validation.json for details")