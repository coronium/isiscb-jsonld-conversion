"""
Classification field converter for IsisCB authority records.

This module provides converters for classification fields in authority records
such as Classification System and Classification Code.
"""

import logging
import pandas as pd
from typing import Dict, Any

from ..base import BaseConverter

logger = logging.getLogger('isiscb_conversion')

class ClassificationConverter(BaseConverter):
    """Converter for classification fields in authority records."""
    
    def __init__(self):
        """Initialize the Classification converter."""
        super().__init__("Classification")
    
    def _convert_impl(self, fields: Dict[str, Any], record_id: str) -> Dict:
        """
        Convert classification fields to JSON-LD format.
        
        Args:
            fields: Dictionary containing classification-related fields
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of the classification
        """
        result = {}
        
        # Handle empty or NaN values
        if not fields or not isinstance(fields, dict):
            return result
        
        # Get classification fields with fallbacks for missing values
        classification_system = fields.get('Classification System', '')
        if pd.isna(classification_system):
            classification_system = ''
            
        classification_code = fields.get('Classification Code', '')
        if pd.isna(classification_code):
            classification_code = ''
        
        # Get record type to determine classification handling
        record_type = fields.get('Record Type', '')
        
        # If no classification data, return empty result
        if not classification_system and not classification_code:
            return result
        
        # Add the classification system
        if classification_system:
            result["isiscb:classificationSystem"] = classification_system
            
            # For concepts and category divisions, add more specific typing
            if record_type in ['Concept', 'Category Division']:
                result["skos:inScheme"] = {
                    "skos:prefLabel": classification_system
                }
        
        # Add the classification code
        if classification_code:
            # Store the original value
            result["isiscb:classificationCode"] = classification_code
            
            # For concepts and categories, add as notation
            if record_type in ['Concept', 'Category Division']:
                result["skos:notation"] = classification_code
                
                # Parse hierarchical codes if present (e.g., "110-340")
                if '-' in str(classification_code):
                    parts = str(classification_code).split('-')
                    if len(parts) == 2:
                        result["isiscb:mainCategory"] = parts[0]
                        result["isiscb:subCategory"] = parts[1]
                else:
                    # Single-level code
                    result["isiscb:mainCategory"] = str(classification_code)
        
        # Add special handling for different classification systems
        if "Guerlac" in classification_system:
            result["isiscb:classificationScheme"] = "Guerlac"
        elif "Whitrow" in classification_system:
            result["isiscb:classificationScheme"] = "Whitrow"
        elif "Weldon" in classification_system:
            result["isiscb:classificationScheme"] = "Weldon"
        elif "SHOT" in classification_system:
            result["isiscb:classificationScheme"] = "SHOT"
        elif "Proper name" in classification_system:
            result["isiscb:classificationScheme"] = "Proper name"
        
        return result