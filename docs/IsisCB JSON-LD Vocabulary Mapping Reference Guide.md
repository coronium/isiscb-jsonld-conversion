# IsisCB JSON-LD Vocabulary Mapping Reference Guide

## Introduction

This document provides a comprehensive reference for the vocabulary mapping used in the IsisCB JSON-LD Conversion Project. It details how fields from the original IsisCB database are mapped to standard vocabularies and IsisCB-specific extensions, ensuring both interoperability with broader systems and preservation of domain-specific knowledge.

## Core Vocabularies Used

The conversion system uses the following standard vocabularies:

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

## Record Identification and Type Mappings

### Record ID

| Original Field | JSON-LD Property | Notes |
|--------------|------------------|----------|
| Record ID (CBB\d+) | `@id` | URI format: `https://data.isiscb.org/citation/{value}` |
| Record ID (CBA\d+) | `@id` | URI format: `https://data.isiscb.org/authority/{value}` |
| Record ID | `isiscb:recordID` | Preserves original ID value |

### Record Type

#### Citation Types

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

#### Authority Types

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

### Record Status

| Original Value | JSON-LD Property | JSON-LD Value |
|----------------|------------------|---------------|
| Active (RecordStatusExplanation...) | `isiscb:recordStatus` | `Active` |
| Inactive (RecordStatusExplanation...) | `isiscb:recordStatus` | `Inactive` |
| Delete (RecordStatusExplanation...) | `isiscb:recordStatus` | `Delete` |
| Redirect (RecordStatusExplanation...) | `isiscb:recordStatus` | `Redirect` |
| Any Record Nature | `isiscb:recordNature` | Original full value |

## Citation Field Mappings

### Bibliographic Fields

| Original Field | JSON-LD Property | Alternative Properties | 
|----------------|------------------|------------------------|
| Title | `dc:title` | `schema:name`, `isiscb:title` |
| Title (main part) | `isiscb:mainTitle` | |
| Title (subtitle) | `isiscb:subtitle` | |
| Author | `dc:creator` | `schema:author` |
| Editor | `schema:editor` | `dc:contributor` |
| Year of publication | `dc:date` | `schema:datePublished` |
| Year of publication (normalized) | `isiscb:yearNormalized` | |
| Place Publisher | `dc:publisher` | `schema:publisher` |
| Place Publisher (location part) | `isiscb:publisherLocation` | |
| Edition Details | `bibo:edition` | `isiscb:editionDetails` |
| Physical Details | `isiscb:physicalDetails` | |
| Extent | `isiscb:extent` | |
| Extent (pages) | `schema:numberOfPages` | |
| Language | `dc:language` | `schema:inLanguage` |
| ISBN | `bibo:isbn` | |
| ISBN | `schema:identifier` | PropertyValue format |
| Abstract | `dc:abstract` | `schema:abstract` |

### Journal-Specific Fields

| Original Field | JSON-LD Property | Alternative Properties | 
|----------------|------------------|------------------------|
| Journal Link | `schema:isPartOf` | `dcterms:isPartOf` |
| Journal Volume | `bibo:volume` | `isiscb:journalVolume` |
| Journal Issue | `bibo:issue` | `isiscb:journalIssue` |
| Pages Free Text | `bibo:pages` | `isiscb:pagesFreeText` |
| Pages (start) | `bibo:pageStart` | |
| Pages (end) | `bibo:pageEnd` | |

### Thesis-Specific Fields

| Original Field | JSON-LD Property | Alternative Properties | 
|----------------|------------------|------------------------|
| Advisor | `vivo:advisorIn` | `dc:contributor` |
| School | `bibo:degreeGrantor` | `schema:CollegeOrUniversity` |

## Authority Field Mappings

### Name Fields

