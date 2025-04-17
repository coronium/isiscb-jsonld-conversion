"""
Related Authorities field converter for IsisCB JSON-LD conversion.

This module provides converters for parsing the complex Related Authorities field
that connects citations to authority records with typed relationships.
"""

import logging
import re
from typing import Dict, List, Any, Optional, Tuple

from ..base import BaseConverter
from ..schema_mappings import get_relationship_property, get_relationship_uri

logger = logging.getLogger('isiscb_conversion')

class RelatedAuthoritiesConverter(BaseConverter):
    """Converter for Related Authorities fields in citation records."""
    
    def __init__(self, field_name: str = "Related Authorities"):
        """Initialize the Related Authorities converter."""
        super().__init__(field_name)
        
        # Define standard vocabulary namespaces
        self.namespaces = {
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/",
            "schema": "http://schema.org/",
            "bibo": "http://purl.org/ontology/bibo/",
            "vivo": "http://vivoweb.org/ontology/core#",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "isiscb": "https://data.isiscb.org/vocabulary/"
        }
        
        # Define relationship groups for specialized processing
        self.person_contributors = [
            "Author", "Editor", "Contributor", "Translator", "Advisor", "Committee_Member"
        ]
        
        self.subject_types = ["Subject", "Category"]
        
        self.publication_types = ["Periodical", "Book_Series"]
        
        self.institution_types = [
            "Publisher", "School", "Institution", "Meeting", 
            "Archival_Repository"
        ]
        
        # Define rarely used relationships that will use generic processing
        self.generic_relationships = [
            "Guest", "Producer", "Director", "Writer", "Performer", 
            "Collector", "Archivist", "Researcher", "Developer", "Compiler", 
            "Distributor", "Maintaining_Institution", "Presenting_Group",
            "Awardee", "Officer", "Host", "Interviewer", "Organizer"
        ]
        
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
            
        # Parse entries and organize by type
        relationships_by_type = self._parse_and_organize_relationships(value, record_id)
        
        # Generate result dictionary
        result = {}
        
        # Add specialized relationship groups
        self._add_person_contributors(result, relationships_by_type)
        self._add_subjects(result, relationships_by_type)
        self._add_publication_relationships(result, relationships_by_type)
        self._add_institution_relationships(result, relationships_by_type)
        
        # Add generic/rare relationships
        self._add_generic_relationships(result, relationships_by_type)
        
        # Also store the full structured representation for preservation
        # if needed for specialized applications
        if any(relationships_by_type.values()):
            all_relationships = []
            for type_relationships in relationships_by_type.values():
                all_relationships.extend(type_relationships)
                
            if all_relationships:
                result["isiscb:relatedAuthorities"] = all_relationships
        
        return result
    
    def _parse_and_organize_relationships(self, value: str, record_id: str) -> Dict[str, List[Dict]]:
        """
        Parse the raw field value and organize relationships by type.
        
        Args:
            value: Raw field value
            record_id: Record ID for error logging
            
        Returns:
            Dictionary of relationship type to list of parsed relationships
        """
        # Split entries by double slash
        entries = value.split(" // ")
        
        # Dictionary to hold relationships by type
        relationships_by_type = {}
        
        for entry in entries:
            try:
                # Parse the entry into a dictionary
                entry_dict = self._parse_entry(entry)
                
                if not entry_dict or "ACRType" not in entry_dict or "AuthorityID" not in entry_dict:
                    continue
                    
                # Get relationship type and normalize
                relationship_type = entry_dict["ACRType"]
                normalized_type = self._normalize_type(relationship_type)
                
                # Create relationship object with proper type URI
                relationship = {
                    "@type": get_relationship_uri(relationship_type),
                    "isiscb:relationshipType": relationship_type,
                    "isiscb:authority": {
                        "@id": f"https://data.isiscb.org/authority/{entry_dict.get('AuthorityID', '')}"
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
                
                # Add to appropriate category
                if normalized_type not in relationships_by_type:
                    relationships_by_type[normalized_type] = []
                    
                relationships_by_type[normalized_type].append(relationship)
                
            except Exception as e:
                logger.warning(f"Error parsing related authority entry for record {record_id}: {entry}. Error: {str(e)}")
                
        return relationships_by_type
    
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
    
    def _normalize_type(self, relationship_type: str) -> str:
        """
        Normalize relationship type for consistent processing.
        
        Args:
            relationship_type: Original relationship type
            
        Returns:
            Normalized relationship type
        """
        # Replace spaces with underscores and convert to uppercase
        normalized = relationship_type.replace(" ", "_").upper()
        return normalized
    
    def _add_person_contributors(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Add person contributor relationships (authors, editors, etc).
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Process authors
        if "AUTHOR" in relationships_by_type:
            authors = self._process_authors(relationships_by_type["AUTHOR"])
            if authors:
                result["dc:creator"] = authors
                result["schema:author"] = authors
        
        # Process editors
        if "EDITOR" in relationships_by_type:
            editors = self._process_editors(relationships_by_type["EDITOR"])
            if editors:
                result["schema:editor"] = editors
                # Also add as contributors for Dublin Core compatibility
                if "dc:contributor" not in result:
                    result["dc:contributor"] = []
                result["dc:contributor"].extend(editors)
        
        # Process translators
        if "TRANSLATOR" in relationships_by_type:
            translators = self._process_generic_contributors(
                relationships_by_type["TRANSLATOR"], "translator"
            )
            if translators:
                result["schema:translator"] = translators
                # Also add as contributors for Dublin Core compatibility
                if "dc:contributor" not in result:
                    result["dc:contributor"] = []
                result["dc:contributor"].extend(translators)
                
        # Process committee members
        if "COMMITTEE_MEMBER" in relationships_by_type:
            committee_members = self._process_generic_contributors(
                relationships_by_type["COMMITTEE_MEMBER"], "committeeMember", "vivo:CommitteeMembership"
            )
            if committee_members:
                result["vivo:hasCommitteeMember"] = committee_members
                # Also add as contributors for Dublin Core compatibility
                if "dc:contributor" not in result:
                    result["dc:contributor"] = []
                result["dc:contributor"].extend(committee_members)
                
        # Process advisors
        if "ADVISOR" in relationships_by_type:
            advisors = self._process_generic_contributors(
                relationships_by_type["ADVISOR"], "advisor", "vivo:AdvisorRole"
            )
            if advisors:
                result["vivo:advisorIn"] = advisors
                # Also add as contributors for Dublin Core compatibility
                if "dc:contributor" not in result:
                    result["dc:contributor"] = []
                result["dc:contributor"].extend(advisors)
                
        # Process general contributors
        if "CONTRIBUTOR" in relationships_by_type:
            contributors = self._process_generic_contributors(
                relationships_by_type["CONTRIBUTOR"], "contributor"
            )
            if contributors:
                if "dc:contributor" not in result:
                    result["dc:contributor"] = []
                result["dc:contributor"].extend(contributors)
    
    def _add_subjects(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Add subject relationships.
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        all_subjects = []
        
        # Process subjects
        if "SUBJECT" in relationships_by_type:
            subjects = self._process_subjects(relationships_by_type["SUBJECT"])
            all_subjects.extend(subjects)
            
        # Process categories (now also treated as subjects)
        if "CATEGORY" in relationships_by_type:
            categories = self._process_subjects(relationships_by_type["CATEGORY"])
            all_subjects.extend(categories)
            
        if all_subjects:
            result["dc:subject"] = all_subjects
            result["schema:about"] = all_subjects
    
    def _add_publication_relationships(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Add publication relationships (periodicals, book series).
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Process periodicals
        if "PERIODICAL" in relationships_by_type:
            periodical = self._process_periodical(relationships_by_type["PERIODICAL"])
            if periodical:
                result["schema:isPartOf"] = periodical
                result["dcterms:isPartOf"] = periodical
                
        # Process book series
        if "BOOK_SERIES" in relationships_by_type:
            series = self._process_periodical(relationships_by_type["BOOK_SERIES"])
            if series:
                # Use same properties as periodicals
                if "schema:isPartOf" not in result:
                    result["schema:isPartOf"] = series
                elif isinstance(result["schema:isPartOf"], list):
                    result["schema:isPartOf"].extend(series if isinstance(series, list) else [series])
                else:
                    result["schema:isPartOf"] = [result["schema:isPartOf"], series]
                    
                if "dcterms:isPartOf" not in result:
                    result["dcterms:isPartOf"] = series
                elif isinstance(result["dcterms:isPartOf"], list):
                    result["dcterms:isPartOf"].extend(series if isinstance(series, list) else [series])
                else:
                    result["dcterms:isPartOf"] = [result["dcterms:isPartOf"], series]
    
    def _add_institution_relationships(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Add institution relationships (publishers, schools, etc).
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        # Process publishers
        if "PUBLISHER" in relationships_by_type:
            publisher = self._process_institution(relationships_by_type["PUBLISHER"], "publisher")
            if publisher:
                result["dc:publisher"] = publisher
                result["schema:publisher"] = publisher
                
        # Process schools
        if "SCHOOL" in relationships_by_type:
            school = self._process_institution(relationships_by_type["SCHOOL"], "school")
            if school:
                result["bibo:degreeGrantor"] = school
                # Also add Schema.org compatibility
                if not isinstance(school, list):
                    school_obj = school
                else:
                    school_obj = school[0]  # Take the first school if multiple
                
                # Add additional type for colleges/universities
                if isinstance(school_obj, dict) and "@type" in school_obj:
                    if isinstance(school_obj["@type"], list):
                        school_obj["@type"].append("schema:CollegeOrUniversity")
                    else:
                        school_obj["@type"] = [school_obj["@type"], "schema:CollegeOrUniversity"]
                
        # Process institutions
        if "INSTITUTION" in relationships_by_type:
            institution = self._process_institution(relationships_by_type["INSTITUTION"], "institution")
            if institution:
                result["isiscb:institution"] = institution
                # Add Schema.org affiliation for compatibility
                result["schema:affiliation"] = institution
                
        # Process meetings
        if "MEETING" in relationships_by_type:
            meeting = self._process_institution(relationships_by_type["MEETING"], "meeting", "Event")
            if meeting:
                result["bibo:presentedAt"] = meeting
                # Also add Schema.org compatibility
                if not isinstance(meeting, list):
                    meeting_obj = meeting
                else:
                    meeting_obj = meeting[0]  # Take the first meeting if multiple
                
                # Add additional type for events
                if isinstance(meeting_obj, dict) and "@type" in meeting_obj:
                    if isinstance(meeting_obj["@type"], list):
                        meeting_obj["@type"].append("schema:Event")
                    else:
                        meeting_obj["@type"] = [meeting_obj["@type"], "schema:Event"]
                
        # Process archival repositories
        if "ARCHIVAL_REPOSITORY" in relationships_by_type:
            repository = self._process_institution(
                relationships_by_type["ARCHIVAL_REPOSITORY"], "archivalRepository"
            )
            if repository:
                result["isiscb:archivalRepository"] = repository
                # Add vivo:ArchivalOrganization if available
                if not isinstance(repository, list):
                    repo_obj = repository
                else:
                    repo_obj = repository[0]  # Take the first repository if multiple
                
                # Add additional type for archival organizations
                if isinstance(repo_obj, dict) and "@type" in repo_obj:
                    if isinstance(repo_obj["@type"], list):
                        repo_obj["@type"].append("vivo:ArchivalOrganization")
                    else:
                        repo_obj["@type"] = [repo_obj["@type"], "vivo:ArchivalOrganization"]
    
    def _add_generic_relationships(self, result: Dict, relationships_by_type: Dict) -> None:
        """
        Add rarely used relationships using generic processing.
        
        Args:
            result: The result dictionary to update
            relationships_by_type: Dictionary of relationships grouped by type
        """
        for rel_type in self.generic_relationships:
            normalized = rel_type.upper()
            if normalized in relationships_by_type:
                # Get the property name from schema mappings
                property_name = get_relationship_property(rel_type)
                
                # Process the relationships
                processed = self._process_generic_contributors(
                    relationships_by_type[normalized], 
                    rel_type.lower()
                )
                
                if processed:
                    # Add to result with the appropriate property
                    result[property_name] = processed
                    
                    # If it's a contributor type, add to dc:contributor as well
                    if "dc:contributor" in property_name or rel_type.lower() in [
                        "interviewer", "organizer", "guest", "host", "performer", 
                        "researcher", "compiler", "collector", "archivist"
                    ]:
                        if "dc:contributor" not in result:
                            result["dc:contributor"] = []
                        result["dc:contributor"].extend(processed)
    
    def _process_authors(self, author_relationships: List[Dict]) -> List[Dict]:
        """
        Process author relationships into standardized author objects.
        
        Args:
            author_relationships: List of author relationship objects
            
        Returns:
            List of author objects in Schema.org-compatible format
        """
        # Sort by display order
        sorted_authors = sorted(
            author_relationships, 
            key=lambda p: float(p.get("isiscb:displayOrder", "1.0"))
        )
        
        author_objects = []
        for idx, author in enumerate(sorted_authors):
            # Create base author object with proper ID
            author_obj = {
                "@id": author["isiscb:authority"]["@id"]
            }
            
            # Set appropriate type based on authority type
            if "isiscb:authorityType" in author:
                authority_type = author["isiscb:authorityType"]
                if authority_type == "Institution" or authority_type == "Organization":
                    author_obj["@type"] = ["schema:Organization", "foaf:Organization"]
                else:
                    author_obj["@type"] = ["schema:Person", "foaf:Person"]
            else:
                # Default to Person
                author_obj["@type"] = ["schema:Person", "foaf:Person"]
            
            # Handle name (prioritize display name over authority name)
            if "isiscb:displayName" in author and author["isiscb:displayName"]:
                display_name = author["isiscb:displayName"].strip()
                author_obj["schema:name"] = display_name
                author_obj["name"] = display_name  # For compatibility
            elif "isiscb:authorityName" in author:
                authority_name = author["isiscb:authorityName"].strip()
                author_obj["schema:name"] = authority_name
                author_obj["name"] = authority_name  # For compatibility
            else:
                # Fallback using ID as placeholder
                authority_id = author["isiscb:authority"]["@id"].split("/")[-1]
                author_obj["schema:name"] = f"Author {authority_id}"
                author_obj["name"] = f"Author {authority_id}"  # For compatibility
            
            # Add position information (order in author list)
            position = author.get("isiscb:displayOrder", str(idx + 1))
            author_obj["schema:position"] = position
            author_obj["isiscb:position"] = position  # For compatibility
            
            # Add role information
            author_obj["schema:roleName"] = "author"
            author_obj["isiscb:role"] = "author"  # For compatibility
            
            author_objects.append(author_obj)
        
        return author_objects
    
    def _process_editors(self, editor_relationships: List[Dict]) -> List[Dict]:
        """
        Process editor relationships into standardized editor objects.
        
        Args:
            editor_relationships: List of editor relationship objects
            
        Returns:
            List of editor objects in Schema.org-compatible format
        """
        # Similar to authors but with editor role
        sorted_editors = sorted(
            editor_relationships, 
            key=lambda p: float(p.get("isiscb:displayOrder", "1.0"))
        )
        
        editor_objects = []
        for idx, editor in enumerate(sorted_editors):
            # Create base editor object with proper ID
            editor_obj = {
                "@id": editor["isiscb:authority"]["@id"]
            }
            
            # Set appropriate type based on authority type
            if "isiscb:authorityType" in editor:
                authority_type = editor["isiscb:authorityType"]
                if authority_type == "Institution" or authority_type == "Organization":
                    editor_obj["@type"] = ["schema:Organization", "foaf:Organization"]
                else:
                    editor_obj["@type"] = ["schema:Person", "foaf:Person"]
            else:
                # Default to Person
                editor_obj["@type"] = ["schema:Person", "foaf:Person"]
            
            # Handle name (prioritize display name over authority name)
            if "isiscb:displayName" in editor and editor["isiscb:displayName"]:
                display_name = editor["isiscb:displayName"].strip()
                editor_obj["schema:name"] = display_name
                editor_obj["name"] = display_name  # For compatibility
            elif "isiscb:authorityName" in editor:
                authority_name = editor["isiscb:authorityName"].strip()
                editor_obj["schema:name"] = authority_name
                editor_obj["name"] = authority_name  # For compatibility
            else:
                # Fallback using ID as placeholder
                authority_id = editor["isiscb:authority"]["@id"].split("/")[-1]
                editor_obj["schema:name"] = f"Editor {authority_id}"
                editor_obj["name"] = f"Editor {authority_id}"  # For compatibility
            
            # Add position information (order in editor list)
            position = editor.get("isiscb:displayOrder", str(idx + 1))
            editor_obj["schema:position"] = position
            editor_obj["isiscb:position"] = position  # For compatibility
            
            # Add role information
            editor_obj["schema:roleName"] = "editor"
            editor_obj["isiscb:role"] = "editor"  # For compatibility
            
            editor_objects.append(editor_obj)
        
        return editor_objects
    
    def _process_generic_contributors(self, relationships: List[Dict], role: str, role_type: str = None) -> List[Dict]:
        """
        Process generic contributor relationships.
        
        Args:
            relationships: List of relationship objects
            role: Role name (e.g., "translator", "advisor")
            role_type: Optional VIVO role type URI
            
        Returns:
            List of contributor objects
        """
        # Sort by display order
        sorted_contributors = sorted(
            relationships, 
            key=lambda p: float(p.get("isiscb:displayOrder", "1.0"))
        )
        
        contributor_objects = []
        for idx, contributor in enumerate(sorted_contributors):
            # Create base contributor object with proper ID
            contributor_obj = {
                "@id": contributor["isiscb:authority"]["@id"]
            }
            
            # Set appropriate type based on authority type
            if "isiscb:authorityType" in contributor:
                authority_type = contributor["isiscb:authorityType"]
                if authority_type == "Institution" or authority_type == "Organization":
                    contributor_obj["@type"] = ["schema:Organization", "foaf:Organization"]
                else:
                    contributor_obj["@type"] = ["schema:Person", "foaf:Person"]
            else:
                # Default to Person
                contributor_obj["@type"] = ["schema:Person", "foaf:Person"]
            
            # Add VIVO role type if provided
            if role_type:
                if isinstance(contributor_obj["@type"], list):
                    contributor_obj["@type"].append(role_type)
                else:
                    contributor_obj["@type"] = [contributor_obj["@type"], role_type]
            
            # Handle name (prioritize display name over authority name)
            if "isiscb:displayName" in contributor and contributor["isiscb:displayName"]:
                display_name = contributor["isiscb:displayName"].strip()
                contributor_obj["schema:name"] = display_name
                contributor_obj["name"] = display_name  # For compatibility
            elif "isiscb:authorityName" in contributor:
                authority_name = contributor["isiscb:authorityName"].strip()
                contributor_obj["schema:name"] = authority_name
                contributor_obj["name"] = authority_name  # For compatibility
            else:
                # Fallback using ID as placeholder
                authority_id = contributor["isiscb:authority"]["@id"].split("/")[-1]
                contributor_obj["schema:name"] = f"{role.capitalize()} {authority_id}"
                contributor_obj["name"] = f"{role.capitalize()} {authority_id}"  # For compatibility
            
            # Add position information if available
            if "isiscb:displayOrder" in contributor:
                position = contributor["isiscb:displayOrder"]
                contributor_obj["schema:position"] = position
                contributor_obj["isiscb:position"] = position  # For compatibility
            
            # Add role information
            contributor_obj["schema:roleName"] = role
            contributor_obj["isiscb:role"] = role  # For compatibility
            
            contributor_objects.append(contributor_obj)
        
        return contributor_objects
    
    def _process_subjects(self, subject_relationships: List[Dict]) -> List[Dict]:
        """
        Process subject relationships into standardized subject objects.
        
        Args:
            subject_relationships: List of subject relationship objects
            
        Returns:
            List of subject objects
        """
        subject_objects = []
        for subject in subject_relationships:
            # Create base subject object with proper ID
            subject_obj = {
                "@id": subject["isiscb:authority"]["@id"]
            }
            
            # Set appropriate type based on authority type
            if "isiscb:authorityType" in subject:
                authority_type = subject["isiscb:authorityType"]
                if authority_type == "Concept":
                    subject_obj["@type"] = ["skos:Concept"]
                elif authority_type == "Geographic Term":
                    subject_obj["@type"] = ["schema:Place"]
                elif authority_type == "Time Period":
                    subject_obj["@type"] = ["dcterms:PeriodOfTime"]
                else:
                    subject_obj["@type"] = ["skos:Concept"]
            else:
                # Default to Concept
                subject_obj["@type"] = ["skos:Concept"]
            
            # Handle name (use authority name)
            if "isiscb:authorityName" in subject:
                authority_name = subject["isiscb:authorityName"].strip()
                subject_obj["skos:prefLabel"] = authority_name
                subject_obj["schema:name"] = authority_name
                subject_obj["name"] = authority_name  # For compatibility
            else:
                # Fallback using ID as placeholder
                authority_id = subject["isiscb:authority"]["@id"].split("/")[-1]
                subject_obj["skos:prefLabel"] = f"Subject {authority_id}"
                subject_obj["schema:name"] = f"Subject {authority_id}"
                subject_obj["name"] = f"Subject {authority_id}"  # For compatibility
            
            subject_objects.append(subject_obj)
        
        return subject_objects
    
    def _process_periodical(self, periodical_relationships: List[Dict]) -> Dict:
        """
        Process periodical or series relationships.
        
        Args:
            periodical_relationships: List of periodical relationship objects
            
        Returns:
            Periodical object or list of periodical objects
        """
        if not periodical_relationships:
            return None
        
        # If multiple periodicals, process as list
        if len(periodical_relationships) > 1:
            periodical_objects = []
            for periodical in periodical_relationships:
                periodical_obj = self._create_publication_object(periodical)
                if periodical_obj:
                    periodical_objects.append(periodical_obj)
            return periodical_objects
        
        # Process single periodical
        return self._create_publication_object(periodical_relationships[0])
    
    def _create_publication_object(self, relationship: Dict) -> Dict:
        """
        Create a publication object (periodical/series) from a relationship.
        
        Args:
            relationship: The relationship object
            
        Returns:
            Publication object
        """
        # Create base object with ID
        publication_obj = {
            "@id": relationship["isiscb:authority"]["@id"]
        }
        
        # Set appropriate type
        if "isiscb:authorityType" in relationship:
            authority_type = relationship["isiscb:authorityType"]
            if authority_type == "Serial Publication":
                publication_obj["@type"] = ["bibo:Periodical", "schema:Periodical"]
            else:
                publication_obj["@type"] = ["bibo:Series", "schema:Series"]
        else:
            # Default to Periodical
            publication_obj["@type"] = ["bibo:Periodical", "schema:Periodical"]
        
        # Handle name (prioritize display name over authority name)
        if "isiscb:displayName" in relationship and relationship["isiscb:displayName"]:
            display_name = relationship["isiscb:displayName"].strip()
            publication_obj["dc:title"] = display_name
            publication_obj["schema:name"] = display_name
            publication_obj["name"] = display_name  # For compatibility
        elif "isiscb:authorityName" in relationship:
            authority_name = relationship["isiscb:authorityName"].strip()
            publication_obj["dc:title"] = authority_name
            publication_obj["schema:name"] = authority_name
            publication_obj["name"] = authority_name  # For compatibility
        else:
            # Fallback using ID as placeholder
            authority_id = relationship["isiscb:authority"]["@id"].split("/")[-1]
            publication_obj["dc:title"] = f"Publication {authority_id}"
            publication_obj["schema:name"] = f"Publication {authority_id}"
            publication_obj["name"] = f"Publication {authority_id}"  # For compatibility
        
        return publication_obj
    
    def _process_institution(self, institution_relationships: List[Dict], role: str, type_override: str = None) -> Dict:
        """
        Process institution relationships.
        
        Args:
            institution_relationships: List of institution relationship objects
            role: Role of the institution (publisher, school, etc.)
            type_override: Optional override for the institution type
            
        Returns:
            Institution object or list of institution objects
        """
        if not institution_relationships:
            return None
        
        # If multiple institutions, process as list
        if len(institution_relationships) > 1:
            institution_objects = []
            for institution in institution_relationships:
                institution_obj = self._create_institution_object(institution, role, type_override)
                if institution_obj:
                    institution_objects.append(institution_obj)
            return institution_objects
        
        # Process single institution
        return self._create_institution_object(institution_relationships[0], role, type_override)
    
    def _create_institution_object(self, relationship: Dict, role: str, type_override: str = None) -> Dict:
        """
        Create an institution object from a relationship.
        
        Args:
            relationship: The relationship object
            role: Role of the institution
            type_override: Optional override for the institution type
            
        Returns:
            Institution object
        """
        # Create base object with ID
        institution_obj = {
            "@id": relationship["isiscb:authority"]["@id"]
        }
        
        # Set appropriate type
        if type_override:
            institution_obj["@type"] = [f"schema:{type_override}", f"foaf:{type_override}"]
        elif "isiscb:authorityType" in relationship:
            authority_type = relationship["isiscb:authorityType"]
            if authority_type == "Institution":
                institution_obj["@type"] = ["schema:Organization", "foaf:Organization"]
            elif authority_type == "Event":
                institution_obj["@type"] = ["schema:Event"]
            else:
                institution_obj["@type"] = ["schema:Organization", "foaf:Organization"]
        else:
            # Default to Organization
            institution_obj["@type"] = ["schema:Organization", "foaf:Organization"]
        
        # Add role type information
        institution_obj["isiscb:role"] = role
        
        # Handle name (prioritize display name over authority name)
        if "isiscb:displayName" in relationship and relationship["isiscb:displayName"]:
            display_name = relationship["isiscb:displayName"].strip()
            institution_obj["schema:name"] = display_name
            institution_obj["name"] = display_name  # For compatibility
        elif "isiscb:authorityName" in relationship:
            authority_name = relationship["isiscb:authorityName"].strip()
            institution_obj["schema:name"] = authority_name
            institution_obj["name"] = authority_name  # For compatibility
        else:
            # Fallback using ID as placeholder
            authority_id = relationship["isiscb:authority"]["@id"].split("/")[-1]
            institution_obj["schema:name"] = f"{role.capitalize()} {authority_id}"
            institution_obj["name"] = f"{role.capitalize()} {authority_id}"  # For compatibility
        
        return institution_obj