# IsisCB JSON-LD Conversion: Schema Mapping Documentation

This document provides detailed information about how fields from the IsisCB database are mapped to standard JSON-LD vocabularies and schemas. For each converter, we outline the specific mappings between source data fields and standard vocabulary terms.

## Core Vocabularies Used

The conversion system uses several standard vocabularies:

- **Dublin Core (dc:, dcterms:)** - Core bibliographic metadata
  - Namespace: http://purl.org/dc/elements/1.1/ and http://purl.org/dc/terms/

- **Schema.org (schema:)** - General-purpose structured data vocabulary
  - Namespace: http://schema.org/

- **Bibliographic Ontology (bibo:)** - Specialized academic publication terms
  - Namespace: http://purl.org/ontology/bibo/

- **SKOS (skos:)** - Simple Knowledge Organization System
  - Namespace: http://www.w3.org/2004/02/skos/core#

- **FOAF (foaf:)** - Friend of a Friend vocabulary for people and organizations
  - Namespace: http://xmlns.com/foaf/0.1/

- **IsisCB Custom (isiscb:)** - Custom namespace for IsisCB-specific terms
  - Namespace: https://ontology.isiscb.org/vocabulary/

## Common Converters

### RecordIdConverter

| Source Field | JSON-LD Property | Comments |
|--------------|------------------|----------|
| Record ID    | @id              | URI constructed as `https://data.isiscb.org/{entity_type}/{value}` |
| Record ID    | isiscb:recordID  | Preserves original ID value |

### RecordTypeConverter

| Source Field | JSON-LD Property | Mapping Pattern |
|--------------|------------------|----------------|
| Record Type  | @type            | Multiple types from different vocabularies |

**Mapping Examples:**
- Book → [bibo:Book, schema:Book, isiscb:Book]
- Article → [bibo:Article, schema:ScholarlyArticle, isiscb:Article]
- Person → [schema:Person, foaf:Person, isiscb:Person]
- Institution → [schema:Organization, foaf:Organization, isiscb:Institution]

### RecordNatureConverter

| Source Field | JSON-LD Property | Mapping |
|--------------|------------------|---------|
| Record Nature | isiscb:recordStatus | Extracts primary status (Active, Inactive, Delete, Redirect) |
| Record Nature | isiscb:recordNature | Preserves full value including explanation |

### LinkedDataConverter

| Source Field | JSON-LD Property | Source Format | Comments |
|--------------|------------------|--------------|----------|
| Linked Data  | isiscb:linkedData | "Type X \|\| URN Y" | Structured array of typed links |
| Linked Data (DOI) | schema:identifier | "Type DOI \|\| URN value" | Structured PropertyValue |
| Linked Data (ISBN) | schema:identifier | "Type ISBN \|\| URN value" | Structured PropertyValue |
| Linked Data (URI) | schema:sameAs | "Type URI \|\| URN value" | Direct URI reference |

### RelatedAuthoritiesConverter

| Source Relationship Type | JSON-LD Property | Schema Used |
|--------------------------|------------------|-------------|
| Author | dc:creator + schema:author | Dublin Core + Schema.org |
| Editor | schema:editor | Schema.org |
| Advisor | vivo:advisorIn | VIVO Ontology |
| Subject | dc:subject + schema:about | Dublin Core + Schema.org |
| Publisher | dc:publisher + schema:publisher | Dublin Core + Schema.org |
| Periodical | schema:isPartOf + dcterms:isPartOf | Schema.org + Dublin Core Terms |
| Category | dc:subject + isiscb:category | Dublin Core + IsisCB |
| School | bibo:degreeGrantor | Bibliographic Ontology |
| Institution | isiscb:institution + schema:affiliation | IsisCB + Schema.org |
| All relationships | isiscb:relatedAuthorities | Full structured representation |

### RelatedCitationsConverter

| Source Relationship Type | JSON-LD Property | Schema Used |
|--------------------------|------------------|-------------|
| Is Reviewed By | isiscb:isReviewedBy | IsisCB |
| Reviews | isiscb:reviews | IsisCB |
| Is Part Of | dcterms:isPartOf | Dublin Core Terms |
| Has Part | dcterms:hasPart | Dublin Core Terms |
| References | dcterms:references | Dublin Core Terms |
| Is Referenced By | dcterms:isReferencedBy | Dublin Core Terms |
| All relationships | isiscb:relatedCitations | Full structured representation |

### AttributesConverter

| Source Attribute Type | JSON-LD Property | Schema Used |
|-----------------------|------------------|-------------|
| BirthToDeathDates | schema:birthDate + schema:deathDate | Schema.org |
| Birth date | schema:birthDate | Schema.org |
| Death date | schema:deathDate | Schema.org |
| FlourishedDate | isiscb:flourishedDate | IsisCB |
| JournalAbbr | bibo:shortTitle | Bibliographic Ontology |
| GeographicEntityType | isiscb:geographicEntityType + @type | IsisCB + Schema.org |
| CountryCode | schema:addressCountry | Schema.org |
| All attributes | isiscb:attributes | Full structured representation |

## Citation-Specific Converters

### TitleConverter

| Source Field | JSON-LD Property | Schema Used |
|--------------|------------------|-------------|
| Title | dc:title | Dublin Core |
| Title (with subtitle) | dc:title + isiscb:mainTitle + isiscb:subtitle | Dublin Core + IsisCB |

