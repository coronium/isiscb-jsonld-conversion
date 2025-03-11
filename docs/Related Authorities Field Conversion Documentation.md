# Related Authorities Field Conversion Documentation

## Overview

The Related Authorities field is a crucial component of the IsisCB database, containing structured relationship information between citation records and authority records. This document explains the format of the field data and how it is processed into JSON-LD format.

## Field Format

The Related Authorities field uses a complex multi-level delimited format that follows this pattern:

```
ACR_ID ACR000606449 || ACRStatus Active || ACRType Author || ACRDisplayOrder 1.0 || ACRNameForDisplayInCitation Joseph W. Dauben || AuthorityID CBA000023541 || AuthorityStatus Active || AuthorityType Person || AuthorityName Dauben, Joseph Warren // ACR_ID ACR150016056 || ACRStatus Active || ACRType Periodical || ACRDisplayOrder 1.0 || ACRNameForDisplayInCitation British Journal for the History of Mathematics || AuthorityID CBA725764209 || AuthorityStatus Active || AuthorityType Serial Publication || AuthorityName British Journal for the History of Mathematics
```

Key characteristics:
- Multiple authority relationships are separated by a double slash (`//`)
- Each relationship consists of key-value pairs separated by double pipes (`||`)
- Each key-value pair has the format `Key Value` where the first space separates the key from the value

## Key Components

Each relationship entry contains several important components:

| Component | Description | Example |
|-----------|-------------|---------|
| ACR_ID | Unique identifier for the authority-citation relationship | ACR000606449 |
| ACRStatus | Status of the relationship (usually Active) | Active |
| ACRType | Type of relationship (Author, Subject, etc.) | Author |
| ACRDisplayOrder | Order for display (important for authors) | 1.0 |
| ACRNameForDisplayInCitation | Name to display in citations | Joseph W. Dauben |
| AuthorityID | ID of the authority record | CBA000023541 |
| AuthorityStatus | Status of the authority record | Active |
| AuthorityType | Type of the authority (Person, Concept, etc.) | Person |
| AuthorityName | Name of the authority record | Dauben, Joseph Warren |

## Relationship Types

The field supports numerous relationship types, including:

### People Relationships
- Author: Primary creators of the work
- Editor: Editors of the work
- Advisor: Thesis advisors
- Contributor: General contributors
- Translator: Translators of the work
- Committee Member: Members of committees
- Interviewer: Interviewers in an interview
- Guest: Guests in an interview or event
- Writer: Writers (similar to authors)
- Director: Directors of films or performances
- Producer: Producers of media
- Performer: Performers or actors

### Subject Relationships
- Subject: Topics of the work
- Category: Classification categories

### Publication Relationships
- Periodical: Journal where the article was published
- Publisher: Publishing organization
- Book Series: Series containing the work
- Distributor: Organization distributing the work

### Institutional Relationships
- School: Educational institution for theses
- Institution: Associated institutions
- Meeting: Meeting or conference where presented
- Archival Repository: Repository holding archives
- Maintaining Institution: Institution maintaining the resource

## Conversion Process

The `RelatedAuthoritiesConverter` handles this complex field by:

1. **Parsing**: Splitting the field into individual entries and then into key-value pairs
2. **Structuring**: Creating relationship objects with appropriate properties
3. **Typing**: Mapping relationship types to standard vocabulary terms
4. **Grouping**: Organizing relationships by type for specialized processing
5. **Formatting**: Generating JSON-LD output with both specialized and standard properties

## JSON-LD Output Structure

The converter produces two levels of representation:

### 1. Complete Relationship List

All relationships are preserved in their original form under `isiscb:relatedAuthorities`:

```json
"isiscb:relatedAuthorities": [
  {
    "@type": "isiscb:author",
    "isiscb:relationshipType": "Author",
    "isiscb:displayOrder": "1.0",
    "isiscb:authority": {
      "@id": "https://data.isiscb.org/authority/CBA000023541"
    },
    "isiscb:authorityName": "Dauben, Joseph Warren",
    "isiscb:authorityType": "Person",
    "isiscb:displayName": "Joseph W. Dauben",
    "isiscb:authorityStatus": "Active"
  },
  // Additional relationships...
]
```

### 2. Standard Vocabulary Properties

Relationships are also represented using standard vocabulary properties based on their type:

```json
"dc:creator": [
  {
    "@id": "https://data.isiscb.org/authority/CBA000023541",
    "name": "Joseph W. Dauben",
    "isiscb:role": "author",
    "isiscb:position": "1.0",
    "isiscb:authorityType": "Person"
  }
],
"schema:isPartOf": {
  "@id": "https://data.isiscb.org/authority/CBA725764209",
  "name": "British Journal for the History of Mathematics",
  "isiscb:type": "Serial Publication"
}
```
## IsisCB Relationship Type Mapping to Standard Vocabularies

This table provides a comprehensive reference of how IsisCB relationship types map to standard vocabulary terms in the JSON-LD conversion.

