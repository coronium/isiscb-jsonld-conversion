"""
Type field converters for IsisCB JSON-LD conversion.

This module provides converters for Record Type and related fields.
"""

import logging
from typing import Dict, List

from ..base import BaseConverter

logger = logging.getLogger('isiscb_conversion')

class RecordTypeConverter(BaseConverter):
    """Converter for Record Type fields."""
    
    # Standard mappings for authority records
    AUTHORITY_TYPE_MAPPING = {
        "Person": ["schema:Person", "foaf:Person"],
        "Institution": ["schema:Organization", "foaf:Organization"],
        "Geographic Term": ["schema:Place"],
        "Concept": ["skos:Concept"],
        "Time Period": ["dcterms:PeriodOfTime"],
        "Serial Publication": ["bibo:Periodical"],
        "Event": ["schema:Event"],
        "Creative Work": ["schema:CreativeWork"],
        "Category Division": ["skos:Collection"],
        "Cross-reference": ["skos:Collection"]
    }
    
    # Standard mappings for citation records
    CITATION_TYPE_MAPPING = {
        "Book": ["bibo:Book", "schema:Book"],
        "Article": ["bibo:Article", "schema:ScholarlyArticle"],
        "Thesis": ["bibo:Thesis", "schema:Thesis"],
        "Chapter": ["bibo:Chapter", "schema:Chapter"],
        "Review": ["bibo:AcademicArticle", "schema:Review"],
        "Essay": ["bibo:AcademicArticle"],
        "Website": ["schema:WebSite"],
        "Conference Proceeding": ["bibo:Proceedings"]
    }
    
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
            type_mapping = self.AUTHORITY_TYPE_MAPPING
        else:
            type_mapping = self.CITATION_TYPE_MAPPING
        
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
        
        # Map to standard vocabularies where possible
        status_mapping = {
            "Active": "isiscb:statusActive",
            "Inactive": "isiscb:statusInactive",
            "Delete": "isiscb:statusMarkedForDeletion",
            "Redirect": "isiscb:statusRedirect"
        }
        
        mapped_status = status_mapping.get(status, f"isiscb:status{status.replace(' ', '')}")
        
        return {
            "isiscb:recordStatus": mapped_status,
            "isiscb:recordNatureOriginal": value
        }