### PublicationDetailsConverter

| Source Field | JSON-LD Property | Schema Used |
|--------------|------------------|-------------|
| Year of publication | dc:date + schema:datePublished | Dublin Core + Schema.org |
| Year of publication (normalized) | isiscb:yearNormalized | IsisCB |
| Place Publisher | dc:publisher + isiscb:publisherLocation | Dublin Core + IsisCB |
| Edition Details | bibo:edition | Bibliographic Ontology |
| Physical Details | isiscb:physicalDetails | IsisCB |
| Extent | isiscb:extent | IsisCB |
| Extent (pages) | schema:numberOfPages | Schema.org |
| Language | dc:language | Dublin Core |
| ISBN | bibo:isbn | Bibliographic Ontology |
| ISBN | schema:identifier (PropertyValue) | Schema.org |

### JournalMetadataConverter

| Source Field | JSON-LD Property | Schema Used |
|--------------|------------------|-------------|
| Journal Link | schema:isPartOf | Schema.org |
| Journal Volume | bibo:volume | Bibliographic Ontology |
| Journal Issue | bibo:issue | Bibliographic Ontology |
| Pages Free Text | bibo:pages | Bibliographic Ontology |
| Pages (start/end) | bibo:pageStart + bibo:pageEnd | Bibliographic Ontology |

### LanguageConverter

| Source Field | JSON-LD Property | Schema Used |
|--------------|------------------|-------------|
| Language | dc:language | Dublin Core |
| Language (with ISO code) | dc:language (@value + @language) | Dublin Core + JSON-LD language tags |

### AbstractConverter

| Source Field | JSON-LD Property | Schema Used |
|--------------|------------------|-------------|
| Abstract | dc:abstract | Dublin Core |
| Abstract | schema:abstract | Schema.org |

### MetadataConverter

| Source Field | JSON-LD Property | Schema Used |
|--------------|------------------|-------------|
| Fully Entered | isiscb:fullyEntered | IsisCB |
| Proofed | isiscb:proofed | IsisCB |
| SPW checked | isiscb:spwChecked | IsisCB |
| Published Print | isiscb:publishedPrint | IsisCB |
| Published RLG | isiscb:publishedRLG | IsisCB |
| Stub Record Status | isiscb:stubRecordStatus | IsisCB |
| Created Date | dc:created | Dublin Core |
| Modified Date | dc:modified | Dublin Core |
| Creator | dc:creator (structured object) | Dublin Core |
| Modifier | isiscb:modifier (structured object) | IsisCB |
| Record History | isiscb:recordHistory | IsisCB |
| Staff Notes | isiscb:staffNotes | IsisCB |
| Staff Notes (metadata) | isiscb:staffNotesMetadata | IsisCB |
| Complete Citation | isiscb:completeCitation | IsisCB |
| Dataset | isiscb:dataset | IsisCB |
| Link to Record | isiscb:linkToRecord | IsisCB |

## Example Conversion

Let's illustrate a complete conversion with an example citation record:

**Original CSV Data:**
```
Record ID: CBB001180697
Record Type: Book
Record Nature: Active (RecordStatusExplanation Active by default.)
Title: The History of Mathematics: An Introduction
Author: Boyer, Carl B.
Year of publication: 1991
Place Publisher: New York: Wiley
Edition Details: 2nd ed.
Physical Details: xvi, 715 p. : ill.
Language: English
ISBN: 978-0471543978
```

**Converted JSON-LD:**
```json
{
  "@context": {
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "schema": "http://schema.org/",
    "bibo": "http://purl.org/ontology/bibo/",
    "isiscb": "https://ontology.isiscb.org/vocabulary/"
  },
  "@id": "https://data.isiscb.org/citation/CBB001180697",
  "@type": ["bibo:Book", "schema:Book", "isiscb:Book"],
  "dc:title": "The History of Mathematics: An Introduction",
  "isiscb:mainTitle": "The History of Mathematics",
  "isiscb:subtitle": "An Introduction",
  "dc:creator": "Boyer, Carl B.",
  "schema:author": "Boyer, Carl B.",
  "dc:date": "1991",
  "schema:datePublished": "1991",
  "isiscb:yearNormalized": 1991,
  "dc:publisher": "Wiley",
  "isiscb:publisherLocation": "New York",
  "bibo:edition": "2nd ed.",
  "isiscb:physicalDetails": "xvi, 715 p. : ill.",
  "isiscb:extent": "715 p.",
  "schema:numberOfPages": 715,
  "dc:language": "English",
  "bibo:isbn": "978-0471543978",
  "schema:identifier": {
    "@type": "PropertyValue",
    "propertyID": "ISBN",
    "value": "978-0471543978"
  },
  "isiscb:recordID": "CBB001180697",
  "isiscb:recordStatus": "Active",
  "isiscb:recordNature": "Active (RecordStatusExplanation Active by default.)"
}
```

This structured mapping system ensures that IsisCB data is converted to JSON-LD in a way that preserves the original information while making it compatible with standard semantic web vocabularies. The hybrid approach uses established vocabularies wherever possible while using the IsisCB namespace for domain-specific properties that don't have standard equivalents.