# IsisCB JSON-LD Schema Design Documentation

## Overview

This document explains the schema design for the IsisCB JSON-LD conversion project. The project aims to transform the IsisCB bibliographic and authority data into JSON-LD format while preserving its specialized focus on the history of science, technology, and medicine.

The schema follows a hybrid approach that leverages standard bibliographic vocabularies (Dublin Core, Schema.org, SKOS, BIBO, etc.) while maintaining domain-specific attributes through custom vocabulary extensions.

## Core Entity Types

### BaseEntity

All entities in the system inherit from a common base with these properties:

- **@id**: URI identifier (format: `https://data.isiscb.org/{entity_type}/{id}`)
- **@type**: Entity type declarations (multiple types from different vocabularies)
- **isiscb:recordID**: Original database identifier (CBA/CBB prefix)
- **isiscb:recordType**: Type of record in the original system
- **isiscb:recordStatus**: Status (Active, Inactive, Delete, Redirect)
- **isiscb:recordNature**: Original record nature value
- **dc:created**: Creation timestamp
- **dc:modified**: Modification timestamp
- **dc:creator**: Record creator with username
- **isiscb:modifier**: Record modifier with username
- **isiscb:staffNotes**: Notes for staff use
- **isiscb:recordHistory**: Change history

### Citation Entities

Citations represent bibliographic records for books, articles, theses, etc.

- **dc:title**: Title of the work
- **isiscb:mainTitle/subtitle**: Title components
- **dc:creator**: Author(s) of the work
- **dc:contributor**: Other contributors
- **schema:editor**: Editor(s)
- **dc:date**: Publication date
- **schema:datePublished**: Normalized publication date
- **dc:publisher**: Publisher information
- **isiscb:publisherLocation**: Location of publication
- **dc:language**: Language(s) of the work
- **dc:abstract**: Abstract or summary
- **dc:subject**: Subject(s) and categories
- **bibo:edition**: Edition information
- **bibo:pages**: Page information
- **isiscb:extent**: Extent of the work
- **isiscb:physicalDetails**: Physical description
- **bibo:isbn**: ISBN/identifiers
- **schema:isPartOf**: Parent work (journal, series)
- **bibo:volume/issue**: Journal issue information
- **isiscb:completeCitation**: Formatted citation

### Authority Entities

Authorities represent controlled vocabulary terms, including people, institutions, concepts, etc.

- **schema:name**: Name of the authority
- **skos:prefLabel**: Preferred display label
- **skos:altLabel**: Alternative labels
- **schema:description**: Description text
- **isiscb:classificationSystem**: Classification system used
- **isiscb:classificationCode**: Classification code

#### Person

- **schema:familyName**: Last name
- **schema:givenName**: First name
- **schema:nameSuffix**: Name suffix
- **isiscb:namePreferred**: Preferred form of name
- **schema:birthDate**: Birth year
- **schema:deathDate**: Death year
- **isiscb:flourishedDate**: Active period

#### Institution

- **schema:location**: Location information
- **schema:foundingDate**: Founding date
- **schema:dissolutionDate**: Dissolution date

#### Concept

- **skos:broader**: Broader concepts
- **skos:narrower**: Narrower concepts
- **skos:related**: Related concepts
- **skos:inScheme**: Classification scheme
- **skos:notation**: Classification notation

#### Geographic Term

- **schema:placeName**: Place name
- **schema:addressCountry**: Country code
- **isiscb:geographicEntityType**: Type of place

#### Time Period

- **dcterms:temporal**: Temporal description
- **schema:startDate**: Start date
- **schema:endDate**: End date

#### Serial Publication

- **bibo:shortTitle**: Abbreviated title
- **schema:issn**: ISSN identifier
- **schema:publisher**: Publisher information

## Relationship Structures

### Related Authorities

Links between citations and authorities or between authorities:

