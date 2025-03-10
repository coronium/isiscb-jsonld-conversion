"""
Type field converters for IsisCB JSON-LD conversion.

This module provides converters for Record Type and related fields.
"""

import logging
from typing import Dict, List

from ..base import BaseConverter
from ..schema_mappings import AUTHORITY_TYPE_MAPPING, CITATION_TYPE_MAPPING, RECORD_STATUS_MAPPING

logger = logging.getLogger('isiscb_conversion')

class RecordTypeConverter(BaseConverter):
    """Converter for Record Type fields."""
    
    def __init__(self, field_name: str = "Record Type"):
        """Initialize the Record Type converter."""
        super().__init__(field_name)
    
    def _convert_impl(self, value: str, record_id: str) -> Dict:
        """
        Convert Record Type to JSON-LD format.
        
        Args:
            value: The raw Record Type value
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of the Record Type
        """
        if not value:
            logger.warning(f"Empty Record Type found for record {record_id}")
            return {"@type": "isiscb:UnknownType"}
        
        # Determine if this is an authority or citation based on record ID pattern
        if record_id.startswith("CBA"):
            type_mapping = AUTHORITY_TYPE_MAPPING
        else:
            type_mapping = CITATION_TYPE_MAPPING
        
        # Get standard types or use a default type
        standard_types = type_mapping.get(value, ["isiscb:UnmappedType"])
        
        # Add custom IsisCB type
        custom_type = f"isiscb:{value.replace(' ', '')}"
        
        # Combine all types with custom type last
        all_types = standard_types + [custom_type]
        
        return {"@type": all_types}


class RecordNatureConverter(BaseConverter):
    """Converter for Record Nature fields."""
    
    def __init__(self, field_name: str = "Record Nature"):
        """Initialize the Record Nature converter."""
        super().__init__(field_name)
    
    def _convert_impl(self, value: str, record_id: str) -> Dict:
        """
        Convert Record Nature to JSON-LD format.
        
        Args:
            value: The raw Record Nature value
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of the Record Nature
        """
        if not value:
            return {}
        
        # Extract the primary status from the complex value
        if "(" in value:
            status = value.split("(")[0].strip()
        else:
            status = value.strip()
        
        # Map to standard vocabularies using the centralized mapping
        mapped_status = RECORD_STATUS_MAPPING.get(status, f"isiscb:status{status.replace(' ', '')}")
        
        return {
            "isiscb:recordStatus": mapped_status,
            "isiscb:recordNature": value
        }