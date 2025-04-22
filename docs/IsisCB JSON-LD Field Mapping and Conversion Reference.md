# IsisCB JSON-LD Field Mapping and Conversion Reference

## Table of Contents

1. [Introduction](#introduction)
2. [For Users: Understanding Field Mappings](#for-users-understanding-field-mappings)
   - [Citation Field Mappings](#citation-field-mappings)
   - [Authority Field Mappings](#authority-field-mappings)
   - [Common Field Mappings](#common-field-mappings)
   - [Complex Fields and Relationships](#complex-fields-and-relationships)
3. [For Developers: Conversion Implementation](#for-developers-conversion-implementation)
   - [Common Converters](#common-converters)
   - [Citation-Specific Converters](#citation-specific-converters)
   - [Authority-Specific Converters](#authority-specific-converters)
   - [Relationship Converters](#relationship-converters)
   - [Data Expectations and Assumptions](#data-expectations-and-assumptions)

## Introduction

This document provides a comprehensive reference for the mapping between fields in the IsisCB database and their corresponding JSON-LD representations. It serves two primary audiences: users who need to understand how their IsisCB data is represented in JSON-LD format, and developers who need details on how the conversion process works.

The field mapping follows a hybrid approach that:
1. Uses established vocabularies (Dublin Core, Schema.org, SKOS, etc.) where possible
2. Preserves domain-specific knowledge through IsisCB-specific extensions
3. Maintains the rich relationship network of the original data

---

## For Users: Understanding Field Mappings

This section explains how fields from the IsisCB database are mapped to JSON-LD properties, helping users understand the structure of the converted data.

### Citation Field Mappings

#### Bibliographic Fields

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
| Complete Citation | `isiscb:completeCitation` | |

#### Journal-Specific Fields

| Original Field | JSON-LD Property | Alternative Properties | 
|----------------|------------------|------------------------|
| Journal Link | `schema:isPartOf` | `dcterms:isPartOf` |
| Journal Volume | `bibo:volume` | `isiscb:journalVolume` |
| Journal Issue | `bibo:issue` | `isiscb:journalIssue` |
| Pages Free Text | `bibo:pages` | `isiscb:pagesFreeText` |
| Pages (start) | `bibo:pageStart` | |
| Pages (end) | `bibo:pageEnd` | |

#### Thesis-Specific Fields

| Original Field | JSON-LD Property | Alternative Properties | 
|----------------|------------------|------------------------|
| Advisor | `vivo:advisorIn` | `dc:contributor` |
| School | `bibo:degreeGrantor` | `schema:CollegeOrUniversity` |

#### Administrative Fields

| Original Field | JSON-LD Property | Notes |
|----------------|------------------|-------|
| Fully Entered | `isiscb:fullyEntered` | Values: "Yes", "No", empty |
| Proofed | `isiscb:proofed` | Values: "Yes", "No", empty |
| SPW checked | `isiscb:spwChecked` | Values: "Yes", "No", empty |
| Published Print | `isiscb:publishedPrint` | Values: "Yes", "No", empty |
| Published RLG | `isiscb:publishedRLG` | Values: "Yes", "No", empty |
| Staff Notes | `isiscb:staffNotes` | Often contains metadata in curly braces |
| Stub Record Status | `isiscb:stubRecordStatus` | Values: "Stub", empty |

### Authority Field Mappings

#### Name Fields

| Original Field | JSON-LD Property | Authority Type |
|----------------|------------------|----------------|
| Name | `schema:name` | All |
| Name | `skos:prefLabel` | All |
| Last Name | `schema:familyName` | Person |
| First Name | `schema:givenName` | Person |
| Name Suffix | `schema:nameSuffix` | Person |
| Name Preferred | `isiscb:namePreferred` | All |
| Name (alternate) | `skos:altLabel` | All |

#### Description and Classification

| Original Field | JSON-LD Property | Alternative Properties |
|----------------|------------------|------------------------|
| Description | `schema:description` | `dc:description` |
| Description (alternate names) | `skos:altLabel` | |
| Classification System | `isiscb:classificationSystem` | `skos:inScheme` for Concepts |
| Classification Code | `isiscb:classificationCode` | `skos:notation` for Concepts |
| Classification (main category) | `isiscb:mainCategory` | |
| Classification (subcategory) | `isiscb:subCategory` | |

#### Type-Specific Fields

| Original Field | JSON-LD Property | Authority Type |
|----------------|------------------|----------------|
| Birth Date | `schema:birthDate` | Person |
| Death Date | `schema:deathDate` | Person |
| Flourished Date | `isiscb:flourishedDate` | Person |
| Place Name | `schema:placeName` | Geographic Term |
| Country Code | `schema:addressCountry` | Geographic Term |
| Temporal Start | `schema:startDate` | Time Period |
| Temporal End | `schema:endDate` | Time Period |
| Short Title | `bibo:shortTitle` | Serial Publication |
| ISSN | `bibo:issn` | Serial Publication |

### Common Field Mappings

| Original Field | JSON-LD Property | Notes |
|----------------|------------------|-------|
| Record ID | `@id` (URI) + `isiscb:recordID` | Format: `https://data.isiscb.org/{entity_type}/{id}` |
| Record Type | `@type` (multiple values) | Maps to multiple vocabularies |
| Record Nature | `isiscb:recordStatus` + `isiscb:recordNature` | Extracts status and preserves full value |
| Created Date | `dc:created` | ISO datetime |
| Modified Date | `dc:modified` | ISO datetime |
| Creator | `dc:creator` (structured) | Format: `Name (username)` |
| Modifier | `isiscb:modifier` (structured) | Format: `Name (username)` |
| Record History | `isiscb:recordHistory` | Changelog text |

### Complex Fields and Relationships

#### Linked Data

External identifiers are mapped in two ways:

1. IsisCB-specific format:
```json
"isiscb:linkedData": [
  {
    "type": "DOI",
    "values": ["10.1086/710720"]
  },
  {
    "type": "VIAF",
    "values": ["http://viaf.org/viaf/18147423004844880849"]
  }
]
```

2. Standard format (varies by type):
```json
"schema:identifier": [
  {
    "@type": "PropertyValue",
    "propertyID": "DOI",
    "value": "10.1086/710720"
  }
],
"schema:sameAs": [
  "http://viaf.org/viaf/18147423004844880849"
]
```

#### Related Authorities

Relationships to authority records are represented in two ways:

1. Standard vocabulary properties (based on relationship type):
```json
"dc:creator": [
  {
    "@id": "https://data.isiscb.org/authority/CBA000023541",
    "name": "Boyer, Carl B.",
    "isiscb:role": "author",
    "isiscb:position": "1.0"
  }
]
```

2. Complete structured representation:
```json
"isiscb:relatedAuthorities": [
  {
    "@type": "isiscb:author",
    "isiscb:relationshipType": "Author",
    "isiscb:displayOrder": "1.0",
    "isiscb:authority": {
      "@id": "https://data.isiscb.org/authority/CBA000023541"
    },
    "isiscb:authorityName": "Boyer, Carl B.",
    "isiscb:authorityType": "Person",
    "isiscb:displayName": "Boyer, Carl B.",
    "isiscb:authorityStatus": "Active"
  }
]
```

#### Related Citations

Citation-to-citation relationships are similarly represented:

1. Standard vocabulary properties:
```json
"isiscb:isReviewedBy": [
  {
    "@id": "https://data.isiscb.org/citation/CBB761549004",
    "dc:title": "Review of Einstein's Approach to Statistical Mechanics"
  }
]
```

2. Complete structured representation:
```json
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
```

#### Attributes

The Attributes field contains structured data about various properties:

```json
"isiscb:attributes": [
  {
    "id": "ATT000199651",
    "status": "Active",
    "type": "BirthToDeathDates",
    "value": [[1922]],
    "freeFormValue": "1922-",
    "start": "1922",
    "end": null,
    "description": null
  }
]
```

This data is also mapped to standard properties where appropriate:
```json
"schema:birthDate": "1922",
"schema:deathDate": null
```

---

## For Developers: Conversion Implementation

This section explains the conversion process and provides details on the converters used to transform IsisCB data to JSON-LD.

### Common Converters

#### RecordIdConverter

Converts the `Record ID` field to a proper JSON-LD identifier.

**Data Expectations**:
- Citation IDs follow the pattern `CBB\d+` (e.g., `CBB001180697`)
- Authority IDs follow the pattern `CBA\d+` (e.g., `CBA000144339`)

**Output**:
```json
{
  "@id": "https://data.isiscb.org/citation/CBB001180697",
  "isiscb:recordID": "CBB001180697"
}
```

#### RecordTypeConverter

Converts the `Record Type` field to appropriate JSON-LD type declarations.

**Data Expectations**:
- Record types match defined mappings for authorities and citations
- Record ID pattern determines whether it's a citation or authority

**Citation Type Mappings**:
- Book → [bibo:Book, schema:Book, isiscb:Book]
- Article → [bibo:Article, schema:ScholarlyArticle, isiscb:Article]
- Thesis → [bibo:Thesis, schema:Thesis, isiscb:Thesis]
- Chapter → [bibo:Chapter, schema:Chapter, isiscb:Chapter]
- Review → [bibo:AcademicArticle, schema:Review, isiscb:Review]
- Essay → [bibo:AcademicArticle, isiscb:Essay]
- Website → [schema:WebSite, isiscb:Website]
- Conference Proceeding → [bibo:Proceedings, isiscb:ConferenceProceeding]
- Conference Paper → [bibo:AcademicArticle, schema:Article, isiscb:ConferencePaper]

**Authority Type Mappings**:
- Person → [schema:Person, foaf:Person, isiscb:Person]
- Institution → [schema:Organization, foaf:Organization, isiscb:Institution]
- Geographic Term → [schema:Place, isiscb:GeographicTerm]
- Concept → [skos:Concept, isiscb:Concept]
- Time Period → [dcterms:PeriodOfTime, isiscb:TimePeriod]
- Serial Publication → [bibo:Periodical, isiscb:SerialPublication]
- Event → [schema:Event, isiscb:Event]
- Creative Work → [schema:CreativeWork, isiscb:CreativeWork]
- Category Division → [skos:Collection, isiscb:CategoryDivision]
- Cross-reference → [skos:Collection, isiscb:CrossReference]

#### RecordNatureConverter

Converts the `Record Nature` field to JSON-LD status properties.

**Data Expectations**:
- Record nature values often follow the pattern "Status (RecordStatusExplanation ...)"
- Primary statuses include: Active, Inactive, Delete, Redirect

**Output**:
```json
{
  "isiscb:recordStatus": "Active",
  "isiscb:recordNature": "Active (RecordStatusExplanation Active by default.)"
}
```

#### LinkedDataConverter

Converts the `Linked Data` field containing external identifiers to JSON-LD format.

**Data Expectations**:
- Entries are separated by " // "
- Each entry follows the pattern: "Type X || URN Y"
- Common types include: DOI, URI, ISBN, VIAF, DNB

**Output**:
```json
{
  "isiscb:linkedData": [
    {
      "type": "DOI",
      "values": ["10.1086/710720"]
    }
  ],
  "schema:identifier": [
    {
      "@type": "PropertyValue",
      "propertyID": "DOI",
      "value": "10.1086/710720"
    }
  ]
}
```

#### AttributesConverter

Converts the `Attributes` field containing structured data about various properties of records.

**Data Expectations**:
- Multiple attribute entries are separated by " // "
- Each entry follows the pattern: "AttributeID X || AttributeStatus Y || AttributeType Z || ..."
- Common AttributeTypes include: BirthToDeathDates, FlourishedDate, JournalAbbr, etc.
- Values may be structured (e.g., [[1922], [2007]]) and need special parsing

**Output**:
```json
{
  "isiscb:attributes": [
    {
      "id": "ATT000215394",
      "status": "Active",
      "type": "BirthToDeathDates",
      "value": [[1922], [2007]],
      "freeFormValue": "1922-2007",
      "start": "1922",
      "end": "2007"
    }
  ],
  "schema:birthDate": "1922",
  "schema:deathDate": "2007"
}
```

### Citation-Specific Converters

#### TitleConverter

Converts the `Title` field to appropriate JSON-LD title properties.

**Data Expectations**:
- Titles may contain special characters, punctuation, and formatting
- Titles might include subtitles separated by a colon (": ")
- Empty titles should be handled gracefully

**Output**:
```json
{
  "dc:title": "The giant leap: A chronology of Ohio aerospace events",
  "isiscb:mainTitle": "The giant leap",
  "isiscb:subtitle": "A chronology of Ohio aerospace events"
}
```

#### PublicationDetailsConverter

Converts publication-related fields including physical details, publisher information, edition details, publication year, extent, language, and ISBN.

**Data Expectations**:
- Year values may have variations: exact year, ranges, approximate dates with "c." or "ca."
- Place Publisher often follows the pattern "Place: Publisher" or "Place: Publisher, Year"
- Page counts might be in various formats (e.g., "xii, 245 p.", "3 volumes")
- ISBN values may or may not include hyphens

**Output**:
```json
{
  "dc:date": "1969",
  "schema:datePublished": "1969",
  "isiscb:yearNormalized": 1969,
  "dc:publisher": "University of Chicago Press",
  "isiscb:publisherLocation": "Chicago",
  "bibo:edition": "2nd ed.",
  "isiscb:physicalDetails": "xiii, 356 p. : ill.",
  "isiscb:extent": "356 p.",
  "schema:numberOfPages": 356,
  "dc:language": "English",
  "bibo:isbn": "9780226789033"
}
```

#### JournalMetadataConverter

Converts journal-specific fields such as Journal Link, Journal Volume, Journal Issue, and Pages Free Text.

**Data Expectations**:
- Journal Link refers to a journal authority record (CBA ID)
- Journal Volume and Issue might include text (e.g., "vol. 10", "no. 2") or just numbers
- Journal Volume/Issue may include range information in the format "value (From start // To end)"
- Pages Free Text might be in various formats: "pp. 1-20", "p. 15", might include Roman numerals

**Output**:
```json
{
  "schema:isPartOf": {
    "@id": "https://data.isiscb.org/authority/CBA000725764"
  },
  "bibo:volume": "42",
  "bibo:issue": "3",
  "bibo:pages": "pp. 215-250",
  "bibo:pageStart": "215",
  "bibo:pageEnd": "250"
}
```

#### AbstractConverter

Converts the `Abstract` field to JSON-LD abstract properties.

**Data Expectations**:
- Abstracts may be long text with multiple paragraphs
- May contain special characters, formatting, and Unicode
- Could potentially contain language indicators (not fully implemented yet)

**Output**:
```json
{
  "dc:abstract": "This book examines the development of aerospace technology in Ohio...",
  "schema:abstract": "This book examines the development of aerospace technology in Ohio..."
}
```

### Relationship Converters

#### RelatedAuthoritiesConverter

Converts the `Related Authorities` field that links citations to authority records with typed relationships.

**Data Expectations**:
- Data follows the structure: "ACR_ID X || ACRStatus Y || ACRType Z || ..."
- Multiple relationships are separated by " // "
- Key components include: ACR_ID, ACRStatus, ACRType, ACRDisplayOrder, ACRNameForDisplayInCitation, AuthorityID, AuthorityStatus, AuthorityType, AuthorityName
- Common relationship types: Author, Editor, Subject, Contributor, Publisher, etc.
- Display order is important for citation rendering

**Processing Rules**:
1. **Ordering**: Authors and contributors are sorted by their display order value
2. **Name Priority**: Display names are preferred over authority names when available
3. **Type Mapping**: Relationship types are mapped to standard vocabulary terms
4. **Grouping**: Related types are grouped together (e.g., all contributor types)

**Output Example**:
```json
{
  "dc:creator": [
    {
      "@id": "https://data.isiscb.org/authority/CBA000023541",
      "name": "Joseph W. Dauben",
      "isiscb:role": "author",
      "isiscb:position": "1.0",
      "isiscb:authorityType": "Person"
    }
  ],
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
    }
  ]
}
```

#### RelatedCitationsConverter

Converts the `Related Citations` field that links citations to other citation records with typed relationships.

**Data Expectations**:
- Data follows the structure: "CCR_ID X || CCRStatus Y || CCRType Z || ..."
- Multiple relationships are separated by " // "
- Key components include: CCR_ID, CCRStatus, CCRType, CitationID, CitationStatus, CitationType, CitationTitle
- Common relationship types: Is Reviewed By, Includes Series Article, References, etc.

**Relationship Type Mapping**:

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

**Output Example**:
```json
{
  "isiscb:isReviewedBy": [
    {
      "@id": "https://data.isiscb.org/citation/CBB761549004",
      "dc:title": "Heavenly Numbers: Astronomy and Authority in Early Imperial China",
      "isiscb:citationType": "Book"
    }
  ],
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
}
```

### Data Expectations and Assumptions

#### Character Encoding and Format

- Data is encoded in UTF-8 format
- Special characters, diacritics, and non-ASCII characters may be present
- Some fields may have inconsistent formatting or missing values
- Complex fields use consistent delimiters: 
  - " // " for separating multiple entries
  - " || " for separating key-value pairs within entries
  - Spaces in delimiters are significant

#### Date Formats

- Publication years might include approximations ("ca.", "c.") and ranges
- Date fields (Created Date, Modified Date) are in ISO datetime format
- Historical dates may be centuries, ranges, or approximate dates

#### Name Formats

- Person names have varying formats across records
- Preferred name format is preserved in namePreferred
- Display names in citations may differ from authority record names

#### Record Status

- Record status is extracted from Record Nature field
- Primary statuses are: Active, Inactive, Delete, Redirect
- Full Record Nature value is preserved including explanations

#### Multilingual Content

- No explicit language tags in original data
- Some fields may contain content in multiple languages
- Language property uses language names rather than ISO codes
