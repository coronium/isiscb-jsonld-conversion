"""
Citation conversion pipeline for IsisCB JSON-LD Conversion Project.

This module orchestrates the conversion of citation records from CSV to JSON-LD format.
"""

import pandas as pd
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import converters
from ..converters.common.identifier import RecordIdConverter
from ..converters.common.types import RecordTypeConverter, RecordNatureConverter
from ..converters.citation.title import TitleConverter

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('isiscb_conversion')

class CitationConverterPipeline:
    """Pipeline for converting IsisCB citation data to JSON-LD."""
    
    def __init__(self):
        """Initialize the citation converter pipeline."""
        # Initialize converters
        self.converters = {
            'record_id': RecordIdConverter(entity_type='citation'),
            'record_type': RecordTypeConverter(),
            'record_nature': RecordNatureConverter(),
            'title': TitleConverter(),
            # Add more converters as they are implemented
        }
        
        # Define the base JSON-LD context
        self.base_context = {
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/",
            "schema": "http://schema.org/",
            "bibo": "http://purl.org/ontology/bibo/",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "isiscb": "https://data.isiscb.org/context/"
        }
    
    def convert_row(self, row: pd.Series) -> Dict:
        """
        Convert a single citation row to JSON-LD.
        
        Args:
            row: DataFrame row containing citation data
            
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
        
        # Apply nature converter
        if 'Record Nature' in row:
            jsonld.update(self.converters['record_nature'].convert(row['Record Nature'], record_id))
        
        # Apply title converter
        if 'Title' in row:
            jsonld.update(self.converters['title'].convert(row['Title'], record_id))
        
        # Additional converters will be applied here as they are implemented
        
        return jsonld
    
    def convert_dataframe(self, df: pd.DataFrame, output_file: Optional[str] = None) -> List[Dict]:
        """
        Convert a DataFrame of citation records to JSON-LD.
        
        Args:
            df: DataFrame containing citation records
            output_file: Optional path to save the JSON-LD output
            
        Returns:
            List of JSON-LD documents
        """
        jsonld_documents = []
        
        for _, row in df.iterrows():
            record_id = row.get('Record ID', 'unknown')
            
            try:
                jsonld = self.convert_row(row)
                jsonld_documents.append(jsonld)
            except Exception as e:
                logger.error(f"Error converting record {record_id}: {str(e)}")
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(jsonld_documents, f, ensure_ascii=False, indent=2)
                logger.info(f"Saved {len(jsonld_documents)} JSON-LD documents to {output_file}")
            except Exception as e:
                logger.error(f"Error saving output file {output_file}: {str(e)}")
        
        return jsonld_documents
    
    def convert_csv_file(self, input_file: str, output_file: Optional[str] = None) -> List[Dict]:
        """
        Convert a CSV file of citation records to JSON-LD.
        
        Args:
            input_file: Path to the input CSV file
            output_file: Optional path to save the JSON-LD output
            
        Returns:
            List of JSON-LD documents
        """
        try:
            df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
            logger.info(f"Loaded {len(df)} records from {input_file}")
            return self.convert_dataframe(df, output_file)
        except Exception as e:
            logger.error(f"Error processing file {input_file}: {str(e)}")
            return []


# Convenience function for direct use
def convert_citations_to_jsonld(input_file: str, output_file: Optional[str] = None) -> List[Dict]:
    """
    Convert citations from a CSV file to JSON-LD.
    
    Args:
        input_file: Path to the input CSV file
        output_file: Optional path to save the JSON-LD output
        
    Returns:
        List of JSON-LD documents
    """
    pipeline = CitationConverterPipeline()
    return pipeline.convert_csv_file(input_file, output_file)