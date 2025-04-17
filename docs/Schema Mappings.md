# Schema Mappings for IsisCB JSON-LD Conversion

## Overview

This document describes the centralized schema mapping approach implemented in the IsisCB JSON-LD conversion project. The goal is to ensure consistent vocabulary usage across all converters and to make the codebase more maintainable.

## Centralized Schema Mappings Module

The core of our approach is the `schema_mappings.py` module which defines:

1. **Standard namespaces**: URI prefixes for all vocabularies used in the project
2. **Property mappings**: Canonical mappings between fields and their JSON-LD representations
3. **Type mappings**: Mappings between IsisCB record types and standard vocabularies
4. **Helper functions**: Utilities to generate context objects and retrieve properties

## Key Components

### Namespace Definitions

```python
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
```

### Property Mappings

Each field has a mapping definition that includes:

- **primary**: The canonical property URI to use
- **equivalents**: Alternative properties that mean the same thing
- **extensions**: IsisCB-specific extensions for specialized metadata

Example:
```python
TITLE_MAPPINGS = {
    "primary": "dc:title",
    "equivalents": ["schema:name", "isiscb:title"],
    "extensions": ["isiscb:mainTitle", "isiscb:subtitle"]
}
```

### Type Mappings

Mappings between IsisCB record types and standard vocabulary types:

```python
CITATION_TYPE_MAPPING = {
    "Book": ["bibo:Book", "schema:Book"],
    "Article": ["bibo:Article", "schema:ScholarlyArticle"],
    ...
}

AUTHORITY_TYPE_MAPPING = {
    "Person": ["schema:Person", "foaf:Person"],
    "Institution": ["schema:Organization", "foaf:Organization"],
    ...
}
```
## Mappings

### Authority Types

In `src/isiscb/converters/schema_mappings.py`

Look at the `Category Division` and `Cross-reference` and determine if those are appropriate mappings. 

```
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
```
### Citation Type

In `src/isiscb/converters/schema_mappings.py`

Look at `Essay` and  `Conference Paper` and see if appropriate mapping is used. 

```
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
```

### Record Status

In `src/isiscb/converters/schema_mappings.py`

Used to convert the CB `Record Nature` field.

```
RECORD_STATUS_MAPPING = {
    "Active": "Active",
    "Inactive": "Inactive",
    "Delete": "Delete",
    "Redirect": "Redirect"
}
```

### Relationship Types (from CCR records)

In `src/isiscb/converters/common/related_citations.py`

Find standardized  vocabulary of `isReviewedBy` and `reviews`.

```
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
```

## Usage in the Codebase

### Defining the JSON-LD Context

```python
from ..converters.schema_mappings import get_base_context

class CitationConverterPipeline:
    def __init__(self):
        # Use the centralized context mapping
        self.base_context = get_base_context()
```

### Using Properties in Converters

```python
from ..schema_mappings import get_property

class TitleConverter(BaseConverter):
    def _convert_impl(self, value: str, record_id: str) -> Dict:
        # Use the primary property from the centralized mappings
        primary_property = get_property("title")
        jsonld = {
            primary_property: title
        }
```

### Using Type Mappings in Converters

```python
from ..schema_mappings import AUTHORITY_TYPE_MAPPING, CITATION_TYPE_MAPPING

class RecordTypeConverter(BaseConverter):
    def _convert_impl(self, value: str, record_id: str) -> Dict:
        # Determine if this is an authority or citation based on record ID pattern
        if record_id.startswith("CBA"):
            type_mapping = AUTHORITY_TYPE_MAPPING
        else:
            type_mapping = CITATION_TYPE_MAPPING
```

## Benefits

1. **Consistency**: All converters use the same property URIs for the same concepts
2. **Maintainability**: Changes to vocabulary mappings can be made in a single place
3. **Documentation**: The mapping definitions serve as documentation of schema usage
4. **Flexibility**: Easy to add new mappings or modify existing ones in a centralized way
5. **JSON-LD Context**: Automatically generates property equivalence statements in the context

## Future Improvements

1. **Schema validation**: Add validation against the defined schema
2. **External vocabulary references**: Import standard vocabulary definitions
3. **Schema versioning**: Add support for versioning the schema mappings
4. **Documentation generation**: Auto-generate documentation from the mappings