| Original Field | JSON-LD Property | Authority Type |
|----------------|------------------|----------------|
| Name | `schema:name` | All |
| Name | `skos:prefLabel` | All |
| Last Name | `schema:familyName` | Person |
| First Name | `schema:givenName` | Person |
| Name Suffix | `schema:nameSuffix` | Person |
| Name Preferred | `isiscb:namePreferred` | All |
| Name (alternate) | `skos:altLabel` | All |

### Description

| Original Field | JSON-LD Property | Alternative Properties |
|----------------|------------------|------------------------|
| Description | `schema:description` | `dc:description` |
| Description (alternate names) | `skos:altLabel` | |

### Classification

| Original Field | JSON-LD Property | Authority Type |
|----------------|------------------|----------------|
| Classification System | `isiscb:classificationSystem` | All |
| Classification System | `skos:inScheme` | Concept, Category Division |
| Classification Code | `isiscb:classificationCode` | All |
| Classification Code | `skos:notation` | Concept, Category Division |
| Classification (main category) | `isiscb:mainCategory` | Concept, Category Division |
| Classification (subcategory) | `isiscb:subCategory` | Concept, Category Division |

## Relationship Mappings

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

### Institutional Relationships

| IsisCB Relationship Type | Primary Property | Equivalent Properties | 
|--------------------------|------------------|------------------------|
| School | `bibo:degreeGrantor` | `schema:CollegeOrUniversity` |
| Institution | `isiscb:institution` | `schema:affiliation` |
| Meeting | `bibo:presentedAt` | |
| Archival Repository | `isiscb:archivalRepository` | `vivo:ArchivalOrganization` |
| Maintaining Institution | `isiscb:maintainingInstitution` | |

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

### Authority-to-Authority Relationships

| IsisCB Relationship Type | Primary Property | Equivalent Properties | 
|--------------------------|------------------|------------------------|
| Broader Term | `skos:broader` | |
| Narrower Term | `skos:narrower` | |
| Related Term | `skos:related` | |
| Parent Institution | `isiscb:parentInstitution` | `skos:broader` |
| Child Institution | `isiscb:childInstitution` | `skos:narrower` |
| Use | `skos:exactMatch` | |
| Used For | `skos:closeMatch` | |

## Complex Field Mappings

### Linked Data Field

| Original Entry Format | JSON-LD Structure | 
|------------------------|-------------------|
| Type DOI \|\| URN value | `schema:identifier` (PropertyValue) + `isiscb:linkedData` array |
| Type ISBN \|\| URN value | `schema:identifier` (PropertyValue) + `isiscb:linkedData` array |
| Type URI \|\| URN value | `schema:sameAs` + `isiscb:linkedData` array |
| Type VIAF \|\| URN value | `isiscb:linkedData` array |
| Type DNB \|\| URN value | `isiscb:linkedData` array |

### Attributes Field

| Attribute Type | JSON-LD Properties | 
|----------------|-------------------|
| BirthToDeathDates | `schema:birthDate`, `schema:deathDate`, `schema:birthDeathDate`, `isiscb:attributes` array |
| Birth date | `schema:birthDate`, `isiscb:attributes` array |
| Death date | `schema:deathDate`, `isiscb:attributes` array |
| FlourishedDate | `isiscb:flourishedDate`, `isiscb:flourishedDisplayValue`, `isiscb:attributes` array |
| JournalAbbr | `bibo:shortTitle`, `isiscb:journalAbbreviation`, `isiscb:attributes` array |
| GeographicEntityType | `isiscb:geographicEntityType`, additional `@type`, `isiscb:attributes` array |
| CountryCode | `schema:addressCountry`, `isiscb:attributes` array |

## Administrative Field Mappings

