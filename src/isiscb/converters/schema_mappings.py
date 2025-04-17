"""
Centralized schema mapping definitions for IsisCB JSON-LD conversion.

This module defines all vocabulary mappings and equivalences used across
the conversion process, ensuring consistency in property usage.
"""

import logging
logger = logging.getLogger('isiscb_conversion')

from typing import Dict, List, Any

# Standard namespace definitions
NAMESPACES = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "schema": "http://schema.org/",
    "bibo": "http://purl.org/ontology/bibo/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "prism": "http://prismstandard.org/namespaces/basic/2.0/",
    "vivo": "http://vivoweb.org/ontology/core#",
    "isiscb": "https://ontology.isiscb.org/vocabulary/"
}

# Title property mappings
TITLE_MAPPINGS = {
    "primary": "dc:title",
    "equivalents": ["schema:name", "isiscb:title"],
    "extensions": ["isiscb:mainTitle", "isiscb:subtitle"]
}

# Author/Creator property mappings
AUTHOR_MAPPINGS = {
    "primary": "dc:creator",
    "equivalents": ["schema:author", "isiscb:author"],
    "extensions": ["isiscb:authorRole", "isiscb:authorOrder"]
}

# Date property mappings
DATE_MAPPINGS = {
    "primary": "dc:date",
    "equivalents": ["schema:datePublished", "isiscb:publicationDate"],
    "extensions": ["isiscb:yearNormalized", "isiscb:dateOriginal"]
}

# Publisher property mappings
PUBLISHER_MAPPINGS = {
    "primary": "dc:publisher",
    "equivalents": ["schema:publisher"],
    "extensions": ["isiscb:publisherLocation"]
}

# Subject property mappings
SUBJECT_MAPPINGS = {
    "primary": "dc:subject",
    "equivalents": ["schema:about"],
    "extensions": ["isiscb:categoryNumber", "isiscb:subjectClassification"]
}

# Language property mappings
LANGUAGE_MAPPINGS = {
    "primary": "dc:language",
    "equivalents": ["schema:inLanguage"],
    "extensions": []
}

# Identifier property mappings
IDENTIFIER_MAPPINGS = {
    "primary": "dc:identifier",
    "equivalents": ["schema:identifier"],
    "extensions": ["isiscb:recordID", "isiscb:recid"]
}

AUTHORITY_RELATIONSHIP_MAPPINGS = {
    "primary": "isiscb:relatedAuthority",
    "equivalents": [],
    "extensions": []
}

