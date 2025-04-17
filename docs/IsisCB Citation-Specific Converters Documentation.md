# IsisCB Citation-Specific Converters Documentation

## Overview

This document provides technical details and usage guidelines for the citation-specific converters used in the IsisCB JSON-LD conversion project. These converters handle fields that are unique to citation records, transforming them from their raw CSV format to structured JSON-LD.

## TitleConverter

Converts the `Title` field to appropriate JSON-LD title properties.

### Data Expectations:
- Titles may contain special characters, punctuation, and formatting
- Titles might include subtitles separated by a colon (": ")
- Empty titles should be handled gracefully

### Usage Example:
```python
title_converter = TitleConverter()
result = title_converter.convert("The giant leap: A chronology of Ohio aerospace events", "CBB001180697")
# Result: {"dc:title": "The giant leap: A chronology of Ohio aerospace events"}
```

## PublicationDetailsConverter

Converts publication-related fields including physical details, publisher information, edition details, publication year, extent, language, and ISBN.

### Data Expectations:
- Multiple related fields are processed together
- Fields include: Year of publication, Place Publisher, Edition Details, Physical Details, Extent, Language, ISBN
- Year values may have variations: exact year, ranges, approximate dates with "c." or "ca."
- Place Publisher often follows the pattern "Place: Publisher" or "Place: Publisher, Year"
- Page counts might be in various formats (e.g., "xii, 245 p.", "3 volumes")
- ISBN values may or may not include hyphens

### Usage Example:
```python
publication_details_converter = PublicationDetailsConverter()
fields = {
    'Year of publication': '1969',
    'Place Publisher': 'Chicago: University of Chicago Press',
    'Edition Details': '2nd ed.',
    'Physical Details': 'xiii, 356 p. : ill.',
    'Extent': '356 p.',
    'Language': 'English',
    'ISBN': '9780226789033'
}
result = publication_details_converter.convert(fields, "CBB001180697")
# Result includes various publication properties like dc:date, bibo:isbn, etc.
```

## JournalMetadataConverter

Converts journal-specific fields such as Journal Link, Journal Volume, Journal Issue, and Pages Free Text.

### Data Expectations:
- Journal Link refers to a journal authority record (CBA ID)
- Journal Volume and Issue might include text (e.g., "vol. 10", "no. 2") or just numbers
- Journal Volume/Issue may include range information in the format "value (From start // To end)"
- Pages Free Text might be in various formats: "pp. 1-20", "p. 15", might include Roman numerals

### Usage Example:
```python
journal_metadata_converter = JournalMetadataConverter()
fields = {
    'Journal Link': 'CBA000725764',
    'Journal Volume': '42',
    'Journal Issue': '3',
    'Pages Free Text': 'pp. 215-250'
}
result = journal_metadata_converter.convert(fields, "CBB001180697")
# Result includes schema:isPartOf, bibo:volume, bibo:issue, bibo:pages properties
```

## LanguageConverter

Converts the `Language` field to JSON-LD language properties with standardized language codes.

### Data Expectations:
- Language values may be single languages or multiple languages separated by commas/semicolons
- Values are language names (e.g., "English", "French") rather than ISO codes
- Language names may need mapping to standard ISO 639-1 codes

### Usage Example:
```python
language_converter = LanguageConverter()
result = language_converter.convert("English, French", "CBB001180697")
# Result: {"dc:language": [{"@value": "English", "@language": "en"}, {"@value": "French", "@language": "fr"}]}
```

## AbstractConverter

Converts the `Abstract` field to JSON-LD abstract properties.

### Data Expectations:
- Abstracts may be long text with multiple paragraphs
- May contain special characters, formatting, and Unicode
- Could potentially contain language indicators (not fully implemented yet)

### Usage Example:
```python
abstract_converter = AbstractConverter()
result = abstract_converter.convert("This book examines the development of aerospace technology in Ohio...", "CBB001180697")
# Result: {"dc:abstract": "This book examines the development of aerospace technology in Ohio...", "schema:abstract": "This book examines the development of aerospace technology in Ohio..."}
```

## MetadataConverter

Converts metadata and administrative fields in citation records, including status flags, dates, and record management information.

### Data Expectations:
- Status fields (Fully Entered, Proofed, SPW checked, Published Print, Published RLG, Stub Record Status) are typically "Yes", "No", or empty
- Record History contains verbose changelog text
- Staff Notes may include structured metadata in curly braces (e.g., {key: value})
- Creator and Modifier fields often follow the pattern "Name (username)"
- Date fields (Created Date, Modified Date) are in ISO datetime format

### Usage Example:
```python
metadata_converter = MetadataConverter()
fields = {
    'Fully Entered': 'Yes',
    'Proofed': 'Yes',
    'SPW checked': 'Yes',
    'Record History': 'Record created on 2016-05-27...',
    'Staff Notes': 'Updated citation format. {Original format: Chicago}',
    'Created Date': '2023-09-11 04:54:46.537316+00:00',
    'Modified Date': '2024-07-22 20:56:26.489993+00:00',
    'Creator': 'Rebecca Marcolina (rmarc)',
    'Modifier': 'Stephen Weldon (StephenPWeldon)'
}
result = metadata_converter.convert(fields, "CBB001180697")
# Result includes various metadata properties
```

## General Data Assumptions and Expectations

For all citation-specific converters, the following assumptions and expectations apply:

1. **Citation-Specific Format**:
   - Citation records are identified by record IDs starting with "CBB"
   - Citations have specific fields like title, author, publication details, etc.
   - Different types of citations (Book, Article, etc.) may have slightly different field usage patterns

2. **Publication Information**:
   - Publication years might include approximations ("ca.", "c.") and ranges
   - Publisher information follows bibliographic conventions
   - Page numbers and extents may use various notations (Roman, Arabic)

3. **Journal Relationships**:
   - Articles are linked to journals via the Journal Link field
   - Journal articles contain volume, issue, and page information
   - Periodical citation relationships use standard bibliographic models

4. **Multilingual Content**:
   - Titles, abstracts, and other text fields may contain content in multiple languages
   - Language marking and identification is not always explicit in the source data

5. **Administrative Metadata**:
   - Record status fields indicate the curation state of the citation
   - History fields contain chronological audit information
   - Staff notes may contain structured metadata for internal use

6. **Status Fields**:
   - Boolean-like status fields use "Yes"/"No" values rather than true/false
   - Empty status fields typically mean "No" or "Not Applicable"

7. **Text Formatting**:
   - Titles and abstracts may contain formatting that should be preserved
   - Special characters and Unicode should be handled correctly

8. **Bibliographic Conventions**:
   - Citations follow standard bibliographic practices for their type
   - Field usage may vary by citation type (Book vs. Article vs. Thesis)
   - Complete Citation field contains a formatted citation according to a style guide

By adhering to these assumptions and expectations, the citation-specific converters provide robust transformation of IsisCB citation data into well-structured JSON-LD. These converters complement the common converters to handle the full range of citation fields in the IsisCB database.