# Related Citations Converter Documentation

## Overview

The `RelatedCitationsConverter` processes the "Related Citations" field from IsisCB citation records. This field contains information about relationships between different citation records, such as reviews, inclusions, references, and series relationships. The converter transforms this complex field format into structured JSON-LD with both preservation of all original data and mapping to standard bibliographic vocabularies.

## Input Data Format

The "Related Citations" field contains citation-to-citation relationships (CCR) with a complex multi-level delimited format:

```
CCR_ID CCR523979453 || CCRStatus Active || CCRType Is Reviewed By || CitationID CBB761549004 || CitationStatus Active || CitationType Book || CitationTitle Heavenly Numbers: Astronomy and Authority in Early Imperial China
```

Key characteristics:
- Multiple citation relationships are separated by a double slash (`//`)
- Each relationship consists of key-value pairs separated by double pipes (`||`)
- Each key-value pair has the format `Key Value` where the first space separates the key from value
- Whitespace can vary between entries and components

### Key Components

| Component | Description | Example |
|-----------|-------------|---------|
| CCR_ID | Unique identifier for the citation-citation relationship | CCR523979453 |
| CCRStatus | Status of the relationship (usually Active) | Active |
| CCRType | Type of relationship between citations | Is Reviewed By, Includes Series Article |
| CitationID | ID of the related citation record | CBB761549004 |
| CitationStatus | Status of the related citation | Active |
| CitationType | Type of the related citation | Book, Article |
| CitationTitle | Title of the related citation | Heavenly Numbers: Astronomy and Authority in Early Imperial China |

### Common Relationship Types

- "Is Reviewed By" - Indicates the citation is reviewed by another citation
- "Includes Series Article" - Indicates the citation includes a series article
- Other potential types include "References", "Is Referenced By", "Precedes", "Succeeds", etc.

## Conversion Process

The converter processes this field through several steps:

1. **Validation**: Checks for empty, NaN or non-string values
2. **Parsing**: Splits the field into individual entries, then into key-value pairs
3. **Normalization**: Converts relationship types into camelCase format (e.g., "Is Reviewed By" → "isReviewedBy")
4. **Structuring**: Creates relationship objects with appropriate properties
5. **Grouping**: Organizes relationships by type for specialized processing
6. **Format Mapping**: Maps relationship types to standard vocabulary terms where possible

## JSON-LD Output Structure

The converter produces two levels of representation:

### 1. Complete Relationship List

All relationships are preserved in their original form under `isiscb:relatedCitations`:

```json
"isiscb:relatedCitations": [
  {
    "@type": "isiscb:isReviewedBy",
    "isiscb:relationshipType": "Is Reviewed By",
    "isiscb:relationshipID": "CCR523979453",
    "isiscb:relationshipStatus": "Active",
    "isiscb:citation": {
      "@id": "https://data.isiscb.org/citation/CBB761549004"
    },
    "isiscb:citationTitle": "Heavenly Numbers: Astronomy and Authority in Early Imperial China",
    "isiscb:citationType": "Book",
    "isiscb:citationStatus": "Active"
  }
]
```

### 2. Standard Vocabulary Properties

Relationships are also represented using standard vocabulary properties based on their type:

```json
"isiscb:isReviewedBy": [
  {
    "@id": "https://data.isiscb.org/citation/CBB761549004",
    "dc:title": "Heavenly Numbers: Astronomy and Authority in Early Imperial China",
    "isiscb:citationType": "Book"
  }
]
```

## Relationship Type Mapping

The converter maps relationship types to standard vocabulary terms where possible:

| Original Relationship Type | Normalized Form | Mapped Property |
|---------------------------|-----------------|-----------------|
| Is Reviewed By | isReviewedBy | isiscb:isReviewedBy |
| Includes Series Article | includesSeriesArticle | isiscb:includesSeriesArticle |
| Is Part Of | isPartOf | dcterms:isPartOf |
| Has Part | hasPart | dcterms:hasPart |
| References | references | dcterms:references |
| Is Referenced By | isReferencedBy | dcterms:isReferencedBy |
| Succeeds | succeeds | dcterms:succeeds |
| Precedes | precedes | dcterms:precedes |

For relationship types not in this mapping, custom properties are created using the normalized form with the `isiscb:` prefix.

## Error Handling

The converter includes robust error handling for:

1. **Missing Data**: NaN, None, or empty values return an empty dictionary
2. **Non-String Values**: Types other than strings are logged and skipped
3. **Malformed Entries**: Entries missing key fields (CCRType, CitationID) are skipped
4. **Parsing Errors**: Exceptions during parsing are logged without failing the entire conversion

## Usage in Pipeline

The converter is registered in the `CitationConverterPipeline` and applied to the "Related Citations" field:

```python
# In pipeline initialization
self.converters = {
    # Other converters...
    'related_citations': RelatedCitationsConverter(),
}

# In convert_row method
if 'Related Citations' in row:
    jsonld.update(self.converters['related_citations'].convert(row['Related Citations'], record_id))
```

## Benefits

1. **Data Preservation**: All original relationship information is maintained
2. **Normalized Relationships**: Consistent relationship type representation
3. **Standard Compliance**: Maps to standard Dublin Core Terms where appropriate
4. **Flexibility**: Handles diverse relationship types through normalization
5. **Robustness**: Tolerates missing or malformed data

This converter ensures that the rich network of citation relationships in the IsisCB database is accurately represented in the JSON-LD format while facilitating interoperability with other bibliographic systems.