| Original Field | JSON-LD Property | Notes |
|----------------|------------------|-------|
| Fully Entered | `isiscb:fullyEntered` | |
| Proofed | `isiscb:proofed` | |
| SPW checked | `isiscb:spwChecked` | |
| Published Print | `isiscb:publishedPrint` | |
| Published RLG | `isiscb:publishedRLG` | |
| Staff Notes | `isiscb:staffNotes` | |
| Staff Notes (metadata) | `isiscb:staffNotesMetadata` | Structured from curly braces |
| Record History | `isiscb:recordHistory` | |
| Created Date | `dc:created` | |
| Modified Date | `dc:modified` | |
| Creator | `dc:creator` | Structured with `schema:name` and `isiscb:username` |
| Modifier | `isiscb:modifier` | Structured with `schema:name` and `isiscb:username` |
| Dataset | `isiscb:dataset` | |

## Example JSON-LD Documents

### Example Citation (Book)

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
  "dc:creator": [
    {
      "@id": "https://data.isiscb.org/authority/CBA000023541",
      "@type": ["schema:Person", "foaf:Person"],
      "schema:name": "Boyer, Carl B.",
      "isiscb:role": "author",
      "isiscb:position": "1.0"
    }
  ],
  "schema:author": [
    {
      "@id": "https://data.isiscb.org/authority/CBA000023541",
      "@type": ["schema:Person", "foaf:Person"],
      "schema:name": "Boyer, Carl B.",
      "isiscb:role": "author",
      "isiscb:position": "1.0"
    }
  ],
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
  "dc:subject": [
    {
      "@id": "https://data.isiscb.org/authority/CBA000067891",
      "@type": ["skos:Concept"],
      "skos:prefLabel": "Mathematics",
      "isiscb:classificationCode": "510"
    }
  ],
  "isiscb:recordID": "CBB001180697",
  "isiscb:recordStatus": "Active",
  "isiscb:recordNature": "Active (RecordStatusExplanation Active by default.)"
}
```

### Example Authority (Person)

```json
{
  "@context": {
    "schema": "http://schema.org/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "isiscb": "https://ontology.isiscb.org/vocabulary/"
  },
  "@id": "https://data.isiscb.org/authority/CBA000023541",
  "@type": ["schema:Person", "foaf:Person", "isiscb:Person"],
  "schema:name": "Boyer, Carl B.",
  "schema:familyName": "Boyer",
  "schema:givenName": "Carl B.",
  "skos:prefLabel": "Boyer, Carl B.",
  "schema:description": "American mathematician and historian of mathematics (1906-1976)",
  "schema:birthDate": "1906",
  "schema:deathDate": "1976",
  "isiscb:recordID": "CBA000023541",
  "isiscb:recordType": "Person",
  "isiscb:recordStatus": "Active",
  "schema:sameAs": [
    "http://viaf.org/viaf/108941091",
    "http://id.loc.gov/authorities/names/n79065001"
  ],
  "isiscb:linkedData": [
    {
      "type": "VIAF",
      "values": ["http://viaf.org/viaf/108941091"]
    },
    {
      "type": "LOC",
      "values": ["http://id.loc.gov/authorities/names/n79065001"]
    }
  ]
}
```

## Best Practices for Using This Mapping

1. **Primary Properties**: Always use the designated primary property for a field first
2. **Equivalent Properties**: Include equivalent properties from standard vocabularies when applicable
3. **Context Definition**: Include all used vocabulary prefixes in the `@context`
4. **URI Patterns**: Follow the established URI patterns for `@id` values
5. **Type Consistency**: Include both standard vocabulary types and IsisCB types
6. **Relationship Representation**: For complex relationships, use both the specific relationship property and the `isiscb:relatedAuthorities` or `isiscb:relatedCitations` array
7. **Attribute Preservation**: For complex attributes, store both the specialized properties and the full `isiscb:attributes` array

## Vocabulary Extension Guidelines

When extending the vocabulary for new terms not covered in this guide:

1. Use the `isiscb:` prefix for all custom terms
2. Follow camelCase naming conventions for properties
3. Follow PascalCase naming conventions for types
4. Document the new term with its relationship to standard vocabularies
5. Consider using subPropertyOf or subClassOf relationships to standard terms
6. Update the JSON-LD context with any new term definitions