- **isiscb:relationshipType**: Type of relationship
- **isiscb:authority**: Referenced authority
- **isiscb:displayOrder**: Order for display
- **isiscb:authorityName**: Name of authority
- **isiscb:authorityType**: Type of authority
- **isiscb:displayName**: Display name

Relationship types include:
- Author, Editor, Translator
- Subject, Category
- Publisher, School, Institution
- Periodical, Book Series
- And many others specific to scholarly contexts

### Related Citations

Links between citation records:

- **isiscb:relationshipType**: Type of relationship
- **isiscb:citation**: Referenced citation
- **isiscb:relationshipID**: ID of relationship
- **isiscb:citationTitle**: Title of referenced citation
- **isiscb:citationType**: Type of referenced citation

Relationship types include:
- Is Reviewed By, Reviews
- Includes Series Article
- Is Part Of, Has Part
- References, Is Referenced By
- And others

### LinkedData

Connections to external authorities:

- **type**: Type of external link (VIAF, DOI, URI, etc.)
- **values**: External identifier values

## Standard Vocabulary Mapping

The schema uses these standard vocabularies:

- **Dublin Core (dc:, dcterms:)** - Core bibliographic metadata
- **Schema.org (schema:)** - General-purpose structured data
- **SKOS** - Simple Knowledge Organization System
- **BIBO** - Bibliographic Ontology
- **FOAF** - Friend of a Friend vocabulary
- **Custom IsisCB namespace (isiscb:)** - Domain-specific extensions

## Examples

### Citation Example (Book)

```json
{
  "@context": {...},
  "@id": "https://data.isiscb.org/citation/CBB001180697",
  "@type": ["bibo:Book", "schema:Book", "isiscb:Book"],
  "dc:title": "The History of Mathematics: An Introduction",
  "isiscb:mainTitle": "The History of Mathematics",
  "isiscb:subtitle": "An Introduction",
  "dc:creator": [
    {
      "@id": "https://data.isiscb.org/authority/CBA000023541",
      "schema:name": "Boyer, Carl B.",
      "isiscb:role": "author",
      "isiscb:position": "1.0"
    }
  ],
  "dc:date": "1991",
  "schema:datePublished": "1991",
  "isiscb:yearNormalized": 1991,
  "dc:publisher": {
    "@id": "https://data.isiscb.org/authority/CBA000725764",
    "schema:name": "Wiley"
  },
  "isiscb:publisherLocation": "New York",
  "bibo:edition": "2nd ed.",
  "isiscb:physicalDetails": "xvi, 715 p. : ill.",
  "isiscb:extent": "715 p.",
  "schema:numberOfPages": 715,
  "dc:language": "English",
  "bibo:isbn": "978-0471543978",
  "isiscb:recordID": "CBB001180697",
  "isiscb:recordStatus": "Active"
}
```

### Authority Example (Person)

```json
{
  "@context": {...},
  "@id": "https://data.isiscb.org/authority/CBA000144339",
  "@type": ["schema:Person", "foaf:Person", "isiscb:Person"],
  "schema:name": "Einstein, Albert",
  "schema:familyName": "Einstein",
  "schema:givenName": "Albert",
  "skos:prefLabel": "Einstein, Albert",
  "schema:birthDate": "1879",
  "schema:deathDate": "1955",
  "schema:description": "Theoretical physicist who developed the theory of relativity",
  "isiscb:classificationSystem": "Proper name",
  "isiscb:recordID": "CBA000144339",
  "isiscb:recordStatus": "Active",
  "sameAs": [
    "http://viaf.org/viaf/75121530"
  ]
}
```

## Schema Benefits

1. **Interoperability** - Uses standard vocabularies for maximum compatibility
2. **Preservation** - Maintains domain-specific knowledge through extensions
3. **Flexibility** - Supports diverse entity and relationship types
4. **Linked Data** - Creates a true web of knowledge with rich relationships
5. **Scholarly Context** - Preserves specialized information for history of science research