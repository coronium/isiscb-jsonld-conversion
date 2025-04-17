"""
Attributes field converter for IsisCB JSON-LD conversion.

This module provides converters for the structured Attributes field in citation and authority records,
handling various attribute types like dates, journal abbreviations, and geographic information.
"""

import logging
import pandas as pd
import re
import json
from typing import Dict, List, Any, Optional, Tuple

from ..base import BaseConverter

logger = logging.getLogger('isiscb_conversion')

class AttributesConverter(BaseConverter):
    """Converter for structured Attributes field in citation and authority records."""
    
    def __init__(self, field_name: str = "Attributes"):
        """Initialize the Attributes converter."""
        super().__init__(field_name)
        
        # Map attribute types to specialized processing methods
        self.type_processors = {
            "BirthToDeathDates": self._process_birth_death_dates,
            "Birth date": self._process_birth_date,
            "Death date": self._process_death_date,
            "FlourishedDate": self._process_flourished_date,
            "JournalAbbr": self._process_journal_abbr,
            "GeographicEntityType": self._process_geographic_entity_type,
            "CountryCode": self._process_country_code
        }
    
    def _convert_impl(self, value: str, record_id: str) -> Dict:
        """
        Convert the Attributes field to JSON-LD format.
        
        Args:
            value: The raw Attributes field string
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of attributes
        """
        # Check for empty, None, or NaN values
        if value is None or pd.isna(value) or value.strip() == "":
            return {}
        
        # Parse all attribute entries
        attribute_entries = self._parse_attributes(value, record_id)
        if not attribute_entries:
            return {}
        
        # Result dictionary with the structured attributes
        result = {
            "isiscb:attributes": attribute_entries
        }
        
        # Process specific attribute types with specialized handling
        self._apply_specialized_processing(attribute_entries, result, record_id)
        
        return result
    
    def _parse_attributes(self, value: str, record_id: str) -> List[Dict]:
        """
        Parse the raw Attributes field into structured entries.
        
        Args:
            value: Raw Attributes field value
            record_id: Record ID for logging
            
        Returns:
            List of structured attribute dictionaries
        """
        entries = []
        
        # Split by " // " to handle multiple attribute entries
        raw_entries = value.split(" // ")
        
        for raw_entry in raw_entries:
            try:
                # Parse a single attribute entry
                entry = self._parse_single_attribute(raw_entry.strip())
                if entry:
                    entries.append(entry)
            except Exception as e:
                logger.warning(f"Error parsing attribute entry for record {record_id}: {str(e)}")
                logger.debug(f"Problematic entry: {raw_entry}")
        
        return entries
    
    def _parse_single_attribute(self, entry: str) -> Dict:
        """
        Parse a single attribute entry into a structured dictionary.
        
        Args:
            entry: Raw attribute entry string
            
        Returns:
            Structured attribute dictionary
        """
        if not entry:
            return {}
        
        # Split by " || " to separate fields
        fields = entry.split(" || ")
        attribute = {}
        
        for field in fields:
            if " " not in field:
                continue
                
            # Split by first space to get key and value
            key, value = field.split(" ", 1)
            
            # Map keys to more friendly names
            key_map = {
                "AttributeID": "id",
                "AttributeStatus": "status",
                "AttributeType": "type",
                "AttributeValue": "value",
                "AttributeFreeFormValue": "displayValue",
                "AttributeStart": "start",
                "AttributeEnd": "end",
                "AttributeDescription": "description"
            }
            
            friendly_key = key_map.get(key, key)
            attribute[friendly_key] = value.strip()
        
        # Parse AttributeValue if it looks like a JSON array
        if "value" in attribute and attribute["value"].startswith("[[") and attribute["value"].endswith("]]"):
            try:
                # Extract inner brackets and convert to list
                values_str = attribute["value"].replace("[[", "[").replace("]]", "]")
                attribute["structuredValue"] = json.loads(values_str)
            except Exception as e:
                logger.debug(f"Could not parse attribute value as JSON: {attribute['value']}")
        
        return attribute
    
    def _apply_specialized_processing(self, attribute_entries: List[Dict], result: Dict, record_id: str) -> None:
        """
        Apply specialized processing for known attribute types.
        
        Args:
            attribute_entries: List of parsed attribute entries
            result: Result dictionary to update
            record_id: Record ID for logging
        """
        for entry in attribute_entries:
            attr_type = entry.get("type")
            if attr_type in self.type_processors:
                processor = self.type_processors[attr_type]
                processor(entry, result, record_id)
    
    def _process_birth_death_dates(self, entry: Dict, result: Dict, record_id: str) -> None:
        """
        Process BirthToDeathDates attribute type.
        
        Args:
            entry: Attribute entry dictionary
            result: Result dictionary to update
            record_id: Record ID for logging
        """
        # Extract structured values if available, otherwise parse from displayValue
        birth_year = None
        death_year = None
        
        if "structuredValue" in entry:
            values = entry["structuredValue"]
            if len(values) > 0:
                birth_year = values[0]
            if len(values) > 1:
                death_year = values[1]
        
        # Also add the free-form value
        display_value = entry.get("displayValue", "")
        
        # Add to schema.org properties
        if birth_year:
            if "schema:birthDate" not in result:
                result["schema:birthDate"] = str(birth_year)
            
        if death_year:
            if "schema:deathDate" not in result:
                result["schema:deathDate"] = str(death_year)
        
        # Add complete birth-death range if both are available
        if birth_year and death_year:
            if "schema:birthDeathDate" not in result:
                result["schema:birthDeathDate"] = display_value if display_value else f"{birth_year}-{death_year}"
    
    def _process_birth_date(self, entry: Dict, result: Dict, record_id: str) -> None:
        """
        Process Birth date attribute type.
        
        Args:
            entry: Attribute entry dictionary
            result: Result dictionary to update
            record_id: Record ID for logging
        """
        if "structuredValue" in entry and entry["structuredValue"]:
            birth_year = entry["structuredValue"][0] if isinstance(entry["structuredValue"], list) else entry["structuredValue"]
            result["schema:birthDate"] = str(birth_year)
        elif "value" in entry and entry["value"]:
            # Try to extract year from the value field
            match = re.search(r'\[(\d+)\]', entry["value"])
            if match:
                birth_year = match.group(1)
                result["schema:birthDate"] = birth_year
    
    def _process_death_date(self, entry: Dict, result: Dict, record_id: str) -> None:
        """
        Process Death date attribute type.
        
        Args:
            entry: Attribute entry dictionary
            result: Result dictionary to update
            record_id: Record ID for logging
        """
        if "structuredValue" in entry and entry["structuredValue"]:
            death_year = entry["structuredValue"][0] if isinstance(entry["structuredValue"], list) else entry["structuredValue"]
            result["schema:deathDate"] = str(death_year)
        elif "value" in entry and entry["value"]:
            # Try to extract year from the value field
            match = re.search(r'\[(\d+)\]', entry["value"])
            if match:
                death_year = match.group(1)
                result["schema:deathDate"] = death_year
    
    def _process_flourished_date(self, entry: Dict, result: Dict, record_id: str) -> None:
        """
        Process FlourishedDate attribute type.
        
        Args:
            entry: Attribute entry dictionary
            result: Result dictionary to update
            record_id: Record ID for logging
        """
        if "structuredValue" in entry and entry["structuredValue"]:
            flourished_year = entry["structuredValue"][0] if isinstance(entry["structuredValue"], list) else entry["structuredValue"]
            result["isiscb:flourishedDate"] = str(flourished_year)
            
            # Also add the display value which might be a century or date range
            if "displayValue" in entry and entry["displayValue"]:
                result["isiscb:flourishedDisplayValue"] = entry["displayValue"]
    
    def _process_journal_abbr(self, entry: Dict, result: Dict, record_id: str) -> None:
        """
        Process JournalAbbr attribute type.
        
        Args:
            entry: Attribute entry dictionary
            result: Result dictionary to update
            record_id: Record ID for logging
        """
        if "value" in entry and entry["value"]:
            journal_abbr = entry["value"]
            
            # Store the journal abbreviation
            result["bibo:shortTitle"] = journal_abbr
            
            # Also store with IsisCB namespace for preservation
            result["isiscb:journalAbbreviation"] = journal_abbr
    
    def _process_geographic_entity_type(self, entry: Dict, result: Dict, record_id: str) -> None:
        """
        Process GeographicEntityType attribute type.
        
        Args:
            entry: Attribute entry dictionary
            result: Result dictionary to update
            record_id: Record ID for logging
        """
        if "value" in entry and entry["value"]:
            geo_type = entry["value"]
            
            # Store the geographic entity type
            result["isiscb:geographicEntityType"] = geo_type
            
            # Add Schema.org place type if applicable
            place_type_map = {
                "City": "schema:City",
                "Country": "schema:Country",
                "State": "schema:State",
                "Province": "schema:AdministrativeArea"
            }
            
            if geo_type in place_type_map:
                if "@type" not in result:
                    result["@type"] = place_type_map[geo_type]
                elif isinstance(result["@type"], list):
                    result["@type"].append(place_type_map[geo_type])
                else:
                    result["@type"] = [result["@type"], place_type_map[geo_type]]
    
    def _process_country_code(self, entry: Dict, result: Dict, record_id: str) -> None:
        """
        Process CountryCode attribute type.
        
        Args:
            entry: Attribute entry dictionary
            result: Result dictionary to update
            record_id: Record ID for logging
        """
        if "value" in entry and entry["value"]:
            country_code = entry["value"]
            
            # Store the country code
            result["schema:addressCountry"] = country_code