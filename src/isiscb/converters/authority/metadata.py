"""
Metadata field converter for IsisCB authority records.

This module provides converters for administrative metadata fields in authority records,
such as record history, staff notes, dates, and citation counts.
"""

import logging
import pandas as pd
import re
from typing import Dict, Any, Optional

from ..base import BaseConverter

logger = logging.getLogger('isiscb_conversion')

class AuthorityMetadataConverter(BaseConverter):
    """Converter for metadata and administrative fields in authority records."""
    
    def __init__(self):
        """Initialize the Authority Metadata converter."""
        super().__init__("Metadata")
    
    def _convert_impl(self, fields: Dict[str, Any], record_id: str) -> Dict:
        """
        Convert metadata fields to JSON-LD format.
        
        Args:
            fields: Dictionary containing metadata fields
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of metadata
        """
        result = {}
        
        # Handle empty or NaN values
        if not fields or not isinstance(fields, dict):
            return result
        
        # Process staff notes
        self._process_staff_notes(fields.get('Staff Notes'), result, record_id)
        
        # Process record history
        self._process_record_history(fields.get('Record History'), result, record_id)
        
        # Process dates
        self._process_dates(fields.get('Created Date'), fields.get('Modified Date'), result, record_id)
        
        # Process creators and modifiers
        self._process_creators(fields.get('Creator'), fields.get('Modifier'), result, record_id)
        
        # Process related citations count
        self._process_citation_count(fields.get('Related Citations Count'), result, record_id)
        
        return result
    
    def _process_staff_notes(self, staff_notes: Any, result: Dict, record_id: str) -> None:
        """
        Process staff notes field.
        
        Args:
            staff_notes: Staff notes value
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        if staff_notes is None or pd.isna(staff_notes):
            return
            
        notes_str = str(staff_notes).strip()
        if not notes_str:
            return
            
        # Add the original staff notes
        result["isiscb:staffNotes"] = notes_str
        
        # Extract metadata from curly braces {key: value}
        metadata_pattern = re.compile(r'\{([^{}]*?)\}')
        metadata_matches = metadata_pattern.findall(notes_str)
        
        if metadata_matches:
            parsed_metadata = []
            for match in metadata_matches:
                # Check if it contains a colon for key-value separation
                if ':' in match:
                    key, value = match.split(':', 1)
                    parsed_metadata.append({
                        "key": key.strip(),
                        "value": value.strip()
                    })
                else:
                    parsed_metadata.append({
                        "value": match.strip()
                    })
            
            if parsed_metadata:
                result["isiscb:staffNotesMetadata"] = parsed_metadata
                
                # Extract birth/death dates if present
                for item in parsed_metadata:
                    if "key" in item and "Birth and Death dates" in item["key"]:
                        # Store as a special property
                        result["isiscb:birthDeathDatesFromNotes"] = item["value"]
                        
                        # Try to extract years for standard properties
                        years_pattern = re.compile(r'(\d{4})-(\d{4})?')
                        match = years_pattern.search(item["value"])
                        if match:
                            birth_year = match.group(1)
                            death_year = match.group(2) if match.group(2) else None
                            
                            if birth_year:
                                result["schema:birthDate"] = birth_year
                            if death_year:
                                result["schema:deathDate"] = death_year
    
    def _process_record_history(self, record_history: Any, result: Dict, record_id: str) -> None:
        """
        Process record history field.
        
        Args:
            record_history: Record history value
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        if record_history is None or pd.isna(record_history):
            return
            
        history_str = str(record_history).strip()
        if not history_str:
            return
            
        # Add the original record history
        result["isiscb:recordHistory"] = history_str
        
        # Potentially extract structured data from history
        # This could be expanded to extract more specific information
        if "bulk change #" in history_str.lower():
            # Extract bulk change IDs
            bulk_changes = re.findall(r"bulk change #(\d+)", history_str, re.IGNORECASE)
            if bulk_changes:
                result["isiscb:bulkChangeIds"] = bulk_changes
    
    def _process_dates(self, created_date: Any, modified_date: Any, result: Dict, record_id: str) -> None:
        """
        Process date fields.
        
        Args:
            created_date: Created date value
            modified_date: Modified date value
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        # Process created date
        if created_date is not None and not pd.isna(created_date):
            result["dc:created"] = str(created_date)
        
        # Process modified date
        if modified_date is not None and not pd.isna(modified_date):
            result["dc:modified"] = str(modified_date)
    
    def _process_creators(self, creator: Any, modifier: Any, result: Dict, record_id: str) -> None:
        """
        Process creator and modifier fields.
        
        Args:
            creator: Creator value
            modifier: Modifier value
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        # Process creator
        if creator is not None and not pd.isna(creator):
            creator_str = str(creator).strip()
            if creator_str:
                # Check if it follows the pattern "Name (username)"
                if '(' in creator_str and ')' in creator_str:
                    name_part = creator_str.split('(')[0].strip()
                    username_part = creator_str.split('(')[1].split(')')[0].strip()
                    
                    result["dc:creator"] = {
                        "schema:name": name_part,
                        "isiscb:username": username_part
                    }
                else:
                    result["dc:creator"] = creator_str
        
        # Process modifier
        if modifier is not None and not pd.isna(modifier):
            modifier_str = str(modifier).strip()
            if modifier_str:
                # Check if it follows the pattern "Name (username)"
                if '(' in modifier_str and ')' in modifier_str:
                    name_part = modifier_str.split('(')[0].strip()
                    username_part = modifier_str.split('(')[1].split(')')[0].strip()
                    
                    result["isiscb:modifier"] = {
                        "schema:name": name_part,
                        "isiscb:username": username_part
                    }
                else:
                    result["isiscb:modifier"] = modifier_str
    
    def _process_citation_count(self, citation_count: Any, result: Dict, record_id: str) -> None:
        """
        Process related citations count field.
        
        Args:
            citation_count: Related citations count value
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        if citation_count is None or pd.isna(citation_count):
            return
            
        try:
            # Try to convert to integer
            count = int(citation_count)
            result["isiscb:relatedCitationsCount"] = count
        except (ValueError, TypeError):
            # If not a valid integer, store as string
            result["isiscb:relatedCitationsCount"] = str(citation_count).strip()