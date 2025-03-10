# Linked Data Field Converter Documentation

## Overview

The LinkedDataConverter module processes external reference links from IsisCB records, converting them from the raw pipe-delimited format to structured JSON-LD. This enables both preservation of the original data and interoperability with standard semantic web practices.

## Input Data Format

The Linked Data field in IsisCB data follows this pattern:

```
Type {TYPE} || URN {VALUE} // Type {TYPE} || URN {VALUE} // ...
```

Where:
- `{TYPE}` represents the identifier type (e.g., DOI, URI, ISBN, VIAF)
- `{VALUE}` contains the actual identifier value
- Multiple entries are separated by ` // ` (space, double forward slash, space)

### Common Types Found in Data:

1. **DOI** (Digital Object Identifier)
   - Example: `Type DOI || URN 10.1086/710720`

2. **URI** (Uniform Resource Identifier)
   - Example: `Type URI || URN https://www.journals.uchicago.edu/doi/10.1086/710720`

3. **ISBN** (International Standard Book Number)
   - Example: `Type ISBN || URN 9783030507602`

4. **VIAF** (Virtual International Authority File)
   - Example: `Type VIAF || URN http://viaf.org/viaf/18147423004844880849`

5. **DNB** (Deutsche Nationalbibliothek)
   - Example: `Type DNB || URN http://d-nb.info/gnd/133578771/about/html`

### Additional Format Considerations:

- Some entries may have multiple representations of the same identifier (e.g., both a DOI and a URI resolving to that DOI)
- Entries do not include internal IDs (like the LinkedData_ID fields mentioned in the documentation)
- Field values may occasionally have formatting inconsistencies

## Conversion Process

The LinkedDataConverter implements the following processing steps:

1. **Splitting**: Divides the raw string into individual entries using ` // ` as the separator
2. **Parsing**: Extracts the type and URN from each entry using a regex pattern
3. **Grouping**: Groups entries by their type
4. **Transformation**: Generates appropriate JSON-LD representation
5. **Fallback Parsing**: Attempts alternative parsing for entries that don't match the expected pattern

### Regular Expression Pattern

```python
re.compile(r"Type\s+([^\s|]+)\s+\|\|\s+URN\s+(.*?)(?:\s*$)")
```

This pattern is designed to extract:
- First capture group: The identifier type (after "Type " and before the pipes)
- Second capture group: The identifier value (after "URN " until the end of the string)

## JSON-LD Output

The converter generates a structured JSON-LD output with two primary components:

### 1. IsisCB-Specific Representation

All linked data entries are preserved in their original structure using an IsisCB-specific property:

```json
"isiscb:linkedData": [
  {
    "type": "DOI",
    "values": ["10.1086/710720", "10.1007/s11024-020-09424-3"]
  },
  {
    "type": "URI",
    "values": ["https://www.journals.uchicago.edu/doi/10.1086/710720"]
  }
]
```

This representation:
- Groups identifiers by type
- Preserves all original values
- Maintains the IsisCB-specific context

### 2. Schema.org Standard Representation

In addition to the IsisCB-specific format, the converter generates standard Schema.org properties for improved interoperability:

#### For DOI and ISBN identifiers:

```json
"schema:identifier": [
  {
    "@type": "PropertyValue",
    "propertyID": "DOI",
    "value": "10.1086/710720"
  },
  {
    "@type": "PropertyValue",
    "propertyID": "ISBN",
    "value": "9783030507602"
  }
]
```

This follows the Schema.org pattern for structured identifiers with explicit typing.

#### For URI identifiers:

```json
"schema:sameAs": [
  "https://www.journals.uchicago.edu/doi/10.1086/710720",
  "https://doi.org/10.1007/s11024-020-09424-3"
]
```

URIs are represented using `schema:sameAs` to indicate they refer to the same entity, following linked data best practices.

## Error Handling

The converter implements robust error handling for various scenarios:

1. **Empty/Null Values**: Returns an empty dictionary
2. **Malformed Entries**: Attempts alternative parsing methods
3. **Missing URNs**: Logs a warning and skips the entry
4. **Parsing Exceptions**: Logs errors with record ID and entry details

## Usage in Pipeline

The LinkedDataConverter is registered in the CitationConverterPipeline and applied to each citation record containing a "Linked Data" field:

```python
# Apply linked data converter
if 'Linked Data' in row:
    jsonld.update(self.converters['linked_data'].convert(row['Linked Data'], record_id))
```

## Edge Cases and Considerations

1. **Varying URL Formats**: The converter handles different URL patterns (with or without https://)
2. **Inconsistent Separators**: Falls back to alternative parsing methods for unusual formats
3. **Duplicate Identifiers**: Groups duplicates under the same type
4. **Mixed Case Types**: Type values are preserved in their original case
5. **Multiple Representation**: The same identifier may appear in multiple forms (e.g., both DOI and URI)

## Integration with JSON-LD Context

For proper interpretation, the JSON-LD context should include:

```json
{
  "@context": {
    "isiscb": "https://ontology.isiscb.org/vocabulary/",
    "schema": "http://schema.org/"
  }
}
```

This ensures that both the IsisCB-specific properties and standard Schema.org properties are correctly interpreted.