# Relationship type mappings for Related Authorities
# Relationship type mappings for Related Authorities
AUTHORITY_RELATIONSHIP_TYPES = {
    "AUTHOR": {
        "primary": "dc:creator",
        "equivalents": ["schema:author"],
        "uri": "isiscb:author"
    },
    "EDITOR": {
        "primary": "schema:editor",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Editor is a type of contributor
        "uri": "isiscb:editor"
    },
    "ADVISOR": {
        "primary": "vivo:AdvisorRole",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Advisor is a type of contributor
        "uri": "isiscb:advisor"
    },
    "CONTRIBUTOR": {
        "primary": "dc:contributor",
        "equivalents": [],
        "uri": "isiscb:contributor"
    },
    "TRANSLATOR": {
        "primary": "schema:translator",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Translator is a type of contributor
        "uri": "isiscb:translator"
    },
    "SUBJECT": {
        "primary": "dc:subject",
        "equivalents": ["schema:about"],
        "uri": "isiscb:subject"
    },
    "CATEGORY": {
        "primary": "dc:subject",
        "equivalents": ["schema:about"],
        "uri": "isiscb:category"
    },
    "PUBLISHER": {
        "primary": "dc:publisher",
        "equivalents": ["schema:publisher"],
        "uri": "isiscb:publisher"
    },
    "SCHOOL": {
        "primary": "bibo:degreeGrantor",
        "equivalents": ["schema:CollegeOrUniversity"],
        "subPropertyOf": ["dc:publisher"],  # School is a specific kind of publisher
        "uri": "isiscb:school"
    },
    "INSTITUTION": {
        "primary": "isiscb:institution",
        "equivalents": [],
        "uri": "isiscb:institution"
    },
    "MEETING": {
        "primary": "bibo:presentedAt",
        "equivalents": [],
        "uri": "isiscb:meeting"
    },
    "PERIODICAL": {
        "primary": "schema:isPartOf",
        "equivalents": ["dc:isPartOf"],
        "uri": "isiscb:periodical"
    },
    "BOOK_SERIES": {
        "primary": "schema:isPartOf",
        "equivalents": ["dc:isPartOf"],
        "uri": "isiscb:bookSeries"
    },
    "COMMITTEE_MEMBER": {
        "primary": "vivo:CommitteeMembership",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Committee member is a type of contributor
        "uri": "isiscb:committeeMember"
    },
    "ORGANIZER": {
        "primary": "isiscb:organizer",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Organizer is a type of contributor
        "uri": "isiscb:organizer"
    },
    "INTERVIEWER": {
        "primary": "isiscb:interviewer",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Interviewer is a type of contributor
        "uri": "isiscb:interviewer"
    },
    "GUEST": {
        "primary": "isiscb:guest",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Guest is a type of contributor
        "uri": "isiscb:guest"
    },
    "CREATOR": {
        "primary": "dc:creator",
        "equivalents": ["schema:creator"],
        "uri": "isiscb:creator"
    },
    "PRODUCER": {
        "primary": "schema:producer",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Producer is a type of contributor
        "uri": "isiscb:producer"
    },
    "DIRECTOR": {
        "primary": "schema:director",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Director is a type of contributor
        "uri": "isiscb:director"
    },
    "WRITER": {
        "primary": "schema:author",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:creator"],  # Writer is a type of creator
        "uri": "isiscb:writer"
    },
    "PERFORMER": {
        "primary": "schema:performer",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Performer is a type of contributor
        "uri": "isiscb:performer"
    },
    "COLLECTOR": {
        "primary": "isiscb:collector",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Collector is a type of contributor
        "uri": "isiscb:collector"
    },
    "ARCHIVIST": {
        "primary": "isiscb:archivist",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Archivist is a type of contributor
        "uri": "isiscb:archivist"
    },
    "RESEARCHER": {
        "primary": "isiscb:researcher",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Researcher is a type of contributor
        "uri": "isiscb:researcher"
    },
    "DEVELOPER": {
        "primary": "isiscb:developer",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Developer is a type of contributor
        "uri": "isiscb:developer"
    },
    "COMPILER": {
        "primary": "isiscb:compiler",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Compiler is a type of contributor
        "uri": "isiscb:compiler"
    },
    "AWARDEE": {
        "primary": "isiscb:awardee",
        "equivalents": [],
        "uri": "isiscb:awardee"
    },
    "OFFICER": {
        "primary": "isiscb:officer",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Officer is a type of contributor
        "uri": "isiscb:officer"
    },
    "HOST": {
        "primary": "isiscb:host",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Host is a type of contributor
        "uri": "isiscb:host"
    },
    "DISTRIBUTOR": {
        "primary": "schema:distributor",
        "equivalents": [],
        "uri": "isiscb:distributor"
    },
    "ARCHIVAL_REPOSITORY": {
        "primary": "isiscb:archivalRepository",
        "equivalents": [],
        "uri": "isiscb:archivalRepository"
    },
    "MAINTAINING_INSTITUTION": {
        "primary": "isiscb:maintainingInstitution",
        "equivalents": [],
        "uri": "isiscb:maintainingInstitution"
    },
    "PRESENTING_GROUP": {
        "primary": "isiscb:presentingGroup",
        "equivalents": [],  # Remove from equivalents
        "subPropertyOf": ["dc:contributor"],  # Presenting group is a type of contributor
        "uri": "isiscb:presentingGroup"
    }
}
# All property mappings dictionary
ALL_MAPPINGS = {
    "title": TITLE_MAPPINGS,
    "author": AUTHOR_MAPPINGS,
    "date": DATE_MAPPINGS,
    "publisher": PUBLISHER_MAPPINGS,
    "subject": SUBJECT_MAPPINGS,
    "language": LANGUAGE_MAPPINGS,
    "identifier": IDENTIFIER_MAPPINGS,
    "relationships": AUTHORITY_RELATIONSHIP_MAPPINGS, 
}

