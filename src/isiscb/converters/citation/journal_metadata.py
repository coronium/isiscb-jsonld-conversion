"""
Journal metadata converter for IsisCB JSON-LD conversion.

This module provides converters for journal-specific fields such as
Journal Link, Journal Volume, Journal Issue, and Pages Free Text.
"""

import logging
import pandas as pd
import re
from typing import Dict, Any, Optional, Tuple

from ..base import BaseConverter
from ..schema_mappings import get_property

logger = logging.getLogger('isiscb_conversion')

class JournalMetadataConverter(BaseConverter):
    """Converter for journal metadata fields in citation records."""
    
    def __init__(self):
        """Initialize the Journal Metadata converter."""
        super().__init__("Journal Metadata")
        # Regex pattern to extract range information
        # Format: "value (From start // To end)" or just "value" if no range
        self.range_pattern = re.compile(r'^(.*?)(?:\s*\(From\s+(.*?)\s*//\s*To\s+(.*?)\s*\))?$')
    
    def _convert_impl(self, row: Dict, record_id: str) -> Dict:
        """
        Convert journal metadata fields to JSON-LD format.
        
        Args:
            row: Dictionary containing journal-related fields
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of journal metadata
        """
        result = {}
        
        # Handle Journal Link - reference to the journal authority
        if 'Journal Link' in row and row['Journal Link'] and not pd.isna(row['Journal Link']):
            journal_id = row['Journal Link'].strip()
            if journal_id:
                result["schema:isPartOf"] = {
                    "@id": f"https://data.isiscb.org/authority/{journal_id}"
                }
                # Add journal type information
                result["schema:isPartOf"]["@type"] = ["bibo:Periodical"]
        
        # Handle Journal Volume with range extraction
        if 'Journal Volume' in row and row['Journal Volume'] and not pd.isna(row['Journal Volume']):
            volume = str(row['Journal Volume']).strip()
            if volume:
                # Extract the display value and range information
                display_value, start_value, end_value = self._extract_range(volume)
                
                # Use bibo:volume for standard compatibility
                result["bibo:volume"] = display_value
                
                # Also keep the original value with IsisCB namespace for preservation
                result["isiscb:journalVolume"] = volume
                
                # Add range information if present
                if start_value and end_value:
                    result["isiscb:journalVolumeStart"] = start_value
                    result["isiscb:journalVolumeEnd"] = end_value
        
        # Handle Journal Issue with range extraction
        if 'Journal Issue' in row and row['Journal Issue'] and not pd.isna(row['Journal Issue']):
            issue = str(row['Journal Issue']).strip()
            if issue:
                # Extract the display value and range information
                display_value, start_value, end_value = self._extract_range(issue)
                
                # Use bibo:issue for standard compatibility
                result["bibo:issue"] = display_value
                
                # Also keep the original value with IsisCB namespace for preservation
                result["isiscb:journalIssue"] = issue
                
                # Add range information if present
                if start_value and end_value:
                    result["isiscb:journalIssueStart"] = start_value
                    result["isiscb:journalIssueEnd"] = end_value
        
        # Handle Pages Free Text with range extraction
        if 'Pages Free Text' in row and row['Pages Free Text'] and not pd.isna(row['Pages Free Text']):
            pages = str(row['Pages Free Text']).strip()
            if pages:
                # Extract the display value and range information
                display_value, start_value, end_value = self._extract_range(pages)
                
                # Use bibo:pages for standard compatibility
                result["bibo:pages"] = display_value
                
                # Also keep the original formatting with IsisCB namespace
                result["isiscb:pagesFreeText"] = pages
                
                # Add structured page range information if present
                if start_value and end_value:
                    result["bibo:pageStart"] = start_value
                    result["bibo:pageEnd"] = end_value
                elif "-" in display_value:
                    # Try to extract page range from display value if formatted with hyphen
                    try:
                        start_page, end_page = display_value.split("-", 1)
                        result["bibo:pageStart"] = start_page.strip()
                        result["bibo:pageEnd"] = end_page.strip()
                    except Exception as e:
                        logger.debug(f"Could not parse page range '{display_value}' for record {record_id}: {str(e)}")
        
        return result
    
    def _extract_range(self, value: str) -> Tuple[str, str, str]:
        """
        Extract display value and range information from a field.
        
        Args:
            value: The raw field value with potential range info
            
        Returns:
            Tuple of (display_value, start_value, end_value)
        """
        try:
            match = self.range_pattern.match(value)
            if match:
                display_value = match.group(1).strip()
                start_value = match.group(2).strip() if match.group(2) else ""
                end_value = match.group(3).strip() if match.group(3) else ""
                return display_value, start_value, end_value
            return value, "", ""
        except Exception as e:
            logger.warning(f"Error extracting range from '{value}': {str(e)}")
            return value, "", ""