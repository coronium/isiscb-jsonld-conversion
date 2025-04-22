"""
Description field converter for IsisCB authority records.

This module provides converters for the Description field in authority records.
"""

import logging
import pandas as pd
from typing import Dict, Any

from ..base import BaseConverter

logger = logging.getLogger('isiscb_conversion')

class DescriptionConverter(BaseConverter):
    """Converter for Description fields in authority records."""
    
    def __init__(self, field_name: str = "Description"):
        """Initialize the Description converter."""
        super().__init__(field_name)
    
    def _convert_impl(self, value: Any, record_id: str) -> Dict:
        """
        Convert a description field to JSON-LD format.
        
        Args:
            value: The raw description text
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of the description
        """
        # Check for NaN, None, or empty values
        if value is None or pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
            return {}
            
        # Ensure value is a string
        if not isinstance(value, str):
            logger.warning(f"Non-string Description value for record {record_id}: {type(value)}")
            try:
                value = str(value)
            except Exception as e:
                logger.error(f"Cannot convert Description to string for record {record_id}: {str(e)}")
                return {}
        
        # Clean up the description text
        description = value.strip()
        
        # Create the JSON-LD representation
        result = {
            "schema:description": description,
            "dc:description": description
        }
        
        # Check for potential alternate names in the description
        # Many descriptions start with "AKA" or "Also known as"
        if description.lower().startswith("aka ") or description.lower().startswith("also known as "):
            # Extract the alternate names - this is a simplistic approach
            # A more sophisticated implementation would use regex patterns
            aka_part = description.split(",")[0]
            if "AKA " in aka_part:
                aka_names = aka_part.replace("AKA ", "").strip()
            elif "Also known as " in aka_part:
                aka_names = aka_part.replace("Also known as ", "").strip()
            else:
                aka_names = ""
                
            if aka_names:
                # Add as alternate label
                result["skos:altLabel"] = [aka_names]
        
        return result