# Citation type mappings (Record Type to standard vocabulary types)
CITATION_TYPE_MAPPING = {
    "Book": ["bibo:Book", "schema:Book"],
    "Article": ["bibo:Article", "schema:ScholarlyArticle"],
    "Thesis": ["bibo:Thesis", "schema:Thesis"],
    "Chapter": ["bibo:Chapter", "schema:Chapter"],
    "Review": ["bibo:AcademicArticle", "schema:Review"],
    "Essay": ["bibo:AcademicArticle"],
    "Website": ["schema:WebSite"],
    "Conference Proceeding": ["bibo:Proceedings"],
    "Conference Paper": ["bibo:AcademicArticle", "schema:Article"]
}
CITATION_RELATIONSHIP_TYPES = {
    "INCLUDES": {
        "primary": "isiscb:includes",
        "equivalents": [],
        "uri": "isiscb:includes"
    },
    "REFERENCES": {
        "primary": "isiscb:references", 
        "equivalents": ["dcterms:references"],
        "uri": "isiscb:references"
    },
    "REVIEWSBOOK": {
        "primary": "isiscb:reviewsBook",
        "equivalents": [],
        "uri": "isiscb:reviewsBook"
    },
    "ISREVIEWOF": {
        "primary": "isiscb:isReviewOf",
        "equivalents": [],
        "uri": "isiscb:isReviewOf"
    },
    "RESPONDTO": {
        "primary": "isiscb:respondsTo",
        "equivalents": [],
        "uri": "isiscb:respondsTo"
    },
    "ISRESPONSETO": {
        "primary": "isiscb:isResponseTo",
        "equivalents": [],
        "uri": "isiscb:isResponseTo"
    },
    "ISPARTOF": {
        "primary": "dcterms:isPartOf",
        "equivalents": ["schema:isPartOf"],
        "uri": "isiscb:isPartOf"
    },
    "HASPART": {
        "primary": "dcterms:hasPart",
        "equivalents": ["schema:hasPart"],
        "uri": "isiscb:hasPart"
    }
}

# Authority type mappings (Record Type to standard vocabulary types)
AUTHORITY_TYPE_MAPPING = {
    "Person": ["schema:Person", "foaf:Person"],
    "Institution": ["schema:Organization", "foaf:Organization"],
    "Geographic Term": ["schema:Place"],
    "Concept": ["skos:Concept"],
    "Time Period": ["dcterms:PeriodOfTime"],
    "Serial Publication": ["bibo:Periodical"],
    "Event": ["schema:Event"],
    "Creative Work": ["schema:CreativeWork"],
    "Category Division": ["skos:Collection"],
    "Cross-reference": ["skos:Collection"]
}

