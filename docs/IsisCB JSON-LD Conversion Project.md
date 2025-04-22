# IsisCB JSON-LD Conversion Project

## User Documentation

### Overview

The IsisCB JSON-LD Conversion project transforms bibliographic and authority data from the IsisCB History of Science Bibliography into modern, interoperable JSON-LD format. This documentation provides guidance on how to use the conversion tools, understand the output, and integrate the converted data into your workflows.

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

3. **Configure your environment**:
   - Review the `config.yml` file to ensure paths are set correctly
   - For production use, set the following environment variables:
     ```bash
     export ISISCB_RAW_DATA_PATH="/path/to/your/csv/files"
     export ISISCB_PROCESSED_DATA_PATH="/path/to/store/jsonld/output"
     export ISISCB_ARCHIVE_PATH="/path/to/archive/original/files"
     ```

### Basic Usage

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

#### Validating Output

To validate the JSON-LD output against the defined schemas:

```bash
python run_converter.py input_file.csv output_file.json --validate
```

Or you can use the validation script directly:

```bash
python src/scripts/validate_jsonld.py output_file.json
```

### Understanding the Output

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

### Hybrid Approach

The converted data uses a hybrid approach that balances interoperability with preservation of domain-specific knowledge:

1. **Standard Vocabularies**: Uses established vocabularies like Dublin Core, Schema.org, and SKOS
2. **Domain-Specific Extensions**: Preserves specialized IsisCB attributes using custom vocabulary extensions
3. **Relationship Preservation**: Maintains the rich network of relationships in the original data

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

#### Memory Issues with Large Files

For very large files, use batch processing:

```bash
python run_converter.py input_file.csv output_file.json --batch-size 500
```

### Integration with Other Systems

The JSON-LD output is designed to work with various systems:

#### Loading into Triple Stores

```bash
# Example using Apache Jena Fuseki
curl -X POST -H "Content-Type: application/ld+json" --data-binary @output_file.json http://localhost:3030/dataset/data
```

#### Conversion to Other RDF Formats

You can use tools like RDF.js or the rdflib Python library to convert the JSON-LD to other RDF formats:

```python
import rdflib
g = rdflib.Graph()
g.parse("output_file.json", format="json-ld")
g.serialize(destination="output_file.ttl", format="turtle")
```

### Further Resources

- Project Documentation: See the `docs/` directory for more detailed documentation
- JSON-LD Context: Explore the context definitions to understand the vocabulary mappings
- Schema Documentation: Review the `docs/schemas.md` file for information about the data models

For questions and support, please create an issue on the project GitHub repository.