"""
Metadata field converter for IsisCB JSON-LD conversion.

This module provides converters for metadata and administrative fields in citation records,
including status flags, dates, and record management information.
"""

import logging
import pandas as pd
from typing import Dict, Any, Optional

from ..base import BaseConverter

logger = logging.getLogger('isiscb_conversion')

class MetadataConverter(BaseConverter):
    """Converter for metadata and administrative fields in citation records."""
    
    def __init__(self):
        """Initialize the Metadata converter."""
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
        
        # Process status flags
        self._process_status_flags(fields, result, record_id)
        
        # Process dates
        self._process_dates(fields, result, record_id)
        
        # Process record creators/modifiers
        self._process_creators(fields, result, record_id)
        
        # Process record history and notes
        self._process_record_history(fields, result, record_id)
        
        # Process dataset and additional fields
        self._process_additional_fields(fields, result, record_id)
        
        return result
    
    def _process_status_flags(self, fields: Dict[str, Any], result: Dict, record_id: str) -> None:
        """
        Process status flag fields.
        
        Args:
            fields: Input fields dictionary
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        # Map of field names to property names
        status_field_map = {
            'Fully Entered': 'isiscb:fullyEntered',
            'Proofed': 'isiscb:proofed',
            'SPW checked': 'isiscb:spwChecked',
            'Published Print': 'isiscb:publishedPrint',
            'Published RLG': 'isiscb:publishedRLG',
            'Stub Record Status': 'isiscb:stubRecordStatus'
        }
        
        # Process each status field
        for field_name, property_name in status_field_map.items():
            if field_name in fields and fields[field_name] and not pd.isna(fields[field_name]):
                result[property_name] = str(fields[field_name]).strip()
    
    def _process_dates(self, fields: Dict[str, Any], result: Dict, record_id: str) -> None:
        """
        Process date fields.
        
        Args:
            fields: Input fields dictionary
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        # Created Date
        if 'Created Date' in fields and fields['Created Date'] and not pd.isna(fields['Created Date']):
            result['dc:created'] = fields['Created Date']
        
        # Modified Date
        if 'Modified Date' in fields and fields['Modified Date'] and not pd.isna(fields['Modified Date']):
            result['dc:modified'] = fields['Modified Date']
    
    def _process_creators(self, fields: Dict[str, Any], result: Dict, record_id: str) -> None:
        """
        Process creator and modifier fields.
        
        Args:
            fields: Input fields dictionary
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        # Creator
        if 'Creator' in fields and fields['Creator'] and not pd.isna(fields['Creator']):
            creator_value = str(fields['Creator']).strip()
            
            # Check if it follows the pattern "Name (username)"
            if '(' in creator_value and ')' in creator_value:
                name_part = creator_value.split('(')[0].strip()
                username_part = creator_value.split('(')[1].split(')')[0].strip()
                
                result['dc:creator'] = {
                    "schema:name": name_part,
                    "isiscb:username": username_part
                }
            else:
                result['dc:creator'] = creator_value
        
        # Modifier
        if 'Modifier' in fields and fields['Modifier'] and not pd.isna(fields['Modifier']):
            modifier_value = str(fields['Modifier']).strip()
            
            # Check if it follows the pattern "Name (username)"
            if '(' in modifier_value and ')' in modifier_value:
                name_part = modifier_value.split('(')[0].strip()
                username_part = modifier_value.split('(')[1].split(')')[0].strip()
                
                result['isiscb:modifier'] = {
                    "schema:name": name_part,
                    "isiscb:username": username_part
                }
            else:
                result['isiscb:modifier'] = modifier_value
    
    def _process_record_history(self, fields: Dict[str, Any], result: Dict, record_id: str) -> None:
        """
        Process record history and notes fields.
        
        Args:
            fields: Input fields dictionary
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        # Record History
        if 'Record History' in fields and fields['Record History'] and not pd.isna(fields['Record History']):
            result['isiscb:recordHistory'] = str(fields['Record History']).strip()
            
            # Optional: Parse structured record history entries
            # This could be expanded to extract structured information if needed
        
        # Staff Notes
        if 'Staff Notes' in fields and fields['Staff Notes'] and not pd.isna(fields['Staff Notes']):
            staff_notes = str(fields['Staff Notes']).strip()
            result['isiscb:staffNotes'] = staff_notes
            
            # Optional: Parse metadata in curly braces {key: value}
            import re
            metadata_pattern = re.compile(r'\{([^{}]*?)\}')
            metadata_matches = metadata_pattern.findall(staff_notes)
            
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
                    result['isiscb:staffNotesMetadata'] = parsed_metadata
        
        # Complete Citation
        if 'Complete Citation' in fields and fields['Complete Citation'] and not pd.isna(fields['Complete Citation']):
            result['isiscb:completeCitation'] = str(fields['Complete Citation']).strip()
    
    def _process_additional_fields(self, fields: Dict[str, Any], result: Dict, record_id: str) -> None:
        """
        Process additional metadata fields.
        
        Args:
            fields: Input fields dictionary
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        # Dataset
        if 'Dataset' in fields and fields['Dataset'] and not pd.isna(fields['Dataset']):
            result['isiscb:dataset'] = str(fields['Dataset']).strip()
        
        # Link to Record (external URL)
        if 'Link to Record' in fields and fields['Link to Record'] and not pd.isna(fields['Link to Record']):
            link_value = str(fields['Link to Record']).strip()
            result['isiscb:linkToRecord'] = link_value
            
            # Add as sameAs if it's a URI
            if link_value.startswith(('http://', 'https://')):
                if 'schema:sameAs' not in result:
                    result['schema:sameAs'] = link_value
                elif isinstance(result['schema:sameAs'], list):
                    result['schema:sameAs'].append(link_value)
                else:
                    result['schema:sameAs'] = [result['schema:sameAs'], link_value]