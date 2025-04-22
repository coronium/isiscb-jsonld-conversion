# IsisCB JSON-LD Schema Design Documentation

## Table of Contents

1. [Overview](#overview)
2. [Core Vocabularies and Namespaces](#core-vocabularies-and-namespaces)
3. [JSON-LD Context](#json-ld-context)
4. [Core Entity Types](#core-entity-types)
5. [Citation Entities](#citation-entities)
6. [Authority Entities](#authority-entities)
7. [Relationship Structures](#relationship-structures)
8. [Standard Vocabulary Mapping](#standard-vocabulary-mapping)
9. [Examples](#examples)

## Overview

The IsisCB JSON-LD schema design transforms the IsisCB bibliographic and authority data into JSON-LD format while preserving its specialized focus on the history of science, technology, and medicine. This schema follows a hybrid approach that leverages standard bibliographic vocabularies while maintaining domain-specific attributes through custom vocabulary extensions.

This document describes the schema design for version 0.1 (April 22, 2025) of the IsisCB JSON-LD conversion project. As this is a development version, the schema is expected to evolve in future releases.

## Core Vocabularies and Namespaces

The schema uses several established vocabularies to maximize interoperability:

| Prefix | Namespace | Description |
|--------|-----------|-------------|
| `dc` | `http://purl.org/dc/elements/1.1/` | Dublin Core Elements - Core bibliographic metadata |
| `dcterms` | `http://purl.org/dc/terms/` | Dublin Core Terms - Extended bibliographic metadata |
| `schema` | `http://schema.org/` | Schema.org - General-purpose structured data vocabulary |
| `bibo` | `http://purl.org/ontology/bibo/` | Bibliographic Ontology - Specialized academic publication terms |
| `skos` | `http://www.w3.org/2004/02/skos/core#` | Simple Knowledge Organization System - For concepts and controlled vocabularies |
| `foaf` | `http://xmlns.com/foaf/0.1/` | Friend of a Friend - For people and organizations |
| `prism` | `http://prismstandard.org/namespaces/basic/2.0/` | Publishing Requirements for Industry Standard Metadata |
| `vivo` | `http://vivoweb.org/ontology/core#` | VIVO Ontology - For academic and research information |
| `isiscb` | `https://ontology.isiscb.org/vocabulary/` | IsisCB Custom - Domain-specific extensions |

## JSON-LD Context

The JSON-LD context defines the mapping between terms used in the JSON document and IRIs. Each document includes its context:

```json
{
  "@context": {
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "schema": "http://schema.org/",
    "bibo": "http://purl.org/ontology/bibo/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "prism": "http://prismstandard.org/namespaces/basic/2.0/",
    "vivo": "http://vivoweb.org/ontology/core#",
    "isiscb": "https://ontology.isiscb.org/vocabulary/",
    
    "title": "dc:title",
    "name": "schema:name",
    "creator": "dc:creator",
    "contributor": "dc:contributor",
    "editor": "schema:editor",
    "date": "dc:date",
    "datePublished": "schema:datePublished",
    "publisher": "dc:publisher",
    "subject": "dc:subject",
    "language": "dc:language",
    "description": "schema:description",
    "abstract": "dc:abstract",
    "identifier": "dc:identifier",
    
    "recordID": "isiscb:recordID",
    "recordType": "isiscb:recordType",
    "recordStatus": "isiscb:recordStatus",
    "recordNature": "isiscb:recordNature",
    "mainTitle": "isiscb:mainTitle",
    "subtitle": "isiscb:subtitle",
    "yearNormalized": "isiscb:yearNormalized",
    "publisherLocation": "isiscb:publisherLocation",
    "extent": "isiscb:extent",
    "physicalDetails": "isiscb:physicalDetails",
    "pagesFreeText": "isiscb:pagesFreeText",
    "completeCitation": "isiscb:completeCitation",
    "staffNotes": "isiscb:staffNotes",
    "recordHistory": "isiscb:recordHistory",
    "namePreferred": "isiscb:namePreferred",
    "flourishedDate": "isiscb:flourishedDate",
    "classificationSystem": "isiscb:classificationSystem",
    "classificationCode": "isiscb:classificationCode",
    "classificationScheme": "isiscb:classificationScheme",
    "mainCategory": "isiscb:mainCategory",
    "subCategory": "isiscb:subCategory",
    "redirectsTo": "isiscb:redirectsTo",
    
    "familyName": "schema:familyName",
    "givenName": "schema:givenName",
    "nameSuffix": "schema:nameSuffix",
    "birthDate": "schema:birthDate",
    "deathDate": "schema:deathDate",
    "placeName": "schema:placeName",
    "addressCountry": "schema:addressCountry",
    "numberOfPages": "schema:numberOfPages",
    "position": "schema:position",
    "isPartOf": "schema:isPartOf",
    "about": "schema:about",
    "sameAs": "schema:sameAs",
    
    "prefLabel": "skos:prefLabel",
    "altLabel": "skos:altLabel",
    "broader": "skos:broader",
    "narrower": "skos:narrower",
    "related": "skos:related",
    "inScheme": "skos:inScheme",
    "notation": "skos:notation",
    
    "edition": "bibo:edition",
    "pages": "bibo:pages",
    "pageStart": "bibo:pageStart",
    "pageEnd": "bibo:pageEnd",
    "volume": "bibo:volume",
    "issue": "bibo:issue",
    "isbn": "bibo:isbn",
    "issn": "bibo:issn",
    "shortTitle": "bibo:shortTitle",
    
    "isReviewedBy": {
      "@id": "isiscb:isReviewedBy",
      "@type": "@id"
    },
    "reviews": {
      "@id": "isiscb:reviews",
      "@type": "@id"
    },
    "includesSeriesArticle": {
      "@id": "isiscb:includesSeriesArticle",
      "@type": "@id"
    },
    "isPartOf": {
      "@id": "dcterms:isPartOf",
      "@type": "@id"
    },
    "hasPart": {
      "@id": "dcterms:hasPart",
      "@type": "@id"
    },
    "references": {
      "@id": "dcterms:references",
      "@type": "@id"
    },
    "isReferencedBy": {
      "@id": "dcterms:isReferencedBy",
      "@type": "@id"
    },
    
    "relatedAuthorities": "isiscb:relatedAuthorities",
    "relatedCitations": "isiscb:relatedCitations",
    "linkedData": "isiscb:linkedData",
    "attributes": "isiscb:attributes"
  }
}
```

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

## Citation Entities

Citations represent bibliographic records for books, articles, theses, etc.

### Citation Types and Type Mapping

| IsisCB Type | JSON-LD Types | 
|-------------|---------------|
| Book | `bibo:Book`, `schema:Book`, `isiscb:Book` |
| Article | `bibo:Article`, `schema:ScholarlyArticle`, `isiscb:Article` |
| Thesis | `bibo:Thesis`, `schema:Thesis`, `isiscb:Thesis` |
| Chapter | `bibo:Chapter`, `schema:Chapter`, `isiscb:Chapter` |
| Review | `bibo:AcademicArticle`, `schema:Review`, `isiscb:Review` |
| Essay | `bibo:AcademicArticle`, `isiscb:Essay` |
| Website | `schema:WebSite`, `isiscb:Website` |
| Conference Proceeding | `bibo:Proceedings`, `isiscb:ConferenceProceeding` |
| Conference Paper | `bibo:AcademicArticle`, `schema:Article`, `isiscb:ConferencePaper` |

### Citation Properties

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

### Journal-Specific Properties

- **schema:isPartOf**: Link to journal authority
- **bibo:volume**: Journal volume
- **bibo:issue**: Journal issue
- **bibo:pages**: Pages free text
- **bibo:pageStart**: Starting page
- **bibo:pageEnd**: Ending page

### Thesis-Specific Properties

- **vivo:advisorIn**: Thesis advisor
- **bibo:degreeGrantor**: Degree-granting institution

## Authority Entities

Authorities represent controlled vocabulary terms, including people, institutions, concepts, etc.

### Authority Types and Type Mapping

| IsisCB Type | JSON-LD Types | 
|-------------|---------------|
| Person | `schema:Person`, `foaf:Person`, `isiscb:Person` |
| Institution | `schema:Organization`, `foaf:Organization`, `isiscb:Institution` |
| Geographic Term | `schema:Place`, `isiscb:GeographicTerm` |
| Concept | `skos:Concept`, `isiscb:Concept` |
| Time Period | `dcterms:PeriodOfTime`, `isiscb:TimePeriod` |
| Serial Publication | `bibo:Periodical`, `isiscb:SerialPublication` |
| Event | `schema:Event`, `isiscb:Event` |
| Creative Work | `schema:CreativeWork`, `isiscb:CreativeWork` |
| Category Division | `skos:Collection`, `isiscb:CategoryDivision` |
| Cross-reference | `skos:Collection`, `isiscb:CrossReference` |

### Authority Properties

- **schema:name**: Name of the authority
- **skos:prefLabel**: Preferred display label
- **skos:altLabel**: Alternative labels
- **schema:description**: Description text
- **isiscb:classificationSystem**: Classification system used
- **isiscb:classificationCode**: Classification code

#### Person Properties

- **schema:familyName**: Last name
- **schema:givenName**: First name
- **schema:nameSuffix**: Name suffix
- **isiscb:namePreferred**: Preferred form of name
- **schema:birthDate**: Birth year
- **schema:deathDate**: Death year
- **isiscb:flourishedDate**: Active period

#### Institution Properties

- **schema:location**: Location information
- **schema:foundingDate**: Founding date
- **schema:dissolutionDate**: Dissolution date

#### Concept Properties

- **skos:broader**: Broader concepts
- **skos:narrower**: Narrower concepts
- **skos:related**: Related concepts
- **skos:inScheme**: Classification scheme
- **skos:notation**: Classification notation

#### Geographic Term Properties

- **schema:placeName**: Place name
- **schema:addressCountry**: Country code
- **isiscb:geographicEntityType**: Type of place

#### Time Period Properties

- **dcterms:temporal**: Temporal description
- **schema:startDate**: Start date
- **schema:endDate**: End date

#### Serial Publication Properties

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

### Person Contributors

| IsisCB Relationship Type | Primary Property | Equivalent Properties | 
|--------------------------|------------------|------------------------|
| Author | `dc:creator` | `schema:author` |
| Editor | `schema:editor` | (subPropertyOf: `dc:contributor`) |
| Advisor | `vivo:advisorIn` | (subPropertyOf: `dc:contributor`) |
| Contributor | `dc:contributor` | |
| Translator | `schema:translator` | (subPropertyOf: `dc:contributor`) |
| Committee Member | `vivo:hasCommitteeMember` | (subPropertyOf: `dc:contributor`) |
| Interviewer | `isiscb:interviewer` | (subPropertyOf: `dc:contributor`) |
| Guest | `isiscb:guest` | (subPropertyOf: `dc:contributor`) |
| Creator | `dc:creator` | `schema:creator` |
| Writer | `schema:author` | (subPropertyOf: `dc:creator`) |
| Director | `schema:director` | (subPropertyOf: `dc:contributor`) |
| Producer | `schema:producer` | (subPropertyOf: `dc:contributor`) |
| Performer | `schema:performer` | (subPropertyOf: `dc:contributor`) |

### Subject Relationships

| IsisCB Relationship Type | Primary Property | Equivalent Properties | 
|--------------------------|------------------|------------------------|
| Subject | `dc:subject` | `schema:about` |
| Category | `dc:subject` | `schema:about` |

### Publication Relationships

| IsisCB Relationship Type | Primary Property | Equivalent Properties | 
|--------------------------|------------------|------------------------|
| Periodical | `schema:isPartOf` | `dcterms:isPartOf` |
| Book Series | `schema:isPartOf` | `dcterms:isPartOf` |
| Publisher | `dc:publisher` | `schema:publisher` |
| Distributor | `schema:distributor` | |

### Citation-to-Citation Relationships

| IsisCB Relationship Type | Primary Property | Equivalent Properties | 
|--------------------------|------------------|------------------------|
| Is Reviewed By | `isiscb:isReviewedBy` | |
| Reviews | `isiscb:reviews` | |
| Includes Series Article | `isiscb:includesSeriesArticle` | |
| Is Part Of | `dcterms:isPartOf` | `schema:isPartOf` |
| Has Part | `dcterms:hasPart` | `schema:hasPart` |
| References | `dcterms:references` | |
| Is Referenced By | `dcterms:isReferencedBy` | |
| Succeeds | `dcterms:succeeds` | |
| Precedes | `dcterms:precedes` | |

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

### Complex Relationship Example

```json
{
  "@context": {...},
  "@id": "https://data.isiscb.org/citation/CBB001180697",
  "@type": ["bibo:Article", "schema:ScholarlyArticle", "isiscb:Article"],
  "dc:title": "Einstein's Approach to Statistical Mechanics",
  "dc:creator": [
    {
      "@id": "https://data.isiscb.org/authority/CBA000023541",
      "schema:name": "Dauben, Joseph W.",
      "isiscb:role": "author",
      "isiscb:position": "1.0"
    }
  ],
  "dc:subject": [
    {
      "@id": "https://data.isiscb.org/authority/CBA000144339",
      "schema:name": "Einstein, Albert",
      "@type": ["schema:Person", "foaf:Person"]
    },
    {
      "@id": "https://data.isiscb.org/authority/CBA000067891",
      "schema:name": "Statistical mechanics",
      "@type": ["skos:Concept"]
    }
  ],
  "schema:isPartOf": {
    "@id": "https://data.isiscb.org/authority/CBA725764209",
    "schema:name": "Physics Today",
    "@type": ["bibo:Periodical"]
  },
  "bibo:volume": "45",
  "bibo:issue": "3",
  "bibo:pages": "42-48",
  "dc:date": "1992",
  "isiscb:relatedCitations": [
    {
      "@type": "isiscb:isReviewedBy",
      "isiscb:relationshipType": "Is Reviewed By",
      "isiscb:citation": {
        "@id": "https://data.isiscb.org/citation/CBB761549004"
      },
      "isiscb:citationTitle": "Review of Einstein's Approach to Statistical Mechanics",
      "isiscb:citationType": "Review"
    }
  ]
}
```