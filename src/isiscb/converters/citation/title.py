"""
Title field converters for IsisCB JSON-LD conversion.

This module provides converters for Title fields in citation records.
"""

import logging
from typing import Dict

from ..base import BaseConverter
from ..schema_mappings import get_property

logger = logging.getLogger('isiscb_conversion')

class TitleConverter(BaseConverter):
    """Converter for Title fields in citation records."""
    
    def __init__(self, field_name: str = "Title"):
        """Initialize the Title converter."""
        super().__init__(field_name)
    
    def _convert_impl(self, value: str, record_id: str) -> Dict:
        """
        Convert a citation title to JSON-LD format.
        
        Args:
            value: The raw title string
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of the title
        """
        title = value.strip() if value else ""
        
        if not title:
            logger.warning(f"Empty title found for record {record_id}")
            title = ""
        
        # Use the primary property from the centralized mappings
        primary_property = get_property("title")
        jsonld = {
            primary_property: title
        }
        
        # Parse for subtitle if present
        #if ': ' in title:
        #    main_title, subtitle = title.split(': ', 1)
        #    jsonld[get_property("title", "mainTitle")] = main_title.strip()
        #    jsonld[get_property("title", "subtitle")] = subtitle.strip()
        
        return jsonld