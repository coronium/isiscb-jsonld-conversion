"""
Publication Details converter for IsisCB JSON-LD conversion.

This module provides converters for publication-related fields including
physical details, publisher information, edition details, publication year,
extent, language, and ISBN.
"""

import logging
import pandas as pd
import re
from typing import Dict, Any, Optional, List

from ..base import BaseConverter
from ..schema_mappings import get_property

logger = logging.getLogger('isiscb_conversion')

class PublicationDetailsConverter(BaseConverter):
    """Converter for publication-related fields in citation records."""
    
    def __init__(self):
        """Initialize the Publication Details converter."""
        super().__init__("Publication Details")
        
        # Regular expression for extracting year from "Year of publication" field
        self.year_pattern = re.compile(r'(\d{4})')
        
        # Regular expression for parsing place and publisher
        # Format: "Place: Publisher" or "Place: Publisher, Year"
        self.place_publisher_pattern = re.compile(r'^(.*?):\s*(.*?)(?:,\s*(\d{4}))?$')
        
    def _convert_impl(self, fields: Dict[str, Any], record_id: str) -> Dict:
        """
        Convert publication-related fields to JSON-LD format.
        
        Args:
            fields: Dictionary containing publication-related fields
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of publication details
        """
        result = {}
        
        # Process Year of publication
        self._process_year(fields.get('Year of publication'), result, record_id)
        
        # Process Edition Details
        self._process_edition(fields.get('Edition Details'), result, record_id)
        
        # Process Physical Details
        self._process_physical_details(fields.get('Physical Details'), result, record_id)
        
        # Process Extent
        self._process_extent(fields.get('Extent'), result, record_id)
        
        # Process Language
        self._process_language(fields.get('Language'), result, record_id)
        
        # Process ISBN
        self._process_isbn(fields.get('ISBN'), result, record_id)
        
        return result
    
    def _process_year(self, year_value: Any, result: Dict, record_id: str) -> None:
        """
        Process Year of publication field.
        
        Args:
            year_value: Year of publication value
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        if not year_value or pd.isna(year_value):
            return
            
        year_str = str(year_value).strip()
        if not year_str:
            return
            
        # Add the original year value
        result["dc:date"] = year_str
        result["schema:datePublished"] = year_str
        
        # Try to extract a normalized year for sorting/filtering
        try:
            # Extract first 4-digit number as the normalized year
            match = self.year_pattern.search(year_str)
            if match:
                normalized_year = int(match.group(1))
                result["isiscb:yearNormalized"] = normalized_year
        except Exception as e:
            logger.debug(f"Could not normalize year '{year_str}' for record {record_id}: {str(e)}")
            
    def _process_edition(self, edition: Any, result: Dict, record_id: str) -> None:
        """
        Process Edition Details field.
        
        Args:
            edition: Edition Details value
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        if not edition or pd.isna(edition):
            return
            
        edition_str = str(edition).strip()
        if not edition_str:
            return
            
        # Add edition information
        result["bibo:edition"] = edition_str
        
        # Store original edition text
        result["isiscb:editionDetails"] = edition_str
    
    def _process_physical_details(self, physical_details: Any, result: Dict, record_id: str) -> None:
        """
        Process Physical Details field.
        
        Args:
            physical_details: Physical Details value
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        if not physical_details or pd.isna(physical_details):
            return
            
        details_str = str(physical_details).strip()
        if not details_str:
            return
            
        # Add physical details information
        result["isiscb:physicalDetails"] = details_str
    
    def _process_extent(self, extent: Any, result: Dict, record_id: str) -> None:
        """
        Process Extent field.
        
        Args:
            extent: Extent value
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        if not extent or pd.isna(extent):
            return
            
        extent_str = str(extent).strip()
        if not extent_str:
            return
            
        # Add extent information
        result["isiscb:extent"] = extent_str
        
        # Try to extract page count if this looks like a page extent
        if 'p.' in extent_str.lower():
            try:
                # Simple extraction of the first number
                page_match = re.search(r'(\d+)\s*p', extent_str)
                if page_match:
                    result["schema:numberOfPages"] = int(page_match.group(1))
            except Exception as e:
                logger.debug(f"Could not extract page count from extent '{extent_str}' for record {record_id}: {str(e)}")
    
    def _process_language(self, language: Any, result: Dict, record_id: str) -> None:
        """
        Process Language field.
        
        Args:
            language: Language value
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        if not language or pd.isna(language):
            return
            
        lang_str = str(language).strip()
        if not lang_str:
            return
            
        # Handle multiple languages separated by commas or semicolons
        if ',' in lang_str or ';' in lang_str:
            # Split by both comma and semicolon
            separators = re.compile(r'[,;]')
            languages = [lang.strip() for lang in separators.split(lang_str) if lang.strip()]
            
            if languages:
                result["dc:language"] = languages
        else:
            result["dc:language"] = lang_str
    
    def _process_isbn(self, isbn: Any, result: Dict, record_id: str) -> None:
        """
        Process ISBN field.
        
        Args:
            isbn: ISBN value
            result: Result dictionary to update
            record_id: Record identifier for logging
        """
        if not isbn or pd.isna(isbn):
            return
            
        # Convert to string and clean
        isbn_str = str(isbn).strip().replace('-', '').replace(' ', '')
        if not isbn_str:
            return
            
        # Add ISBN information
        result["bibo:isbn"] = isbn_str
        
        # Add as a structured schema.org identifier
        result["schema:identifier"] = {
            "@type": "PropertyValue",
            "propertyID": "ISBN",
            "value": isbn_str
        }