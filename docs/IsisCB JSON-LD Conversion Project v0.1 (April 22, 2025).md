# IsisCB JSON-LD Conversion Project v0.1 (April 22, 2025)

## Table of Contents

1. [Overview](#overview)
2. [For Librarians and Researchers](#for-librarians-and-researchers)
   - [Understanding the JSON-LD Output](#understanding-the-json-ld-output)
   - [Basic Usage](#basic-usage)
   - [Common Issues and Solutions](#common-issues-and-solutions)
3. [For Developers and Technical Users](#for-developers-and-technical-users)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Configuration](#configuration)
   - [Running Conversions](#running-conversions)
   - [Advanced Usage](#advanced-usage)
   - [Handling Large Files](#handling-large-files)

## Overview

The IsisCB JSON-LD Conversion project transforms bibliographic and authority data from the IsisCB History of Science Bibliography into modern, interoperable JSON-LD format. This documentation provides guidance on how to use the conversion tools, understand the output, and integrate the converted data into your workflows.

JSON-LD (JavaScript Object Notation for Linked Data) is a method of encoding Linked Data using JSON. This conversion makes the rich IsisCB dataset more accessible for modern web applications while preserving its specialized focus on the history of science, technology, and medicine.

---

## For Librarians and Researchers

### Understanding the JSON-LD Output

The conversion process produces JSON-LD files that contain:

1. **Core Entities**: Citations and authorities with their properties
2. **Relationships**: Links between entities preserving the original relationships
3. **External References**: Links to external authorities like VIAF and DNB

#### Citation Record Example

```json
{
  "@context": {
    "dc": "http://purl.org/dc/elements/1.1/",
    "schema": "http://schema.org/",
    "bibo": "http://purl.org/ontology/bibo/",
    "isiscb": "https://ontology.isiscb.org/vocabulary/"
  },
  "@id": "https://data.isiscb.org/citation/CBB001180697",
  "@type": ["bibo:Book", "schema:Book", "isiscb:Book"],
  "dc:title": "The History of Mathematics: An Introduction",
  "dc:creator": [
    {
      "@id": "https://data.isiscb.org/authority/CBA000023541",
      "name": "Boyer, Carl B.",
      "schema:position": "1.0",
      "isiscb:role": "author"
    }
  ],
  "dc:date": "1991",
  "dc:publisher": "Wiley",
  "isiscb:publisherLocation": "New York",
  "isiscb:recordID": "CBB001180697"
}
```

#### Authority Record Example

```json
{
  "@context": {
    "schema": "http://schema.org/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "isiscb": "https://ontology.isiscb.org/vocabulary/"
  },
  "@id": "https://data.isiscb.org/authority/CBA000023541",
  "@type": ["schema:Person", "foaf:Person"],
  "schema:name": "Boyer, Carl B.",
  "schema:familyName": "Boyer",
  "schema:givenName": "Carl B.",
  "schema:birthDate": "1906",
  "schema:deathDate": "1976",
  "isiscb:recordID": "CBA000023541",
  "isiscb:recordType": "Person"
}
```

### Basic Usage

To convert your IsisCB export files, follow these steps:

1. Ensure your CSV files are exported from the IsisCB database
2. Place the CSV files in your configured input directory
3. Run the conversion command (see details in the Developer section)
4. Access the resulting JSON-LD files from the configured output directory

### Common Issues and Solutions

#### CSV File Encoding

If you encounter encoding issues with your CSV files, ensure they are UTF-8 encoded:

```bash
iconv -f ISO-8859-1 -t UTF-8 input_file.csv > input_file_utf8.csv
```

#### Missing Relationships

If relationships between records are not appearing in the output:

1. Check that both citation and authority records have been converted
2. Verify that the relationship fields (`Related Authorities`, `Related Citations`) are present in the input CSV
3. Ensure the record IDs match between the related entities

---

## For Developers and Technical Users

### Prerequisites

To use the IsisCB JSON-LD conversion tools, you will need:

- Python 3.10 or later
- Basic knowledge of bibliographic data and JSON-LD concepts
- Input CSV files exported from the IsisCB database

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/coronium/isiscb-jsonld-conversion
   cd isiscb-jsonld-conversion
   ```

2. **Set up the Python environment**:
   ```bash
   # Using conda (recommended)
   conda create -n isiscb-env python=3.10
   conda activate isiscb-env
   
   # Install required packages
   pip install -r requirements.txt
   ```

### Configuration

The conversion process uses configuration settings defined in a `config.yml` file. You can also set environment variables to override these settings.

1. **Review the default configuration**:

   The `config.yml` file contains settings for input/output paths, batch size, and other options.

2. **Set environment variables (optional)**:

   For production environments, you can set the following environment variables:
   ```bash
   export ISISCB_RAW_DATA_PATH="/path/to/your/csv/files"
   export ISISCB_PROCESSED_DATA_PATH="/path/to/store/jsonld/output"
   export ISISCB_ARCHIVE_PATH="/path/to/archive/original/files"
   ```

3. **Configuration options**:

   Based on the available documentation, the following configuration options are available:
   
   - `raw_data_path`: Path to input CSV files
   - `processed_data_path`: Path for output JSON-LD files
   - `archive_path`: Path for archiving original files
   - `batch_size`: Number of records to process per batch (default: 1000)
   - `validate_output`: Whether to validate output against schemas (default: true)
   - `log_level`: Logging level (default: INFO)

### Running Conversions

#### Converting Citation Records

To convert a CSV file containing citation records to JSON-LD:

```bash
python run_converter.py input_file.csv output_file.json
```

For example:
```bash
python run_converter.py data/raw/samples/IsisCB_citation_sample.csv data/processed/citation_output.json
```

#### Converting Authority Records

To convert a CSV file containing authority records to JSON-LD:

```bash
python run_converter.py input_file.csv output_file.json --authority
```

#### Testing With Sample Data

To run a test conversion using sample data:

```bash
python run_converter.py -test
```

This will use a sample file from the `data/raw/samples` directory and save the output to the `data/processed` directory.

### Advanced Usage

#### Converting Specific Record Types

You can specify which record types to convert:

```bash
python run_converter.py input_file.csv output_file.json --types Book,Article
```

#### Specifying Schema Version

To use a specific schema version:

```bash
python run_converter.py input_file.csv output_file.json --schema-version 0.1
```


