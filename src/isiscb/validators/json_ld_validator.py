"""
JSON-LD Schema validator for IsisCB conversion project.

This module provides validation functionality for JSON-LD documents
against defined schemas and best practices.
"""

import json
import logging
import os
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path
import jsonschema
from jsonschema import validate, ValidationError, Draft7Validator

# Set up logging
logger = logging.getLogger('isiscb_validation')

class JSONLDValidator:
    """Validator for JSON-LD documents produced by the IsisCB conversion process."""
    
    def __init__(self, schema_dir: Optional[str] = None):
        """
        Initialize the validator with schemas.
        
        Args:
            schema_dir: Optional directory containing schema files
        """
        self.schema_dir = schema_dir
        self.schemas = {}
        self.load_schemas()
    
    def load_schemas(self):
        """Load schemas from schema directory if provided, or use default schemas."""
        if self.schema_dir and os.path.isdir(self.schema_dir):
            # Load schemas from files
            schema_files = [f for f in os.listdir(self.schema_dir) if f.endswith('.json')]
            for schema_file in schema_files:
                schema_path = os.path.join(self.schema_dir, schema_file)
                try:
                    with open(schema_path, 'r', encoding='utf-8') as f:
                        schema = json.load(f)
                        schema_id = Path(schema_file).stem  # Use filename without extension as ID
                        self.schemas[schema_id] = schema
                    logger.info(f"Loaded schema: {schema_id}")
                except Exception as e:
                    logger.error(f"Error loading schema {schema_file}: {str(e)}")
        else:
            # Define default schemas inline
            self.schemas = self._get_default_schemas()
            logger.info(f"Using default schemas: {', '.join(self.schemas.keys())}")
    
    def _get_default_schemas(self) -> Dict[str, Dict]:
        """
        Get default schemas for validation.
        
        Returns:
            Dictionary of schema ID to schema definition
        """
        return {
            'citation': {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": "IsisCB Citation Schema",
                "type": "object",
                "required": ["@context", "@id", "@type"],
                "properties": {
                    "@context": {
                        "type": ["object", "array", "string"]
                    },
                    "@id": {
                        "type": "string",
                        "format": "uri"
                    },
                    "@type": {
                        "oneOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}}
                        ]
                    },
                    "dc:title": {
                        "type": "string"
                    },
                    "dc:creator": {
                        "oneOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "object"}
                        ]
                    },
                    "dc:date": {
                        "type": "string"
                    },
                    "isiscb:recordID": {
                        "type": "string",
                        "pattern": "^CBB\\d+"
                    }
                },
                "additionalProperties": True
            },
            'authority': {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": "IsisCB Authority Schema",
                "type": "object",
                "required": ["@context", "@id", "@type"],
                "properties": {
                    "@context": {
                        "type": ["object", "array", "string"]
                    },
                    "@id": {
                        "type": "string",
                        "format": "uri"
                    },
                    "@type": {
                        "oneOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}}
                        ]
                    },
                    "name": {
                        "type": "string"
                    },
                    "isiscb:recordType": {
                        "type": "string"
                    },
                    "isiscb:recordID": {
                        "type": "string",
                        "pattern": "^CBA\\d+"
                    }
                },
                "additionalProperties": True
            }
        }
    
    def validate_document(self, document: Dict, schema_id: Optional[str] = None) -> Tuple[bool, List[str]]:
        """
        Validate a single JSON-LD document against a schema.
        
        Args:
            document: JSON-LD document to validate
            schema_id: Optional ID of the schema to use (if None, will be inferred from document)
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        # If schema_id not provided, try to infer from document
        if not schema_id:
            record_id = document.get('@id', '')
            if 'citation' in record_id or record_id.startswith('https://data.isiscb.org/citation/'):
                schema_id = 'citation'
            elif 'authority' in record_id or record_id.startswith('https://data.isiscb.org/authority/'):
                schema_id = 'authority'
            else:
                return False, ["Unable to determine document type for validation"]
        
        # Check if schema exists
        if schema_id not in self.schemas:
            return False, [f"Schema '{schema_id}' not found"]
        
        schema = self.schemas[schema_id]
        validator = Draft7Validator(schema)
        
        # Collect all validation errors
        errors = list(validator.iter_errors(document))
        if errors:
            error_messages = []
            for error in errors:
                path = '/'.join(str(p) for p in error.path) if error.path else '(root)'
                error_messages.append(f"{path}: {error.message}")
            return False, error_messages
            
        return True, []
    
    def validate_documents(self, documents: List[Dict], schema_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a list of JSON-LD documents.
        
        Args:
            documents: List of JSON-LD documents to validate
            schema_id: Optional ID of the schema to use (if None, will be inferred from each document)
            
        Returns:
            Dict with validation results
        """
        results = {
            'total': len(documents),
            'valid': 0,
            'invalid': 0,
            'errors': {}
        }
        
        for i, doc in enumerate(documents):
            # Get document ID for reference
            doc_id = doc.get('@id', f"document_{i}")
            
            # Validate document
            is_valid, errors = self.validate_document(doc, schema_id)
            
            # Update results
            if is_valid:
                results['valid'] += 1
            else:
                results['invalid'] += 1
                results['errors'][doc_id] = errors
        
        return results
    
    def validate_file(self, file_path: str, schema_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate JSON-LD documents from a file.
        
        Args:
            file_path: Path to JSON-LD file
            schema_id: Optional ID of the schema to use
            
        Returns:
            Dict with validation results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Handle both single document and array of documents
            documents = data if isinstance(data, list) else [data]
            
            return self.validate_documents(documents, schema_id)
            
        except Exception as e:
            return {
                'total': 0,
                'valid': 0,
                'invalid': 0,
                'errors': {
                    'file_error': str(e)
                }
            }
    
    def validate_context(self, context: Union[Dict, List, str]) -> Tuple[bool, List[str]]:
        """
        Validate a JSON-LD @context for good practices.
        
        Args:
            context: JSON-LD @context object, array or string
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check if context is a string (URI)
        if isinstance(context, str):
            # Basic URI validation
            if not context.startswith(('http://', 'https://')):
                errors.append(f"Context URI should start with http:// or https://: {context}")
            return len(errors) == 0, errors
            
        # Check if context is an array
        if isinstance(context, list):
            # Validate each item in the array
            for i, item in enumerate(context):
                is_valid, item_errors = self.validate_context(item)
                if not is_valid:
                    errors.extend([f"Context[{i}]: {err}" for err in item_errors])
            return len(errors) == 0, errors
            
        # Check if context is an object
        if isinstance(context, dict):
            # Check for namespace definitions
            for key, value in context.items():
                if not key.startswith('@'):  # Skip @vocab, @language, etc.
                    if isinstance(value, str):
                        # Namespace URI validation
                        if not value.startswith(('http://', 'https://')):
                            errors.append(f"Namespace URI for '{key}' should start with http:// or https://: {value}")
                    elif isinstance(value, dict):
                        # Property definition validation
                        if '@id' not in value:
                            errors.append(f"Property definition for '{key}' is missing @id")
                        elif not isinstance(value['@id'], str):
                            errors.append(f"@id for property '{key}' should be a string")
                        elif not value['@id'].startswith(('http://', 'https://')) and ':' in value['@id']:
                            prefix = value['@id'].split(':')[0]
                            if prefix not in context and prefix not in ['rdfs', 'xsd', 'dc', 'dcterms', 'schema', 'skos']:
                                errors.append(f"Undefined prefix '{prefix}' in @id '{value['@id']}' for property '{key}'")
            
            return len(errors) == 0, errors
            
        # Invalid context type
        return False, [f"Invalid @context type: {type(context).__name__}"]


# Convenience function to validate a single document
def validate_json_ld(document: Dict, schema_id: Optional[str] = None) -> Tuple[bool, List[str]]:
    """
    Validate a JSON-LD document using default schemas.
    
    Args:
        document: JSON-LD document to validate
        schema_id: Optional schema ID to use
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    validator = JSONLDValidator()
    return validator.validate_document(document, schema_id)


# If run directly, test validation with a sample document
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create sample document
    sample_citation = {
        "@context": {
            "dc": "http://purl.org/dc/elements/1.1/",
            "isiscb": "https://data.isiscb.org/vocabulary/"
        },
        "@id": "https://data.isiscb.org/citation/CBB001180697",
        "@type": ["bibo:Book", "isiscb:Citation"],
        "dc:title": "The giant leap: A chronology of Ohio aerospace events",
        "dc:creator": "Smith, John",
        "dc:date": "1969",
        "isiscb:recordID": "CBB001180697"
    }
    
    # Validate sample document
    validator = JSONLDValidator()
    is_valid, errors = validator.validate_document(sample_citation, 'citation')
    
    # Print results
    if is_valid:
        print("Validation successful!")
    else:
        print("Validation errors:")
        for error in errors:
            print(f"- {error}")