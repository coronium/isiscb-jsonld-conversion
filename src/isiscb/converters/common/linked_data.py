"""
Linked Data field converters for IsisCB JSON-LD conversion.

This module provides converters for Linked Data fields that connect
IsisCB records to external authority systems like VIAF, DNB, etc.
"""

import logging
import re
import pandas as pd
from typing import Dict, List, Optional, Any

from ..base import BaseConverter

logger = logging.getLogger('isiscb_conversion')

class LinkedDataConverter(BaseConverter):
    """Converter for Linked Data fields in citation and authority records."""
    
    def __init__(self, field_name: str = "Linked Data"):
        """Initialize the Linked Data converter."""
        super().__init__(field_name)
        # Regex pattern to match the simplified format: Type X || URN Y
        self.entry_pattern = re.compile(r"Type\s+([^\s|]+)\s+\|\|\s+URN\s+(.*?)(?:\s*$)")
    
    def _convert_impl(self, value: str, record_id: str) -> Dict:
        """
        Convert Linked Data field to JSON-LD format.
        
        Args:
            value: The raw Linked Data string
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of the linked data
        """
        if not value or pd.isna(value):
            return {}
            
        # Split entries using the separator
        entries = []
        try:
            # Look for separate entries (multiple linked data items)
            # Multiple entries may be separated by double forward slashes
            raw_entries = value.split(" // ")
            
            for entry in raw_entries:
                entry = entry.strip()
                if not entry:
                    continue
                    
                # Parse the entry using regex
                match = self.entry_pattern.match(entry)
                if match:
                    link_type, urn = match.groups()
                    
                    # Build structured entry
                    linked_entry = {
                        "type": link_type.strip(),
                        "urn": urn.strip() if urn else None
                    }
                    
                    # Skip entries with no URN (likely incomplete)
                    if not linked_entry["urn"]:
                        logger.warning(f"Skipping linked data entry without URN for record {record_id}: {entry}")
                        continue
                        
                    entries.append(linked_entry)
                else:
                    # Try alternative parsing approach for malformed entries
                    parts = entry.split("||")
                    if len(parts) >= 2:  # We need at least Type and URN
                        try:
                            type_part = parts[0].strip()
                            urn_part = parts[1].strip()
                            
                            if type_part.startswith("Type ") and urn_part.startswith("URN "):
                                linked_entry = {
                                    "type": type_part[5:].strip(),
                                    "urn": urn_part[4:].strip()
                                }
                                entries.append(linked_entry)
                        except Exception as e:
                            logger.warning(f"Error parsing linked data entry for record {record_id}: {entry}. Error: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing linked data for record {record_id}: {str(e)}")
            
        # Convert to JSON-LD format
        if not entries:
            return {}
            
        # Build appropriate JSON-LD
        result = {}
        
        # Group entries by type
        grouped_entries = {}
        for entry in entries:
            entry_type = entry["type"]
            if entry_type not in grouped_entries:
                grouped_entries[entry_type] = []
            grouped_entries[entry_type].append(entry["urn"])
        
        # Store all linked data entries
        result["isiscb:linkedData"] = [
            {"type": type_name, "values": values}
            for type_name, values in grouped_entries.items()
        ]
        
        # Handle specific types for standard schema properties
        # DOIs
        if "DOI" in grouped_entries:
            doi_values = grouped_entries["DOI"]
            if len(doi_values) == 1:
                result["schema:identifier"] = {
                    "@type": "PropertyValue",
                    "propertyID": "DOI",
                    "value": doi_values[0]
                }
            else:
                result["schema:identifier"] = [
                    {
                        "@type": "PropertyValue",
                        "propertyID": "DOI",
                        "value": doi
                    }
                    for doi in doi_values
                ]
                
        # ISBNs
        if "ISBN" in grouped_entries:
            isbn_values = grouped_entries["ISBN"]
            
            # Add to schema:identifier if not already there
            if "schema:identifier" not in result:
                if len(isbn_values) == 1:
                    result["schema:identifier"] = {
                        "@type": "PropertyValue",
                        "propertyID": "ISBN",
                        "value": isbn_values[0]
                    }
                else:
                    result["schema:identifier"] = [
                        {
                            "@type": "PropertyValue",
                            "propertyID": "ISBN",
                            "value": isbn
                        }
                        for isbn in isbn_values
                    ]
            else:
                # Convert to list if it's not already
                if not isinstance(result["schema:identifier"], list):
                    result["schema:identifier"] = [result["schema:identifier"]]
                
                # Add ISBN identifiers
                for isbn in isbn_values:
                    result["schema:identifier"].append({
                        "@type": "PropertyValue",
                        "propertyID": "ISBN",
                        "value": isbn
                    })
        
        # URIs - add as sameAs
        if "URI" in grouped_entries:
            uri_values = grouped_entries["URI"]
            if len(uri_values) == 1:
                result["schema:sameAs"] = uri_values[0]
            else:
                result["schema:sameAs"] = uri_values
            
        return result