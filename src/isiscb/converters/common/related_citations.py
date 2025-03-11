"""
Related Citations field converter for IsisCB JSON-LD conversion.

This module provides converters for parsing the Related Citations field
that connects citations to other citation records with typed relationships.
"""

import logging
import pandas as pd
from typing import Dict, List, Any, Optional

from ..base import BaseConverter
from ..schema_mappings import get_relationship_property, get_relationship_uri

logger = logging.getLogger('isiscb_conversion')

class RelatedCitationsConverter(BaseConverter):
    """Converter for Related Citations fields in citation records."""
    
    def __init__(self, field_name: str = "Related Citations"):
        """Initialize the Related Citations converter."""
        super().__init__(field_name)
        
    def _convert_impl(self, value: Any, record_id: str) -> Dict:
        """
        Convert Related Citations field to JSON-LD format.
        
        Args:
            value: The raw Related Citations string
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of the related citations
        """
        # Check for NaN, None, or empty values
        if value is None or pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
            return {}
            
        # Ensure value is a string
        if not isinstance(value, str):
            logger.warning(f"Non-string Related Citations value for record {record_id}: {type(value)}")
            return {}
            
        # Split entries by double slash
        entries = value.split(" // ")
        
        # Process each entry
        citation_relationships = []
        
        # Track relationships by type for special handling
        relationships_by_type = {}
        
        for entry in entries:
            try:
                # Parse the entry into a dictionary
                entry_dict = self._parse_entry(entry)
                
                if not entry_dict or "CCRType" not in entry_dict or "CitationID" not in entry_dict:
                    continue
                    
                # Get relationship type
                relationship_type = entry_dict["CCRType"]
                
                # Create relationship object with proper type URI
                relationship = {
                    "@type": f"isiscb:{self._normalize_type(relationship_type)}",
                    "isiscb:relationshipType": relationship_type,
                    "isiscb:citation": {
                        "@id": f"https://data.isiscb.org/citation/{entry_dict.get('CitationID', '').strip()}"
                    }
                }
                
                # Add relation ID if available
                if "CCR_ID" in entry_dict:
                    relationship["isiscb:relationshipID"] = entry_dict["CCR_ID"]
                
                # Add status if available
                if "CCRStatus" in entry_dict:
                    relationship["isiscb:relationshipStatus"] = entry_dict["CCRStatus"].strip()
                
                # Add other properties
                if "CitationTitle" in entry_dict:
                    relationship["isiscb:citationTitle"] = entry_dict["CitationTitle"].strip()
                    
                if "CitationType" in entry_dict:
                    relationship["isiscb:citationType"] = entry_dict["CitationType"].strip()
                    
                # Add status if available
                if "CitationStatus" in entry_dict:
                    relationship["isiscb:citationStatus"] = entry_dict["CitationStatus"].strip()
                
                # Add to full relationships list
                citation_relationships.append(relationship)
                
                # Normalize type for grouping
                norm_type = self._normalize_type(relationship_type)
                
                # Group by type for special handling
                if norm_type not in relationships_by_type:
                    relationships_by_type[norm_type] = []
                relationships_by_type[norm_type].append(relationship)
                
            except Exception as e:
                logger.warning(f"Error parsing related citation entry for record {record_id}: {entry}. Error: {str(e)}")
        
        # Generate result dictionary
        result = {}
        
        # Add the full list of relationships
        if citation_relationships:
            result["isiscb:relatedCitations"] = citation_relationships
        
        # Add specialized relationships
        self._add_normalized_relationships(result, relationships_by_type)
        
        return result
    
    def _parse_entry(self, entry: str) -> Dict:
        """
        Parse a single entry into a dictionary.
        
        Args:
            entry: A single citation relationship entry
            
        Returns:
            Dictionary of key-value pairs
        """
        if not entry or entry.strip() == "":
            return {}
            
        # Split by double pipe and create key-value pairs
        parts = entry.split(" || ")
        result = {}
        
        for part in parts:
            if " " not in part:
                continue
                
            # Split only on the first space to handle values that may contain spaces
            key, value = part.split(" ", 1)
            result[key] = value
            
        return result
    
    def _normalize_type(self, relationship_type: str) -> str:
        """
        Normalize relationship type for consistent mapping.
        
        Args:
            relationship_type: Original relationship type
            
        Returns:
            Normalized relationship type as camelCase
        """
        # Trim whitespace
        relationship_type = relationship_type.strip()
        
        # Replace spaces with empty string and capitalize first letter of each word
        words = [word.strip() for word in relationship_type.split()]
        if not words:
            return "unknownRelation"
            
        # First word lowercase, rest capitalized - camelCase format
        camel_case = words[0].lower()
        for word in words[1:]:
            if word:
                camel_case += word[0].upper() + word[1:].lower()
                
        return camel_case
    
    def _add_normalized_relationships(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Add normalized relationships to the result.
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Map of normalized relationship types to standard property names
        standard_mappings = {
            "isReviewedBy": "isiscb:isReviewedBy",
            "reviews": "isiscb:reviews",
            "includesSeriesArticle": "isiscb:includesSeriesArticle",
            "isPartOf": "dcterms:isPartOf",
            "hasPart": "dcterms:hasPart",
            "references": "dcterms:references",
            "isReferencedBy": "dcterms:isReferencedBy",
            "succeeds": "dcterms:succeeds",
            "precedes": "dcterms:precedes",
            "replaces": "dcterms:replaces",
            "isReplacedBy": "dcterms:isReplacedBy"
        }
        
        # Process each relationship type
        for norm_type, relationships in relationships_by_type.items():
            # Get the standard property name or create a custom one
            property_name = standard_mappings.get(norm_type, f"isiscb:{norm_type}")
            
            # Add the relationships to the result
            result[property_name] = self._process_citations(relationships)
    
    def _process_citations(self, citations: List[Dict]) -> List[Dict]:
        """
        Process citation relationships into proper citation objects.
        
        Args:
            citations: List of citation relationship objects
            
        Returns:
            List of citation objects in JSON-LD format
        """
        citation_objects = []
        for citation in citations:
            citation_obj = {
                "@id": citation["isiscb:citation"]["@id"]
            }
            
            if "isiscb:citationTitle" in citation:
                citation_obj["dc:title"] = citation["isiscb:citationTitle"]
                
            if "isiscb:citationType" in citation:
                citation_obj["isiscb:citationType"] = citation["isiscb:citationType"]
                
            citation_objects.append(citation_obj)
            
        return citation_objects