"""
Related Authorities field converter for IsisCB JSON-LD conversion.

This module provides converters for parsing the complex Related Authorities field
that connects citations to authority records with typed relationships.
"""

import logging
import re
from typing import Dict, List, Any, Optional

from ..base import BaseConverter
from ..schema_mappings import get_relationship_property, get_relationship_uri

logger = logging.getLogger('isiscb_conversion')

class RelatedAuthoritiesConverter(BaseConverter):
    """Converter for Related Authorities fields in citation records."""
    
    def __init__(self, field_name: str = "Related Authorities"):
        """Initialize the Related Authorities converter."""
        super().__init__(field_name)
        
    def _convert_impl(self, value: str, record_id: str) -> Dict:
        """
        Convert Related Authorities field to JSON-LD format.
        
        Args:
            value: The raw Related Authorities string
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of the related authorities
        """
        if not value or value.strip() == "":
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
                    "@type": get_relationship_uri(relationship_type),
                    "isiscb:relationshipType": relationship_type,
                    "isiscb:displayOrder": entry_dict.get("ACRDisplayOrder", "1.0"),
                    "isiscb:authority": {
                        "@id": f"https://data.isiscb.org/authority/{entry_dict.get('AuthorityID', '')}"
                    }
                }
                
                # Add other properties
                if "AuthorityName" in entry_dict:
                    relationship["isiscb:authorityName"] = entry_dict["AuthorityName"]
                    
                if "AuthorityType" in entry_dict:
                    relationship["isiscb:authorityType"] = entry_dict["AuthorityType"]
                    
                if "ACRNameForDisplayInCitation" in entry_dict and entry_dict["ACRNameForDisplayInCitation"].strip():
                    relationship["isiscb:displayName"] = entry_dict["ACRNameForDisplayInCitation"]
                
                # Add status if available
                if "AuthorityStatus" in entry_dict:
                    relationship["isiscb:authorityStatus"] = entry_dict["AuthorityStatus"]
                
                # Add to full relationships list
                authority_relationships.append(relationship)
                
                # Group by type for special handling
                if relationship_type not in relationships_by_type:
                    relationships_by_type[relationship_type] = []
                relationships_by_type[relationship_type].append(relationship)
                
            except Exception as e:
                logger.warning(f"Error parsing related authority entry for record {record_id}: {entry}. Error: {str(e)}")
        
        # Generate result dictionary
        result = {}
        
        # First, add the full list
        if authority_relationships:
            result["isiscb:relatedAuthorities"] = authority_relationships
        
        # Process different types of relationships
        self._add_creator_contributors(result, relationships_by_type)
        self._add_subjects_and_categories(result, relationships_by_type)
        self._add_publishing_info(result, relationships_by_type)
        self._add_institutional_relationships(result, relationships_by_type)
        
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
                
            key, value = part.split(" ", 1)
            result[key] = value.strip()
            
        return result
    
    def _add_creator_contributors(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Add creator and contributor relationships to the result.
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Process authors
        if "Author" in relationships_by_type:
            result[get_relationship_property("Author")] = self._process_persons(
                relationships_by_type["Author"], "author"
            )
        
        # Process editors
        if "Editor" in relationships_by_type:
            result[get_relationship_property("Editor")] = self._process_persons(
                relationships_by_type["Editor"], "editor"
            )
        
        # Process other contributor types
        contributor_types = [
            "Advisor", "Contributor", "Translator", "Committee_Member", 
            "Interviewer", "Guest", "Writer", "Performer", "Researcher",
            "Director", "Producer", "Organizer", "Host"
        ]
        
        all_contributors = []
        for rel_type in contributor_types:
            if rel_type in relationships_by_type:
                contributors = self._process_persons(
                    relationships_by_type[rel_type], rel_type.lower()
                )
                all_contributors.extend(contributors)
        
        if all_contributors:
            result["dc:contributor"] = all_contributors
    
    def _add_subjects_and_categories(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Add subject and category relationships to the result.
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Process subjects
        if "Subject" in relationships_by_type:
            result["dc:subject"] = self._process_subjects(relationships_by_type["Subject"])
        
        # Process categories
        if "Category" in relationships_by_type:
            result["isiscb:category"] = self._process_subjects(relationships_by_type["Category"])
    
    def _add_publishing_info(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Add publishing-related relationships to the result.
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Process periodical
        if "Periodical" in relationships_by_type:
            result["schema:isPartOf"] = self._process_periodical(relationships_by_type["Periodical"])
        
        # Process publisher
        if "Publisher" in relationships_by_type:
            result["dc:publisher"] = self._process_publisher(relationships_by_type["Publisher"])
        
        # Process book series
        if "Book_Series" in relationships_by_type:
            result["isiscb:bookSeries"] = self._process_book_series(relationships_by_type["Book_Series"])
        
        # Process distributor
        if "Distributor" in relationships_by_type:
            result["schema:distributor"] = self._process_publisher(relationships_by_type["Distributor"])
    
    def _add_institutional_relationships(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Add institutional relationships to the result.
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Process school
        if "School" in relationships_by_type:
            result["schema:school"] = self._process_institution(relationships_by_type["School"])
        
        # Process institution
        if "Institution" in relationships_by_type:
            result["isiscb:institution"] = self._process_institution(relationships_by_type["Institution"])
        
        # Process meeting
        if "Meeting" in relationships_by_type:
            result["bibo:presentedAt"] = self._process_event(relationships_by_type["Meeting"])
        
        # Process archival repository
        if "Archival_Repository" in relationships_by_type:
            result["isiscb:archivalRepository"] = self._process_institution(
                relationships_by_type["Archival_Repository"]
            )
        
        # Process maintaining institution
        if "Maintaining_Institution" in relationships_by_type:
            result["isiscb:maintainingInstitution"] = self._process_institution(
                relationships_by_type["Maintaining_Institution"]
            )
    
    def _process_persons(self, persons: List[Dict], role: str) -> List[Dict]:
        """
        Process person relationships into proper person objects.
        
        Args:
            persons: List of person relationship objects
            role: Role of the persons (e.g., "author", "editor")
            
        Returns:
            List of person objects in JSON-LD format
        """
        # Sort by display order
        sorted_persons = sorted(persons, key=lambda p: float(p.get("isiscb:displayOrder", "1.0")))
        
        # Create person objects
        person_objects = []
        for person in sorted_persons:
            person_obj = {
                "@id": person["isiscb:authority"]["@id"],
                "isiscb:role": role
            }
            
            # Use display name if available, otherwise use authority name
            if "isiscb:displayName" in person and person["isiscb:displayName"].strip():
                person_obj["name"] = person["isiscb:displayName"]
            elif "isiscb:authorityName" in person:
                person_obj["name"] = person["isiscb:authorityName"]
                
            # Add position in the list
            person_obj["isiscb:position"] = person.get("isiscb:displayOrder", "1.0")
            
            # Add authority type
            if "isiscb:authorityType" in person:
                person_obj["isiscb:authorityType"] = person["isiscb:authorityType"]
            
            person_objects.append(person_obj)
            
        return person_objects
    
    def _process_subjects(self, subjects: List[Dict]) -> List[Dict]:
        """
        Process subject relationships into proper subject objects.
        
        Args:
            subjects: List of subject relationship objects
            
        Returns:
            List of subject objects in JSON-LD format
        """
        subject_objects = []
        for subject in subjects:
            subject_obj = {
                "@id": subject["isiscb:authority"]["@id"]
            }
            
            if "isiscb:authorityName" in subject:
                subject_obj["name"] = subject["isiscb:authorityName"]
                
            if "isiscb:authorityType" in subject:
                subject_obj["isiscb:type"] = subject["isiscb:authorityType"]
                
            subject_objects.append(subject_obj)
            
        return subject_objects
    
    def _process_periodical(self, periodicals: List[Dict]) -> Dict:
        """
        Process periodical relationships.
        
        Args:
            periodicals: List of periodical relationship objects
            
        Returns:
            Periodical object in JSON-LD format or list if multiple
        """
        # If multiple periodicals (rare), return as list
        if len(periodicals) > 1:
            return [self._create_entity_obj(p) for p in periodicals]
        
        # Usually there's only one periodical, so take the first one
        if not periodicals:
            return {}
            
        return self._create_entity_obj(periodicals[0])
    
    def _process_publisher(self, publishers: List[Dict]) -> Dict:
        """
        Process publisher relationships.
        
        Args:
            publishers: List of publisher relationship objects
            
        Returns:
            Publisher object in JSON-LD format or list if multiple
        """
        # If multiple publishers, return as list
        if len(publishers) > 1:
            return [self._create_entity_obj(p) for p in publishers]
        
        # Usually there's only one publisher, so take the first one
        if not publishers:
            return {}
            
        return self._create_entity_obj(publishers[0])
    
    def _process_book_series(self, series: List[Dict]) -> Dict:
        """
        Process book series relationships.
        
        Args:
            series: List of book series relationship objects
            
        Returns:
            Book series object in JSON-LD format
        """
        if not series:
            return {}
            
        return self._create_entity_obj(series[0])
    
    def _process_institution(self, institutions: List[Dict]) -> Dict:
        """
        Process institution relationships.
        
        Args:
            institutions: List of institution relationship objects
            
        Returns:
            Institution object in JSON-LD format or list if multiple
        """
        # If multiple institutions, return as list
        if len(institutions) > 1:
            return [self._create_entity_obj(i) for i in institutions]
        
        if not institutions:
            return {}
            
        return self._create_entity_obj(institutions[0])
    
    def _process_event(self, events: List[Dict]) -> Dict:
        """
        Process event relationships.
        
        Args:
            events: List of event relationship objects
            
        Returns:
            Event object in JSON-LD format
        """
        if not events:
            return {}
            
        return self._create_entity_obj(events[0])
    
    def _create_entity_obj(self, relationship: Dict) -> Dict:
        """
        Create a basic entity object from a relationship.
        
        Args:
            relationship: The relationship object
            
        Returns:
            Entity object in JSON-LD format
        """
        entity_obj = {
            "@id": relationship["isiscb:authority"]["@id"]
        }
        
        if "isiscb:displayName" in relationship and relationship["isiscb:displayName"].strip():
            entity_obj["name"] = relationship["isiscb:displayName"]
        elif "isiscb:authorityName" in relationship:
            entity_obj["name"] = relationship["isiscb:authorityName"]
            
        if "isiscb:authorityType" in relationship:
            entity_obj["isiscb:type"] = relationship["isiscb:authorityType"]
            
        return entity_obj