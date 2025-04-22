"""
Name field converter for IsisCB authority records.

This module provides converters for name fields in authority records
including personal names, institutional names, concept names, etc.
"""

import logging
import pandas as pd
from typing import Dict, Any, Optional

from ..base import BaseConverter
from ..schema_mappings import get_property

logger = logging.getLogger('isiscb_conversion')

class NameConverter(BaseConverter):
    """Converter for Name fields in authority records."""
    
    def __init__(self):
        """Initialize the Name converter."""
        super().__init__("Name")
    
    def _convert_impl(self, fields: Dict[str, Any], record_id: str) -> Dict:
        """
        Convert name fields to JSON-LD format.
        
        Args:
            fields: Dictionary containing name-related fields
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of the name
        """
        result = {}
        
        # Handle empty or NaN values
        if not fields or not isinstance(fields, dict):
            return result
            
        # Get record type to determine name handling
        record_type = fields.get('Record Type', '')
        
        # Get name fields with fallbacks for missing values
        name = fields.get('Name', '')
        if pd.isna(name):
            name = ''
            
        last_name = fields.get('Last Name', '')
        if pd.isna(last_name):
            last_name = ''
            
        first_name = fields.get('First Name', '')
        if pd.isna(first_name):
            first_name = ''
            
        name_suffix = fields.get('Name Suffix', '')
        if pd.isna(name_suffix):
            name_suffix = ''
            
        name_preferred = fields.get('Name Preferred', '')
        if pd.isna(name_preferred):
            name_preferred = ''
        
        # Process different authority types differently
        if record_type == 'Person':
            return self._process_person_name(name, last_name, first_name, name_suffix, name_preferred, record_id)
        elif record_type in ['Institution', 'Serial Publication']:
            return self._process_organization_name(name, name_preferred, record_id)
        elif record_type == 'Concept':
            return self._process_concept_name(name, name_preferred, record_id)
        elif record_type == 'Geographic Term':
            return self._process_geographic_name(name, name_preferred, record_id)
        elif record_type == 'Time Period':
            return self._process_time_period_name(name, name_preferred, record_id)
        else:
            # Default handling for other record types
            return self._process_generic_name(name, name_preferred, record_id)
    
    def _process_person_name(self, name: str, last_name: str, first_name: str, 
                            name_suffix: str, name_preferred: str, record_id: str) -> Dict:
        """
        Process a person name.
        
        Args:
            name: Full name value
            last_name: Last name value
            first_name: First name value
            name_suffix: Name suffix value
            name_preferred: Preferred name form
            record_id: Record ID for logging
            
        Returns:
            Dict with JSON-LD representation
        """
        result = {}
        
        # Use name_preferred if available, otherwise use name
        preferred_display = name_preferred if name_preferred else name
        result["schema:name"] = preferred_display
        
        # Add SKOS labeling
        result["skos:prefLabel"] = preferred_display
        
        # Add separate name components if available
        if last_name:
            result["schema:familyName"] = last_name
            
        if first_name:
            result["schema:givenName"] = first_name
            
        if name_suffix:
            result["schema:nameSuffix"] = name_suffix
            
        # Store the preferred name form if different from the main name
        if name_preferred and name_preferred != name:
            result["isiscb:namePreferred"] = name_preferred
            
            # Add as alternate label
            if "skos:altLabel" not in result:
                result["skos:altLabel"] = []
            result["skos:altLabel"].append(name)
        
        return result
    
    def _process_organization_name(self, name: str, name_preferred: str, record_id: str) -> Dict:
        """
        Process an organization name.
        
        Args:
            name: Organization name
            name_preferred: Preferred name form
            record_id: Record ID for logging
            
        Returns:
            Dict with JSON-LD representation
        """
        result = {}
        
        # Use name_preferred if available, otherwise use name
        preferred_display = name_preferred if name_preferred else name
        result["schema:name"] = preferred_display
        
        # Add SKOS labeling
        result["skos:prefLabel"] = preferred_display
        
        # Store the preferred name form if different from the main name
        if name_preferred and name_preferred != name:
            result["isiscb:namePreferred"] = name_preferred
            
            # Add as alternate label
            result["skos:altLabel"] = [name]
        
        return result
    
    def _process_concept_name(self, name: str, name_preferred: str, record_id: str) -> Dict:
        """
        Process a concept name.
        
        Args:
            name: Concept name
            name_preferred: Preferred name form
            record_id: Record ID for logging
            
        Returns:
            Dict with JSON-LD representation
        """
        result = {}
        
        # Use name_preferred if available, otherwise use name
        preferred_display = name_preferred if name_preferred else name
        result["schema:name"] = preferred_display
        
        # Add SKOS labeling which is particularly relevant for concepts
        result["skos:prefLabel"] = preferred_display
        
        # Store the preferred name form if different from the main name
        if name_preferred and name_preferred != name:
            result["isiscb:namePreferred"] = name_preferred
            
            # Add as alternate label
            result["skos:altLabel"] = [name]
        
        return result
    
    def _process_geographic_name(self, name: str, name_preferred: str, record_id: str) -> Dict:
        """
        Process a geographic name.
        
        Args:
            name: Geographic name
            name_preferred: Preferred name form
            record_id: Record ID for logging
            
        Returns:
            Dict with JSON-LD representation
        """
        result = {}
        
        # Use name_preferred if available, otherwise use name
        preferred_display = name_preferred if name_preferred else name
        result["schema:name"] = preferred_display
        
        # Add as place name
        result["schema:placeName"] = preferred_display
        
        # Add SKOS labeling
        result["skos:prefLabel"] = preferred_display
        
        # Store the preferred name form if different from the main name
        if name_preferred and name_preferred != name:
            result["isiscb:namePreferred"] = name_preferred
            
            # Add as alternate label
            result["skos:altLabel"] = [name]
        
        return result
    
    def _process_time_period_name(self, name: str, name_preferred: str, record_id: str) -> Dict:
        """
        Process a time period name.
        
        Args:
            name: Time period name
            name_preferred: Preferred name form
            record_id: Record ID for logging
            
        Returns:
            Dict with JSON-LD representation
        """
        result = {}
        
        # Use name_preferred if available, otherwise use name
        preferred_display = name_preferred if name_preferred else name
        result["schema:name"] = preferred_display
        
        # Add SKOS labeling
        result["skos:prefLabel"] = preferred_display
        
        # Add temporal coverage
        result["dcterms:temporal"] = preferred_display
        
        # Store the preferred name form if different from the main name
        if name_preferred and name_preferred != name:
            result["isiscb:namePreferred"] = name_preferred
            
            # Add as alternate label
            result["skos:altLabel"] = [name]
        
        return result
    
    def _process_generic_name(self, name: str, name_preferred: str, record_id: str) -> Dict:
        """
        Process a generic authority name.
        
        Args:
            name: Authority name
            name_preferred: Preferred name form
            record_id: Record ID for logging
            
        Returns:
            Dict with JSON-LD representation
        """
        result = {}
        
        # Use name_preferred if available, otherwise use name
        preferred_display = name_preferred if name_preferred else name
        result["schema:name"] = preferred_display
        
        # Add SKOS labeling
        result["skos:prefLabel"] = preferred_display
        
        # Store the preferred name form if different from the main name
        if name_preferred and name_preferred != name:
            result["isiscb:namePreferred"] = name_preferred
            
            # Add as alternate label
            result["skos:altLabel"] = [name]
        
        return result