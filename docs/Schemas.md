# Best Practices for Handling Multiple Schema References in JSON-LD

When working with JSON-LD in the IsisCB conversion project, you'll often need to represent the same data using multiple vocabulary terms from different schemas. This document outlines best practices for handling these scenarios efficiently.


## Best Practice 1: Use JSON-LD Context for Property Equivalence

The preferred approach is to define property relationships in the `@context` section:

```json
{
  "@context": {
    "dc": "http://purl.org/dc/elements/1.1/",
    "schema": "http://schema.org/",
    "isiscb": "https://data.isiscb.org/context/",
    
    "schema:name": {"@id": "dc:title"},
    "isiscb:Title": {"@id": "dc:title"}
  },
  "dc:title": "The History of Science"
}
```

This tells JSON-LD processors that `schema:name` and `isiscb:Title` are equivalent to `dc:title`, so they all refer to the same value.

### Implementation in Python:

```python
class CitationConverterPipeline:
    def __init__(self):
        self.base_context = {
            # Standard vocabulary prefixes
            "dc": "http://purl.org/dc/elements/1.1/",
            "schema": "http://schema.org/",
            "isiscb": "https://data.isiscb.org/context/",
            
            # Property equivalences
            "schema:name": {"@id": "dc:title"},
            "isiscb:Title": {"@id": "dc:title"}
        }

class TitleConverter(BaseConverter):
    def _convert_impl(self, value: str, record_id: str) -> Dict:
        # Only store the value once under the primary property
        jsonld = {
            "dc:title": value.strip()
        }
        
        # Additional properties specific to this field
        if ': ' in value:
            main_title, subtitle = value.split(': ', 1)
            jsonld["isiscb:mainTitle"] = main_title.strip()
            jsonld["isiscb:subtitle"] = subtitle.strip()
        
        return jsonld
```

## Best Practice 2: Establish a Primary Vocabulary

For each data type, establish a primary vocabulary term:

| Data Type | Primary Term | Equivalent Terms |
|-----------|--------------|------------------|
| Title     | `dc:title`   | `schema:name`, `isiscb:Title` |
| Author    | `dc:creator` | `schema:author`, `isiscb:Author` |
| Date      | `dc:date`    | `schema:datePublished`, `isiscb:PublicationDate` |

Document these mappings in your project to ensure consistency.

## Best Practice 3: Define Vocabulary Extensions Properly

When you need custom properties that don't exist in standard vocabularies:

```json
{
  "@context": {
    "dc": "http://purl.org/dc/elements/1.1/",
    "isiscb": "https://data.isiscb.org/context/",
    
    "mainTitle": "isiscb:mainTitle",
    "subtitle": "isiscb:subtitle"
  },
  "dc:title": "The History of Science: A New Perspective",
  "mainTitle": "The History of Science",
  "subtitle": "A New Perspective"
}
```

## Best Practice 4: Use JSON-LD Frames for Consistent Output

Create JSON-LD frames to ensure consistent structure when processing your data:

```json
{
  "@context": {
    "dc": "http://purl.org/dc/elements/1.1/",
    "schema": "http://schema.org/",
    "isiscb": "https://data.isiscb.org/context/"
  },
  "@type": "bibo:Article",
  "dc:title": {},
  "dc:creator": {}
}
```

## Best Practice 5: Centralize Schema Mapping Logic

Create a dedicated module to define and manage all schema mappings:

```python
# src/isiscb/converters/schema_mappings.py

# Title property mappings
TITLE_MAPPINGS = {
    "primary": "dc:title",
    "equivalents": ["schema:name", "isiscb:Title"],
    "extensions": ["isiscb:mainTitle", "isiscb:subtitle"]
}

# Author property mappings
AUTHOR_MAPPINGS = {
    "primary": "dc:creator",
    "equivalents": ["schema:author", "isiscb:Author"],
    "extensions": ["isiscb:authorRole", "isiscb:authorOrder"]
}

def get_context_mappings():
    """Generate context mappings for JSON-LD."""
    context = {
        # Standard namespaces
        "dc": "http://purl.org/dc/elements/1.1/",
        "dcterms": "http://purl.org/dc/terms/",
        "schema": "http://schema.org/",
        "bibo": "http://purl.org/ontology/bibo/",
        "isiscb": "https://data.isiscb.org/context/"
    }
    
    # Add property equivalences
    for mapping in [TITLE_MAPPINGS, AUTHOR_MAPPINGS]:
        primary = mapping["primary"]
        for equivalent in mapping["equivalents"]:
            context[equivalent] = {"@id": primary}
    
    return context
```

Then use this in your pipeline:

```python
from src.isiscb.converters.schema_mappings import get_context_mappings

class CitationConverterPipeline:
    def __init__(self):
        self.base_context = get_context_mappings()
```

## Best Practice 6: Document Your Schema Usage

Create a schema documentation file that explains which vocabularies you're using and why:

```markdown
# IsisCB JSON-LD Schema Usage

## Core Vocabularies

- **Dublin Core** (`dc`, `dcterms`): Used for basic bibliographic metadata
- **Schema.org** (`schema`): Used for improved web discovery and indexing
- **Bibliographic Ontology** (`bibo`): Used for academic publication types
- **IsisCB** (`isiscb`): Custom extensions specific to history of science

## Property Mappings

| Data Element | Primary Property | Equivalent Properties | Extensions |
|--------------|------------------|------------------------|------------|
| Title        | dc:title         | schema:name, isiscb:Title | isiscb:mainTitle, isiscb:subtitle |
| Author       | dc:creator       | schema:author, isiscb:Author | isiscb:authorRole |
| Date         | dc:date          | schema:datePublished | isiscb:yearNormalized |
```