# Record status mappings
RECORD_STATUS_MAPPING = {
    "Active": "Active",
    "Inactive": "Inactive",
    "Delete": "Delete",
    "Redirect": "Redirect"
}
def get_context_mappings() -> Dict[str, Any]:
    """
    Generate context mappings for JSON-LD.
    
    Returns:
        Dict containing JSON-LD context with namespaces and property equivalences
    """
    context = NAMESPACES.copy()
    
    # Add property equivalences for all standard mappings
    for mapping_key, mapping in ALL_MAPPINGS.items():
        primary = mapping["primary"]
        for equivalent in mapping["equivalents"]:
            context[equivalent] = {"@id": primary}
    
    # Add relationship equivalences
    for rel_type, rel_mapping in AUTHORITY_RELATIONSHIP_TYPES.items():
        primary = rel_mapping["primary"]
        
        # Add equivalent properties (bidirectional mapping)
        for equivalent in rel_mapping.get("equivalents", []):
            if equivalent not in context:  # Avoid overwriting existing mappings
                context[equivalent] = {"@id": primary}
        
        # Add hierarchical relationships (unidirectional mapping)
        if "subPropertyOf" in rel_mapping:
            # Define that this property is a subproperty of another
            context[primary] = {
                "@id": primary,
                "@subPropertyOf": rel_mapping["subPropertyOf"]
            }
    
    return context

def get_base_context() -> Dict[str, Any]:
    """
    Get the base context for all JSON-LD documents.
    
    Returns:
        Dict containing the base JSON-LD context
    """
    return get_context_mappings()

def get_property(mapping_key: str, extension_key: str = None) -> str:
    """
    Get the appropriate property URI for a field.
    
    Args:
        mapping_key: Key in ALL_MAPPINGS (e.g., "title", "author")
        extension_key: Optional specific extension key
        
    Returns:
        Property URI to use (e.g., "dc:title", "isiscb:authorRole")
    """
    if mapping_key not in ALL_MAPPINGS:
        return f"isiscb:{mapping_key}"
    
    mapping = ALL_MAPPINGS[mapping_key]
    
    if extension_key:
        # Look for the extension key in the extensions list
        for ext in mapping["extensions"]:
            if ext.lower().endswith(extension_key.lower()):
                return ext
        
        # If not found, create a custom one
        return f"isiscb:{extension_key}"
    
    # Return the primary property
    return mapping["primary"]

# Function to get relationship URI from type
def get_relationship_property(relationship_type):
    """Get property URI for a relationship type."""
    relationship_type = relationship_type.upper()
    
    if relationship_type in AUTHORITY_RELATIONSHIP_TYPES:
        return AUTHORITY_RELATIONSHIP_TYPES[relationship_type]["primary"]
    elif relationship_type in CITATION_RELATIONSHIP_TYPES:
        return CITATION_RELATIONSHIP_TYPES[relationship_type]["primary"]
    else:
        return f"isiscb:{relationship_type.lower()}"

def get_relationship_uri(relationship_type):
    """Get URI for a relationship type."""
    relationship_type = relationship_type.upper()
    
    if relationship_type in AUTHORITY_RELATIONSHIP_TYPES:
        return AUTHORITY_RELATIONSHIP_TYPES[relationship_type]["uri"]
    elif relationship_type in CITATION_RELATIONSHIP_TYPES:
        return CITATION_RELATIONSHIP_TYPES[relationship_type]["uri"]
    else:
        return f"isiscb:{relationship_type.lower()}"
    
# In schema_mappings.py - update the helper function
def get_normalized_relation_type(relationship_type: str) -> str:
    """
    Get the normalized form of a relationship type.
    
    Args:
        relationship_type: Original relationship type string
        
    Returns:
        Normalized relationship type (camelCase)
    """
    # First try direct mapping from the dictionary
    upper_type = relationship_type.upper().replace(' ', '')
    if upper_type in CITATION_RELATIONSHIP_TYPES:
        return CITATION_RELATIONSHIP_TYPES[upper_type].get("normalized", "")
    
    # If not found, normalize manually
    words = [word.strip() for word in relationship_type.split()]
    if not words:
        return "unknownRelation"
        
    # First word lowercase, rest capitalized - camelCase format
    camel_case = words[0].lower()
    for word in words[1:]:
        if word:
            camel_case += word[0].upper() + word[1:].lower()
            
    return camel_case    
