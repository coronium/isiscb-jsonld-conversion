"""
Related Authorities field converter for IsisCB authority records.

This module provides converters for parsing authority-to-authority relationships
in the Related Authorities field of authority records.
"""

import logging
import re
import pandas as pd
from typing import Dict, List, Any, Optional

from ..base import BaseConverter
from ..schema_mappings import get_relationship_property, get_relationship_uri

logger = logging.getLogger('isiscb_conversion')

class AuthorityRelatedAuthoritiesConverter(BaseConverter):
    """Converter for Related Authorities fields in authority records."""
    
    def __init__(self, field_name: str = "Related Authorities"):
        """Initialize the Related Authorities converter."""
        super().__init__(field_name)
    
    def _convert_impl(self, value: Any, record_id: str) -> Dict:
        """
        Convert Related Authorities field to JSON-LD format.
        
        Args:
            value: The raw Related Authorities string
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of the related authorities
        """
        # Check for NaN, None, or empty values
        if value is None or pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
            return {}
            
        # Ensure value is a string
        if not isinstance(value, str):
            logger.warning(f"Non-string Related Authorities value for record {record_id}: {type(value)}")
            return {}
            
        # Split entries by double slash
        entries = value.split(" // ")
        
        # Process each entry
        authority_relationships = []
        
        # Track relationships by type for special handling
        relationships_by_type = {}
        
        for entry in entries:
            try:
                # Parse the entry into a dictionary
                entry_dict = self._parse_entry(entry)
                
                if not entry_dict or "ACRType" not in entry_dict or "AuthorityID" not in entry_dict:
                    continue
                    
                # Get relationship type
                relationship_type = entry_dict["ACRType"]
                
                # Create relationship object with proper type URI
                relationship = {
                    "@type": f"isiscb:{self._normalize_type(relationship_type)}",
                    "isiscb:relationshipType": relationship_type,
                    "isiscb:authority": {
                        "@id": f"https://data.isiscb.org/authority/{entry_dict.get('AuthorityID', '').strip()}"
                    }
                }
                
                # Add display order if available
                if "ACRDisplayOrder" in entry_dict:
                    relationship["isiscb:displayOrder"] = entry_dict["ACRDisplayOrder"]
                
                # Add authority name if available
                if "AuthorityName" in entry_dict:
                    relationship["isiscb:authorityName"] = entry_dict["AuthorityName"].strip()
                
                # Add authority type if available
                if "AuthorityType" in entry_dict:
                    relationship["isiscb:authorityType"] = entry_dict["AuthorityType"].strip()
                    
                # Add display name if available
                if "ACRNameForDisplayInCitation" in entry_dict and entry_dict["ACRNameForDisplayInCitation"].strip():
                    relationship["isiscb:displayName"] = entry_dict["ACRNameForDisplayInCitation"].strip()
                
                # Add status if available
                if "AuthorityStatus" in entry_dict:
                    relationship["isiscb:authorityStatus"] = entry_dict["AuthorityStatus"].strip()
                
                # Add to full relationships list
                authority_relationships.append(relationship)
                
                # Normalize type for grouping
                norm_type = self._normalize_type(relationship_type)
                
                # Group by type for special handling
                if norm_type not in relationships_by_type:
                    relationships_by_type[norm_type] = []
                relationships_by_type[norm_type].append(relationship)
                
            except Exception as e:
                logger.warning(f"Error parsing related authority entry for record {record_id}: {entry}. Error: {str(e)}")
        
        # Generate result dictionary
        result = {}
        
        # Add the full list of relationships
        if authority_relationships:
            result["isiscb:relatedAuthorities"] = authority_relationships
        
        # Add specialized relationships based on type
        self._add_normalized_relationships(result, relationships_by_type)
        
        return result
    
    def _parse_entry(self, entry: str) -> Dict:
        """
        Parse a single entry into a dictionary.
        
        Args:
            entry: A single authority relationship entry
            
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
            result[key] = value.strip()
            
        return result
    
    def _normalize_type(self, relationship_type: str) -> str:
        """
        Normalize relationship type for consistent processing.
        
        Args:
            relationship_type: Original relationship type
            
        Returns:
            Normalized relationship type as camelCase
        """
        # Replace spaces with underscores and convert to uppercase for consistent lookup
        normalized = relationship_type.replace(" ", "_").upper()
        return normalized
    
    def _add_normalized_relationships(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Add normalized relationships to the result.
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Process hierarchical relationships
        self._process_hierarchical_relationships(result, relationships_by_type)
        
        # Process equivalent relationships
        self._process_equivalent_relationships(result, relationships_by_type)
        
        # Process other relationships
        self._process_other_relationships(result, relationships_by_type)
    
    def _process_hierarchical_relationships(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Process hierarchical relationships like broader/narrower terms.
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Handle broader terms (parent concepts)
        if "BROADER_TERM" in relationships_by_type:
            broader_terms = self._process_related_authorities(relationships_by_type["BROADER_TERM"])
            if broader_terms:
                result["skos:broader"] = broader_terms
        
        # Handle narrower terms (child concepts)
        if "NARROWER_TERM" in relationships_by_type:
            narrower_terms = self._process_related_authorities(relationships_by_type["NARROWER_TERM"])
            if narrower_terms:
                result["skos:narrower"] = narrower_terms
        
        # Handle parent-child institution relationships
        if "PARENT_INSTITUTION" in relationships_by_type:
            parent_institutions = self._process_related_authorities(relationships_by_type["PARENT_INSTITUTION"])
            if parent_institutions:
                result["isiscb:parentInstitution"] = parent_institutions
                # Also add as broader if it's a concept or category
                result["skos:broader"] = parent_institutions if "skos:broader" not in result else result["skos:broader"] + parent_institutions
                
        if "CHILD_INSTITUTION" in relationships_by_type:
            child_institutions = self._process_related_authorities(relationships_by_type["CHILD_INSTITUTION"])
            if child_institutions:
                result["isiscb:childInstitution"] = child_institutions
                # Also add as narrower if it's a concept or category
                result["skos:narrower"] = child_institutions if "skos:narrower" not in result else result["skos:narrower"] + child_institutions
    
    def _process_equivalent_relationships(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Process equivalent relationships like related terms.
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Handle related terms
        if "RELATED_TERM" in relationships_by_type:
            related_terms = self._process_related_authorities(relationships_by_type["RELATED_TERM"])
            if related_terms:
                result["skos:related"] = related_terms
        
        # Handle use/used for relationships
        if "USE" in relationships_by_type:
            use_terms = self._process_related_authorities(relationships_by_type["USE"])
            if use_terms:
                result["skos:exactMatch"] = use_terms
        
        if "USED_FOR" in relationships_by_type:
            used_for_terms = self._process_related_authorities(relationships_by_type["USED_FOR"])
            if used_for_terms:
                result["skos:closeMatch"] = used_for_terms
    
    def _process_other_relationships(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Process other types of relationships.
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Process all other relationship types
        for rel_type, relationships in relationships_by_type.items():
            # Skip types we've already processed
            if rel_type in ["BROADER_TERM", "NARROWER_TERM", "RELATED_TERM", 
                           "PARENT_INSTITUTION", "CHILD_INSTITUTION", "USE", "USED_FOR"]:
                continue
            
            # Create a property name for this relationship type
            property_name = f"isiscb:{self._camel_case(rel_type)}"
            
            # Process the relationships
            related_authorities = self._process_related_authorities(relationships)
            
            if related_authorities:
                result[property_name] = related_authorities
    
    def _process_related_authorities(self, relationships: List[Dict]) -> List[Dict]:
        """
        Process a list of authority relationships into structured objects.
        
        Args:
            relationships: List of relationship objects
            
        Returns:
            List of structured authority objects
        """
        authority_objects = []
        for relationship in relationships:
            authority_obj = {
                "@id": relationship["isiscb:authority"]["@id"]
            }
            
            # Add name if available
            if "isiscb:authorityName" in relationship:
                authority_obj["skos:prefLabel"] = relationship["isiscb:authorityName"]
                authority_obj["schema:name"] = relationship["isiscb:authorityName"]
            
            # Add type if available
            if "isiscb:authorityType" in relationship:
                auth_type = relationship["isiscb:authorityType"]
                if auth_type == "Concept":
                    authority_obj["@type"] = ["skos:Concept"]
                elif auth_type == "Person":
                    authority_obj["@type"] = ["schema:Person"]
                elif auth_type == "Institution":
                    authority_obj["@type"] = ["schema:Organization"]
                elif auth_type == "Geographic Term":
                    authority_obj["@type"] = ["schema:Place"]
                elif auth_type == "Time Period":
                    authority_obj["@type"] = ["dcterms:PeriodOfTime"]
                elif auth_type == "Serial Publication":
                    authority_obj["@type"] = ["bibo:Periodical"]
                else:
                    authority_obj["@type"] = ["skos:Concept"]
            
            authority_objects.append(authority_obj)
        
        return authority_objects
    
    def _camel_case(self, text: str) -> str:
        """
        Convert a string to camelCase.
        
        Args:
            text: String to convert
            
        Returns:
            camelCase string
        """
        # Remove underscores and split
        words = text.replace('_', ' ').split()
        
        # Convert to camelCase
        if not words:
            return ""
            
        # First word lowercase
        result = words[0].lower()
        
        # Capitalize subsequent words
        for word in words[1:]:
            if word:
                result += word[0].upper() + word[1:].lower()
        
        return result