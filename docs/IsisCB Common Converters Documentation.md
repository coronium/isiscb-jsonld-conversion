# IsisCB Common Converters Documentation

## Overview

This document provides technical details and usage guidelines for the common converters used in the IsisCB JSON-LD conversion project. These converters handle fields that appear in both citation and authority records, transforming them from their raw CSV format to structured JSON-LD.

## BaseConverter

The `BaseConverter` class serves as the foundation for all converters, providing error handling and a common interface.

### Key Assumptions:
- All converters will follow the same interface pattern
- Record IDs are available for logging purposes
- Exceptions should be caught and handled gracefully

### Usage:
```python
from src.isiscb.converters.base import BaseConverter

class MyConverter(BaseConverter):
    def __init__(self, field_name: str = "My Field"):
        super().__init__(field_name)
    
    def _convert_impl(self, value: str, record_id: str) -> Dict:
        # Implement conversion logic here
        return {"property": value}
```

## RecordIdConverter

Converts the `Record ID` field to a proper JSON-LD identifier.

### Data Expectations:
- Citation IDs follow the pattern `CBB\d+` (e.g., `CBB001180697`)
- Authority IDs follow the pattern `CBA\d+` (e.g., `CBA000144339`)
- Entity type (`citation` or `authority`) must be provided during initialization

### Usage Example:
```python
record_id_converter = RecordIdConverter(entity_type='citation')
result = record_id_converter.convert("CBB001180697", "CBB001180697")
# Result: {"@id": "https://data.isiscb.org/citation/CBB001180697", "isiscb:recordID": "CBB001180697"}
```

## RecordTypeConverter

Converts the `Record Type` field to appropriate JSON-LD type declarations.

### Data Expectations:
- Record types are consistent with the values defined in `AUTHORITY_TYPE_MAPPING` and `CITATION_TYPE_MAPPING`
- Record ID pattern is used to determine whether it's a citation or authority

### Usage Example:
```python
type_converter = RecordTypeConverter()
result = type_converter.convert("Book", "CBB001180697")
# Result: {"@type": ["bibo:Book", "schema:Book", "isiscb:Book"]}
```

## RecordNatureConverter

Converts the `Record Nature` field to JSON-LD status properties.

### Data Expectations:
- Record nature values often follow the pattern "Status (RecordStatusExplanation ...)"
- Primary statuses include: Active, Inactive, Delete, Redirect

### Usage Example:
```python
nature_converter = RecordNatureConverter()
result = nature_converter.convert("Active (RecordStatusExplanation Active by default.)", "CBA000144339")
# Result: {"isiscb:recordStatus": "Active", "isiscb:recordNature": "Active (RecordStatusExplanation Active by default.)"}
```

## LinkedDataConverter

Converts the `Linked Data` field containing external identifiers to JSON-LD format.

### Data Expectations:
- Entries are separated by " // "
- Each entry follows the pattern: "Type X || URN Y"
- Common types include: DOI, URI, ISBN, VIAF, DNB
- Some entries may be malformed and require fallback parsing

### Usage Example:
```python
linked_data_converter = LinkedDataConverter()
result = linked_data_converter.convert("Type VIAF || URN http://viaf.org/viaf/18147423004844880849", "CBA000144339")
# Result includes structured data with schema:sameAs and isiscb:linkedData properties
```

## RelatedAuthoritiesConverter

Converts the `Related Authorities` field that links citations to authority records with typed relationships.

### Data Expectations:
- Data follows the structure: "ACR_ID X || ACRStatus Y || ACRType Z || ..."
- Multiple relationships are separated by " // "
- Key components include: ACR_ID, ACRStatus, ACRType, ACRDisplayOrder, ACRNameForDisplayInCitation, AuthorityID, AuthorityStatus, AuthorityType, AuthorityName
- Common relationship types: Author, Editor, Subject, Contributor, Publisher, etc.
- Display order is important for citation rendering

