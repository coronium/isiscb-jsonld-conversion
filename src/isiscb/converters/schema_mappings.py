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

# All property mappings dictionary
ALL_MAPPINGS = {
    "title": TITLE_MAPPINGS,
    "author": AUTHOR_MAPPINGS,
    "date": DATE_MAPPINGS,
    "publisher": PUBLISHER_MAPPINGS,
    "subject": SUBJECT_MAPPINGS,
    "language": LANGUAGE_MAPPINGS,
    "identifier": IDENTIFIER_MAPPINGS
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
    
    # Add property equivalences for all mappings
    for mapping_key, mapping in ALL_MAPPINGS.items():
        primary = mapping["primary"]
        for equivalent in mapping["equivalents"]:
            context[equivalent] = {"@id": primary}
    
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