# IsisCB Field to JSON-LD Property Mapping

This document provides a mapping between the original CSV fields from IsisCB records and their corresponding JSON-LD properties in the unified schema, including allowed values from the sample data.

## Citation and Authority Common Fields

| Original Field      | JSON-LD Property       | Data Type    | Allowed Values / Format / Notes   *(See `Schema Mappings.md` for mappings of the CB terms used here.)*        |
|---------------------|------------------------|--------------|-------------------------------------------|
| **Record ID**           | isiscb:recordID    (should this be some starndr identificer, permalink or something?)    | string       | Citations: `CBB\d+` (e.g., CBB001180697)<br>Authorities: `CBA\d+` (e.g., CBA000144339)  |
| **Record Type**         | isiscb:recordType      | string       | **Citations**: Book, Article, Chapter, Review, Essay, Thesis, Conference Proceeding, Conference Paper, Website, Report<br>**Authorities**: Person, Institution, Geographic Term, Concept, Time Period, Serial Publication, Event, Creative Work, Category Division, Cross-reference, Bibliographic List.  |
| **Record Nature**       | isiscb:recordNature    | string       | Starts with: Active, Delete, Inactive, Redirect<br>Often includes "(RecordStatusExplanation *text*)" suffix |
| Record Action       | isiscb:recordAction    | string       | Processing instruction (appears to be internal)                     |
| Description         | dc:description         | string/object| Variable length text, may contain multiple paragraphs<br>For authorities: may include biographical information, AKA names, Wikipedia links |
| Subjects            | dc:subject             | array        | References to authority records, delimited in original by double slashes (//) |
| CategoryNumbers     | isiscb:categoryNumbers | array        | Alphanumeric codes related to classification systems |
| Language            | dc:language            | string/array | Language names (e.g., "English", "French") rather than ISO codes in raw data |
| Staff Notes         | isiscb:staffNotes      | string       | Internal notes, often contains bracketed metadata like {Birth and Death dates: 1857-1921} |
| Record History      | isiscb:recordHistory   | string       | Verbose changelog containing usernames, dates, and bulk change IDs<br>Often includes "This record was changed as part of bulk change #*ID*" |
| Dataset             | isiscb:dataset         | string       | e.g., "Isis Bibliography of the History of Science (Stephen P. Weldon, ed.)" |
| Created Date        | dc:created             | string       | ISO datetime with timezone: YYYY-MM-DD HH:MM:SS.μs+00:00 |
| Modified Date       | dc:modified            | string       | ISO datetime with timezone: YYYY-MM-DD HH:MM:SS.μs+00:00 |
| Creator             | dc:creator             | string/object| Format: "Name (username)", e.g., "Rebecca Marcolina (rmarc)" |
| Modifier            | isiscb:modifier        | string/object| Format: "Name (username)", e.g., "Stephen Weldon (StephenPWeldon)" |

## Citation-Specific Fields

| Original Field      | JSON-LD Property       | Data Type    | Allowed Values / Format / Notes          |
|---------------------|------------------------|--------------|-------------------------------------------|
| Title               | dc:title               | string/object| Variable length text, may include punctuation like colons for subtitles<br>May contain special characters, quotes, and formatting symbols |
| Author              | dc:creator             | string/array | Format varies: "Last, First", "Last, First Middle", "Organization Name"<br>Multiple authors often separated by " // " in raw data |
| Subtype             | isiscb:recordSubtype   | string       | Further type specification, uncommon in sample data |
| Editor              | schema:editor          | string/array | Format similar to Author<br>May be specified as "ed." or "eds." in raw data |
| Year of publication | schema:datePublished   | string       | Format: YYYY, but may include ranges (YYYY-YYYY) or approximate dates ("ca. YYYY") |
| Edition Details     | bibo:edition           | string       | e.g., "2nd ed.", "Revised edition", format not standardized |
| Place Publisher     | isiscb:placePublisher  | string       | Format: "Place: Publisher, Year" or "Place: Publisher"<br>May include multiple locations separated by semicolons |
| Physical Details    | isiscb:physicalDetails | string       | Format varies, may include page counts, illustrations, dimensions |
| Series              | isiscb:series          | string       | Series title, sometimes with numbering in parentheses |
| ISBN                | bibo:isbn              | string       | Standard 10 or 13 digit ISBN, may include hyphens |
| Pages Free Text     | isiscb:pagesFreeText   | string       | Variable formats: "pp. 1-20", "p. 15", may include Roman numerals |
| Fully Entered       | isiscb:fullyEntered    | string       | Values observed: "Yes", "No", can be empty |
| Proofed             | isiscb:proofed         | string       | Values observed: "Yes", "No", can be empty |
| SPW checked         | isiscb:spwChecked      | string       | Values observed: "Yes", "No", can be empty |
| Published Print     | isiscb:publishedPrint  | string       | Values observed: "Yes", "No", can be empty |
| Published RLG       | isiscb:publishedRLG    | string       | Values observed: "Yes", "No", can be empty |
| Link to Record      | isiscb:linkToRecord    | string       | URI format, uncommon in sample data |
| Journal Link        | isiscb:journalLink     | object       | Reference to journal authority record (CBA ID) |
| Journal Volume      | bibo:volume            | string/number| May include text (e.g., "vol. 10") or just numbers |
| Journal Issue       | bibo:issue             | string/number| May include text (e.g., "no. 2") or just numbers<br>May include special issue information |
| Advisor             | schema:advisors        | string/array | Format similar to Author, for thesis works |
| School              | schema:school          | string/object| Institution name for thesis |
| Includes Series Article | isiscb:includesSeriesArticle | boolean | True/False (uncommon in sample data) |
| Extent              | isiscb:extent          | string       | Size information, e.g., "xii, 245 p.", "3 volumes" |
| Abstract            | dc:abstract            | string/object| Long-form text, may include formatting, paragraphs |
| Complete Citation   | isiscb:completeCitation| string       | Formatted citation following a style guide |
| Stub Record Status  | isiscb:stubRecordStatus| string       | Values observed: "Stub", can be empty |

## Authority-Specific Fields

| Original Field      | JSON-LD Property       | Data Type    | Allowed Values / Format / Notes          |
|---------------------|------------------------|--------------|-------------------------------------------|
| Name                | schema:name            | string       | Variable formats depending on Record Type:<br>- Persons: "Last, First"<br>- Concepts: Single or multi-word terms<br>- Time Periods: "12th century", specific date ranges<br>- Organizations: Full institutional names |
| Last Name           | schema:familyName      | string       | For person authorities; may include compound names, hyphens, apostrophes<br>May include particles like "van", "de", "von" |
| First Name          | schema:givenName       | string       | For person authorities; may include middle names/initials<br>Some records use full middle names, others just initials |
| Name Suffix         | schema:nameSuffix      | string       | Values observed: "of Buckfield", titles, generational suffixes (Jr., Sr., III) |
| Name Preferred      | isiscb:namePreferred   | string       | Canonical form, may differ from Name field<br>Format tends to be more standardized than Name field |
| Classification System | isiscb:classificationSystem | string | **Values observed in sample:**<br>- "Guerlac Committee Classification System (1953-2001)"<br>- "Proper name"<br>- "SHOT Thesaurus Terms"<br>- "Weldon Classification System (2002-present)"<br>- "Weldon Thesaurus Terms (2002-present)"<br>- "Whitrow Classification System (1913-1999)" |
| Classification Code | isiscb:classificationCode | string/number | Alphanumeric code associated with the Classification System |
| Redirect            | isiscb:redirect        | object       | References another authority record (CBA ID)<br>Used with Record Nature "Redirect" |

## Relationship and Complex Fields (To Be Addressed Later)

| Original Field      | JSON-LD Property       | Format/Structure Notes                       |
|---------------------|------------------------|----------------------------------------------|
| Linked Data         | isiscb:linkedData      | Format in raw data: "LinkedData_ID LED544064469 \|\| Status Active \|\| Type DNB \|\| URN http://d-nb.info/gnd/133578771/about/html \|\| ResourceName Deutsche Nationalbibliothek GND Authority file \|\| URL"<br><br>Contains multiple entries with typed links to external authorities (VIAF, DNB, etc.) |
| Attributes          | isiscb:attributes      | Format in raw data: "AttributeID ATT000199651 \|\| AttributeStatus Active \|\| AttributeType BirthToDeathDates \|\| AttributeValue [[1922]] \|\| AttributeFreeFormValue 1922- \|\| AttributeStart 1922 \|\| AttributeEnd  \|\| AttributeDescription"<br><br>Highly structured with multiple attribute types and values |
| Related Authorities | isiscb:relatedAuthorities | References to other authority records with relationship types |
| Related Citations   | isiscb:relatedCitations | Format in raw data: "ACR_ID ACR000606449 \|\| ACRStatus Active \|\| ACRType Subject \|\| ACRDisplayOrder 1.0 \|\| ACRNameForDisplayInCitation  \|\| CitationID CBB001320847 \|\| CitationStatus Active \|\| CitationType Article \|\| CitationTitle Neolithic Adhesive..."<br><br>Contains structured citation references with relationships |
| Related Citations Count | isiscb:relatedCitationsCount | Integer value representing number of related citations |

## Multilingual Content Fields

The following fields commonly contain multilingual content and should use language tags:

- dc:title
- dc:description
- dc:abstract
- schema:name
- skos:prefLabel
- skos:altLabel

### Example of Multilingual Content

```json
"dc:title": [
  {"@value": "History of Science", "@language": "en"},
  {"@value": "Histoire des sciences", "@language": "fr"}
]
```

## Complex Field Structures

Several fields in the IsisCB data contain complex structured information using custom delimiters. These structures need to be parsed and transformed into proper JSON-LD objects:

### Attributes Field Structure

The Attributes field contains structured data with the following pattern:
```
AttributeID ATT000199651 || AttributeStatus Active || AttributeType BirthToDeathDates || AttributeValue [[1922]] || AttributeFreeFormValue 1922- || AttributeStart 1922 || AttributeEnd || AttributeDescription
```

This should be converted to a structured object:
```json
{
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
}
```

### Linked Data Field Structure

The Linked Data field follows this pattern:
```
LinkedData_ID LED544064469 || Status Active || Type DNB || URN http://d-nb.info/gnd/133578771/about/html || ResourceName Deutsche Nationalbibliothek GND Authority file || URL
```

This should be converted to:
```json
{
  "isiscb:linkedData": [
    {
      "id": "LED544064469",
      "status": "Active",
      "type": "DNB",
      "urn": "http://d-nb.info/gnd/133578771/about/html",
      "resourceName": "Deutsche Nationalbibliothek GND Authority file",
      "url": null
    }
  ]
}
```

### Related Citations Field Structure

The Related Citations field follows this pattern:
```
ACR_ID ACR000606449 || ACRStatus Active || ACRType Subject || ACRDisplayOrder 1.0 || ACRNameForDisplayInCitation || CitationID CBB001320847 || CitationStatus Active || CitationType Article || CitationTitle Neolithic Adhesive...
```

Multiple citations are separated by " // " in the original data.

### Staff Notes Field Structure

Staff Notes often contain metadata in curly braces:
```
Removed dates from name. These need to be added to Attributes record. {Birth and Death dates: 1857-1921}{Original name data: Abbott, Wallace Calvin (1857-1921)}
```

This metadata could be structured as:
```json
{
  "isiscb:staffNotes": {
    "text": "Removed dates from name. These need to be added to Attributes record.",
    "metadata": [
      {"key": "Birth and Death dates", "value": "1857-1921"},
      {"key": "Original name data", "value": "Abbott, Wallace Calvin (1857-1921)"}
    ]
  }
}
```

## Edge Cases and Potential Issues

Based on the sample data analysis, the following edge cases and issues should be addressed:

1. **Complex Record Nature Values**:
   - Record Nature often contains explanations in parentheses that vary widely
   - Some include specific usernames and dates, e.g., "Delete (RecordStatusExplanation Deleted as duplicate authority: BES: 2021-08-16)"
   - Consider splitting into separate fields: status and explanation

2. **Inconsistent Date Formats**:
   - Publication years may include approximations ("ca. 1077- ca. 1165")
   - Dates may be ranges, single years, or centuries
   - Need normalization rules for sorting and filtering

3. **Name Field Variations**:
   - Person names have inconsistent formats across records
   - Corporate names may contain punctuation and special characters
   - Historical names may include honorifics and contextual information

4. **Delimited Fields**:
   - Several fields use custom delimiters like " // " or " || "
   - Parsing rules needed for consistent conversion

5. **Nested Complex Data**:
   - Attributes, Linked Data, and Related Citations contain deeply nested structured data
   - Original format uses custom delimiters that need careful parsing

6. **Record History Content**:
   - Contains multiple entries with timestamps, usernames, and actions
   - May include bulk change references that apply to multiple records
   - Consider structured representation rather than raw text

7. **Special Characters and Encoding**:
   - Records contain non-ASCII characters, quotes, diacritics
   - Need consistent UTF-8 handling and character escaping

8. **Multilingual Content Detection**:
   - No explicit language tags in original data
   - Need rules to detect or infer languages

9. **Classification System Alignment**:
   - Multiple overlapping classification systems are in use (Weldon, Whitrow, SHOT, etc.)
   - Need mapping between systems for equivalent concepts

10. **Empty vs. Missing Fields**:
    - Distinction between explicitly empty fields and missing/null fields
    - Some boolean-like fields use "Yes"/"No" vs. empty

## Best Practices for Field Conversion

1. **IDs and URIs**: 
   - Always construct valid URIs for @id using the recordID as base
   - Format: `https://data.isiscb.org/{entity_type}/{record_id}`

2. **Types**: 
   - Use both standard vocabularies (schema:, bibo:) and isiscb: types
   - Map Record Type to the appropriate standard vocabularies

3. **Complex Field Parsing**:
   - Develop robust parsers for fields with custom delimiters
   - Use structured objects rather than raw strings for complex data

4. **Normalization and Original Values**:
   - Normalize values for searching/filtering where appropriate
   - Preserve original values even when normalized versions are added
   - Example: `"schema:datePublished": "ca. 1077", "isiscb:yearNormalized": 1077`

5. **Relationships**:
   - Use @id references to maintain linked data principles
   - Include relationship type information

6. **Language Detection and Tagging**:
   - Implement rules to detect or infer languages in multilingual fields
   - Use ISO 639 language codes in language tags

7. **Hierarchical Classifications**:
   - Preserve classification hierarchy information
   - Link related classification terms

8. **Attribute Structuring**:
   - Convert pipe-delimited attributes to structured objects
   - Preserve typing information (dates, numbers, URIs)

9. **Missing and Empty Values**:
   - Establish consistent rules for handling missing vs. empty fields
   - Omit properties rather than including null values

10. **Date and Number Standardization**:
    - Parse and normalize dates to ISO-8601 format where possible
    - Handle approximate dates, ranges, and special cases
    - Create separate normalized fields for sorting purposes

## Implementation Recommendations

To effectively implement this schema, the following approaches are recommended:

1. **Develop Custom Parsers for Complex Fields**:
   - Create dedicated parsers for Attributes, Linked Data, and Related Citations
   - Implement a pattern-based parser for Staff Notes metadata extraction
   - Extract structured data from Record History entries

2. **Implement a Two-Phase Conversion Process**:
   - Phase 1: Direct field mapping with minimal transformation
   - Phase 2: Advanced parsing and normalization of complex fields

3. **Handle Record Nature Consistently**:
   - Primary statuses observed in sample data: "Active", "Delete", "Redirect", "Inactive"
   - Separate the status from explanation text
   - Create a structured representation including the original text

4. **Address Date Format Variations**:
   - Patterns observed: simple ranges ("1922-2007"), approximate dates ("ca. 1077"), centuries ("13th century")
   - Create a normalized year field for sorting/filtering while preserving original text

   
# Mappings

``