### Usage Example:
```python
related_authorities_converter = RelatedAuthoritiesConverter()
# Complex example with multiple relationships
result = related_authorities_converter.convert("ACR_ID ACR000606449 || ACRStatus Active || ACRType Author || ...", "CBB001180697")
# Result includes dc:creator, schema:author, and isiscb:relatedAuthorities properties
```

## RelatedCitationsConverter

Converts the `Related Citations` field that links citations to other citation records with typed relationships.

### Data Expectations:
- Data follows the structure: "CCR_ID X || CCRStatus Y || CCRType Z || ..."
- Multiple relationships are separated by " // "
- Key components include: CCR_ID, CCRStatus, CCRType, CitationID, CitationStatus, CitationType, CitationTitle
- Common relationship types: Is Reviewed By, Includes Series Article, References, etc.

### Usage Example:
```python
related_citations_converter = RelatedCitationsConverter()
# Complex example with citation relationships
result = related_citations_converter.convert("CCR_ID CCR523979453 || CCRStatus Active || CCRType Is Reviewed By || ...", "CBB001180697") 
# Result includes isiscb:relatedCitations and specific relationship properties
```

## AttributesConverter

Converts the `Attributes` field containing structured data about various properties of records.

### Data Expectations:
- Multiple attribute entries are separated by " // "
- Each entry follows the pattern: "AttributeID X || AttributeStatus Y || AttributeType Z || ..."
- Core components: AttributeID, AttributeStatus, AttributeType, AttributeValue, AttributeFreeFormValue, AttributeStart, AttributeEnd, AttributeDescription
- Common AttributeTypes:
  - BirthToDeathDates - For person birth/death years
  - Birth date - Specifically for birth dates
  - Death date - Specifically for death dates
  - FlourishedDate - When a person was active
  - JournalAbbr - Journal abbreviations
  - GeographicEntityType - Type of geographic entity
  - CountryCode - Country codes
- Values may be structured (e.g., [[1922], [2007]]) and need special parsing

### Usage Example:
```python
attributes_converter = AttributesConverter()
# Complex attribute example
result = attributes_converter.convert("AttributeID ATT000215394 || AttributeStatus Active || AttributeType BirthToDeathDates || AttributeValue [[1922], [2007]] || AttributeFreeFormValue 1922-2007 || AttributeStart 1922 || AttributeEnd 2007 || AttributeDescription", "CBA000144339")
# Result includes structured attributes and mapped schema.org properties
```

## General Data Assumptions and Expectations

For all common converters, the following assumptions and expectations apply:

1. **Data Format**:
   - Input data is from CSV exports of the IsisCB database
   - Field values may contain NaN, None, or empty strings that should be handled gracefully
   - String values should be normalized (trimmed, etc.) before processing

2. **Character Encoding**:
   - Data is encoded in UTF-8 format
   - Special characters, diacritics, and non-ASCII characters may be present

3. **Data Quality**:
   - Some fields may have inconsistent formatting or missing values
   - Converters should handle edge cases gracefully without failing
   - Errors should be logged but should not stop the conversion process

4. **Field Delimiters**:
   - Complex fields use consistent delimiters: 
     - " // " for separating multiple entries
     - " || " for separating key-value pairs within entries
     - Spaces in delimiters are significant

5. **IDs and References**:
   - Record IDs follow consistent patterns (CBB for citations, CBA for authorities)
   - References between records use these IDs

6. **Value Processing**:
   - Converters preserve original values while mapping to standard vocabularies
   - Normalization is performed where needed (e.g., dates, types)
   - Structured data is parsed into appropriate JSON-LD structures

7. **Field Inheritance**:
   - Some fields may inherit values from related records (e.g., titles from cited works)
   - The conversion process does not resolve these inheritances automatically

8. **Context and Vocabulary**:
   - JSON-LD context definitions are managed centrally and applied during final output
   - Standard vocabularies (Dublin Core, Schema.org, etc.) are used where applicable
   - IsisCB-specific terms use the "isiscb:" namespace

By adhering to these assumptions and expectations, the common converters provide a robust foundation for transforming IsisCB data into well-structured JSON-LD.