| IsisCB Relationship Type | Primary Property | Equivalent Properties | IsisCB URI |
|--------------------------|------------------|------------------------|------------|
| **Creator and Contributor Relationships** |
| Author | dc:creator | schema:author | isiscb:author |
| Editor | schema:editor | dc:contributor | isiscb:editor |
| Advisor | schema:advisor | dc:contributor | isiscb:advisor |
| Contributor | dc:contributor | | isiscb:contributor |
| Translator | schema:translator | dc:contributor | isiscb:translator |
| Committee Member | isiscb:committeeMember | dc:contributor | isiscb:committeeMember |
| Interviewer | isiscb:interviewer | dc:contributor | isiscb:interviewer |
| Guest | isiscb:guest | dc:contributor | isiscb:guest |
| Creator | dc:creator | schema:creator | isiscb:creator |
| Writer | schema:author | dc:creator | isiscb:writer |
| Director | schema:director | dc:contributor | isiscb:director |
| Producer | schema:producer | dc:contributor | isiscb:producer |
| Organizer | isiscb:organizer | dc:contributor | isiscb:organizer |
| Host | isiscb:host | dc:contributor | isiscb:host |
| Performer | schema:performer | dc:contributor | isiscb:performer |
| Researcher | isiscb:researcher | dc:contributor | isiscb:researcher |
| Developer | isiscb:developer | dc:contributor | isiscb:developer |
| Compiler | isiscb:compiler | dc:contributor | isiscb:compiler |
| Collector | isiscb:collector | dc:contributor | isiscb:collector |
| Archivist | isiscb:archivist | dc:contributor | isiscb:archivist |
| **Subject Relationships** |
| Subject | dc:subject | schema:about | isiscb:subject |
| Category | isiscb:category | dc:type | isiscb:category |
| **Publication Relationships** |
| Periodical | schema:isPartOf | dc:isPartOf | isiscb:periodical |
| Publisher | dc:publisher | schema:publisher | isiscb:publisher |
| Book Series | schema:isPartOf | dc:isPartOf | isiscb:bookSeries |
| Distributor | schema:distributor | | isiscb:distributor |
| **Institutional Relationships** |
| School | schema:school | | isiscb:school |
| Institution | isiscb:institution | schema:affiliation | isiscb:institution |
| Meeting | bibo:presentedAt | | isiscb:meeting |
| Archival Repository | isiscb:archivalRepository | | isiscb:archivalRepository |
| Maintaining Institution | isiscb:maintainingInstitution | | isiscb:maintainingInstitution |
| Presenting Group | isiscb:presentingGroup | dc:contributor | isiscb:presentingGroup |
| **Award Relationships** |
| Awardee | isiscb:awardee | | isiscb:awardee |
| Officer | isiscb:officer | dc:contributor | isiscb:officer |

### Notes on Vocabulary Usage

1. **Dublin Core (dc:)** is used extensively for core bibliographic relationships
   - `dc:creator` for primary creators (authors, writers)
   - `dc:contributor` as a catch-all for secondary contributors
   - `dc:subject` for topical subjects
   - `dc:publisher` for publishing organizations

2. **Schema.org (schema:)** provides web-friendly, widely recognized properties
   - `schema:author` as equivalent to `dc:creator`
   - `schema:isPartOf` for containing publications
   - `schema:editor`, `schema:translator`, etc. for specific roles

3. **Bibliographic Ontology (bibo:)** offers specialized academic publishing properties
   - `bibo:presentedAt` for meetings and conferences

4. **IsisCB (isiscb:)** custom namespace used for specialized terms not covered by standard vocabularies
   - Used for all unique IsisCB relationship types
   - Preserves the rich scholarly context specific to history of science

This mapping system ensures that IsisCB data is both broadly interoperable through standard terms and also preserves the specialized relationships needed for history of science scholarship.


## Processing Rules

The converter applies several rules during processing:

1. **Ordering**: Authors and contributors are sorted by their display order value
2. **Name Priority**: Display names are preferred over authority names when available
3. **Type Mapping**: Relationship types are mapped to standard vocabulary terms when possible
4. **Grouping**: Related types are grouped together (e.g., all contributor types under `dc:contributor`)
5. **Cardinality**: Properties that typically have one value (like publisher) use a single object, while others use arrays

## Handling Special Cases

The converter includes specialized processing for different relationship categories:

1. **Person Relationships** (`_process_persons`): Handles individuals with roles, ordering, and proper attribution
2. **Subject Relationships** (`_process_subjects`): Processes subjects and categories with type information
3. **Publishing Information** (`_process_periodical`, `_process_publisher`, etc.): Manages publication-related relationships
4. **Institutional Relationships** (`_process_institution`, `_process_event`): Handles organizations and events

## Error Handling

The converter includes robust error handling to deal with malformed entries:

1. **Missing Fields**: Entries missing critical fields (ACRType, AuthorityID) are skipped
2. **Malformed Entries**: Parsing errors are logged without failing the entire conversion
3. **Empty Values**: Empty display names or other fields are handled gracefully by falling back to alternatives

## Schema Mapping Integration

The converter uses the centralized schema mappings to ensure consistent vocabulary usage:

1. `get_relationship_property()`: Returns the appropriate standard property URI for a relationship type
2. `get_relationship_uri()`: Returns the URI to use for a relationship's @type value

This ensures that all relationship types are consistently represented in the JSON-LD output, following the project's overall vocabulary strategy.