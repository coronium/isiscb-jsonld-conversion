# IsisCB JSON-LD Conversion Project - Developer Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Project Architecture](#project-architecture)
3. [Adding New Converters](#adding-new-converters)
4. [Testing Procedures](#testing-procedures)
5. [Code Organization and Standards](#code-organization-and-standards)
6. [Error Handling](#error-handling)
7. [Performance Considerations](#performance-considerations)
8. [Contribution Guidelines](#contribution-guidelines)

## Introduction

This Developer Guide provides technical information for developers who want to understand, modify, or extend the IsisCB JSON-LD Conversion codebase. While the main documentation describes the schema design and field mappings from a user perspective, this guide focuses on the implementation details and development processes.

## Project Architecture

### Pipeline Components

The IsisCB JSON-LD conversion is implemented through a modular pipeline architecture that processes records through a series of specialized converters. This approach allows for flexible, maintainable, and extensible conversion logic.

#### Core Pipeline Classes

Two main pipeline classes orchestrate the conversion process:

- **CitationConverterPipeline**: Handles the conversion of bibliographic records
- **AuthorityConverterPipeline**: Handles the conversion of authority records

Each pipeline initializes and chains together field-specific converters to transform the original data into JSON-LD format.

#### Converter Hierarchy

Converters follow an inheritance structure:

1. **BaseConverter**: Abstract base class that defines the common interface and error handling
2. **Field-specific converters**: Specialized converters that inherit from BaseConverter
   - **Common converters**: Handle fields present in both citation and authority records
   - **Citation-specific converters**: Handle fields unique to bibliographic records
   - **Authority-specific converters**: Handle fields unique to authority records

#### Conversion Flow

The conversion process follows these steps:

1. Load CSV data into memory
2. For each record:
   - Apply record identifier conversion
   - Apply record type conversion
   - Apply field-specific converters
   - Validate the resulting JSON-LD document
3. Output the converted records as JSON-LD files

#### Converter Types

The system includes several types of converters:

- **Core field converters**: Handle basic fields like titles, dates, identifiers
- **Relationship converters**: Process complex relationship fields
- **Metadata converters**: Handle administrative metadata
- **Attribute converters**: Process structured attribute data

Each converter is responsible for transforming its specific field into the appropriate JSON-LD structure according to the schema mappings.

### Directory Structure

```
isiscb-jsonld-conversion/
├── config.yml                         # Main configuration file
├── requirements.txt                   # Python dependencies
├── run_converter.py                   # Command-line entry point
├── data/                              # Data directory
│   ├── raw/                           # Input CSV files
│   │   └── samples/                   # Sample files for testing
│   └── processed/                     # Output JSON-LD files
├── docs/                              # Documentation
├── src/                               # Source code
│   └── isiscb/                        # Main package
│       ├── __init__.py
│       ├── converters/                # Field converters
│       │   ├── __init__.py
│       │   ├── base.py                # Base converter class
│       │   ├── schema_mappings.py     # Centralized mapping definitions
│       │   ├── common/                # Common field converters
│       │   ├── citation/              # Citation-specific converters
│       │   └── authority/             # Authority-specific converters
│       ├── pipeline/                  # Pipeline classes
│       │   ├── __init__.py
│       │   ├── citation_pipeline.py   # Citation conversion pipeline
│       │   └── authority_pipeline.py  # Authority conversion pipeline
│       ├── utils/                     # Utility functions
│       │   ├── __init__.py
│       │   ├── data_loader.py         # Data loading utilities
│       │   └── paths.py               # Path management utilities
│       ├── validators/                # Validation utilities
│       │   ├── __init__.py
│       │   └── json_ld_validator.py   # JSON-LD validator
│       └── schemas/                   # JSON schemas for validation
│           ├── citation.json          # Citation schema
│           └── authority.json         # Authority schema
└── tests/                             # Test suite
    ├── __init__.py
    ├── test_conversion.py             # Conversion tests
    └── test_linked_data_conversion.py # Specific converter tests
```

## Adding New Converters

### Creating a New Field Converter

To create a new converter for a field not yet handled:

1. Identify the appropriate category (common, citation, or authority)
2. Create a new file in the corresponding directory
3. Define a class that inherits from `BaseConverter`
4. Implement the `_convert_impl` method

Here's a template for a new converter:

```python
from ..base import BaseConverter
from ..schema_mappings import get_property

class NewFieldConverter(BaseConverter):
    """Converter for the New Field."""
    
    def __init__(self, field_name: str = "New Field"):
        """Initialize the converter."""
        super().__init__(field_name)
    
    def _convert_impl(self, value: str, record_id: str) -> dict:
        """
        Convert the field to JSON-LD format.
        
        Args:
            value: The raw field value
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation
        """
        # Your conversion logic here
        result = {}
        
        # Example: Use centralized property mapping
        property_name = get_property("new_field")
        result[property_name] = value
        
        return result
```

### Adding the Converter to the Pipeline

Once you've created a new converter, you need to add it to the appropriate pipeline:

1. Open the pipeline file (`citation_pipeline.py` or `authority_pipeline.py`)
2. Import your new converter class
3. Add it to the `converters` dictionary in the pipeline's `__init__` method
4. Use it in the `convert_row` method

Example:

```python
from ..converters.citation.new_field import NewFieldConverter

class CitationConverterPipeline:
    def __init__(self, validate: bool = True):
        # Other converters...
        self.converters = {
            # Existing converters...
            'new_field': NewFieldConverter(),
        }
    
    def convert_row(self, row: pd.Series) -> Dict:
        # Existing conversion code...
        
        # Add your new converter
        if 'New Field' in row:
            jsonld.update(self.converters['new_field'].convert(row['New Field'], record_id))
        
        # Rest of conversion code...
```

### Extending Schema Mappings

If your new converter requires additional property mappings:

1. Open `schema_mappings.py`
2. Add your mapping definitions to the appropriate sections
3. Update the `ALL_MAPPINGS` dictionary to include your new mapping

Example:

```python
# Define your new mapping
NEW_FIELD_MAPPING = {
    "primary": "dc:newField",
    "equivalents": ["schema:newField"],
    "extensions": ["isiscb:newFieldExtension"]
}

# Add to ALL_MAPPINGS
ALL_MAPPINGS = {
    # Existing mappings...
    "new_field": NEW_FIELD_MAPPING,
}
```

## Testing Procedures

### Running Tests

The project uses pytest for testing. To run the tests:

```bash
# Run all tests
pytest tests/

# Run a specific test file
pytest tests/test_conversion.py

# Run a specific test function
pytest tests/test_conversion.py::test_single_citation_conversion
```

### Writing Tests for a New Converter

When creating a new converter, you should also create tests for it:

1. Create a test file or add to an existing one in the `tests/` directory
2. Write test functions that check various aspects of your converter
3. Include tests for edge cases (empty values, malformed data, etc.)

Example test for a new converter:

```python
def test_new_field_converter():
    """Test the NewFieldConverter."""
    from src.isiscb.converters.citation.new_field import NewFieldConverter
    
    converter = NewFieldConverter()
    
    # Test with normal value
    result = converter.convert("Test value", "CBB000001")
    assert "dc:newField" in result
    assert result["dc:newField"] == "Test value"
    
    # Test with empty value
    result = converter.convert("", "CBB000002")
    assert len(result) == 0
    
    # Test with malformed value
    # ...
```

### Integration Testing

In addition to testing individual converters, test the integration of your converter in the pipeline:

```python
def test_pipeline_with_new_field():
    """Test the pipeline with the new field converter."""
    # Create a sample row with your new field
    sample_row = pd.Series({
        'Record ID': 'CBB000001',
        'Record Type': 'Book',
        'Title': 'Test Title',
        'New Field': 'Test value'
    })
    
    # Run the pipeline
    pipeline = CitationConverterPipeline()
    result = pipeline.convert_row(sample_row)
    
    # Check the result
    assert "dc:newField" in result
    assert result["dc:newField"] == "Test value"
```

## Code Organization and Standards

### Naming Conventions

- **Classes**: Use CamelCase (e.g., `RecordIdConverter`)
- **Methods and functions**: Use snake_case (e.g., `convert_row`)
- **Variables**: Use snake_case (e.g., `record_id`)
- **Constants**: Use UPPER_SNAKE_CASE (e.g., `CITATION_TYPE_MAPPING`)
- **File names**: Use snake_case (e.g., `record_id_converter.py`)

### Documentation Standards

- **Module docstrings**: Include a brief description of the module's purpose
- **Class docstrings**: Describe the class's purpose and behavior
- **Method docstrings**: Use Google-style docstrings with Args, Returns, and Raises sections
- **Type annotations**: Include type annotations for function parameters and return values

Example:

```python
"""
Module docstring describing the module.
"""

from typing import Dict, Any

class MyClass:
    """
    Class docstring describing the class.
    """
    
    def my_method(self, param1: str, param2: int) -> Dict[str, Any]:
        """
        Method docstring describing what the method does.
        
        Args:
            param1: Description of param1
            param2: Description of param2
            
        Returns:
            Dictionary with the processed result
            
        Raises:
            ValueError: If param1 is empty
        """
        # Method implementation
```

### Error Handling

- Use exceptions for exceptional conditions
- Log errors at appropriate levels
- Include contextual information in error messages
- Handle and recover from errors when possible

## Error Handling

### Error Types

The codebase uses a custom `ConverterException` class for conversion-specific errors. This exception is raised when a converter encounters an error that it cannot recover from.

### Logging

The project uses the Python `logging` module for logging. Each module should get its own logger:

```python
import logging
logger = logging.getLogger('isiscb_conversion')
```

Use appropriate log levels:
- `DEBUG`: Detailed information for debugging
- `INFO`: Confirmation that things are working as expected
- `WARNING`: Indication that something unexpected happened but the program is still working
- `ERROR`: A serious problem that prevented a function from executing
- `CRITICAL`: A very serious error that may prevent the program from continuing

### Error Recovery

Converters should handle errors gracefully and recover when possible:

- Check for missing or malformed data
- Provide reasonable defaults when data is missing
- Log warnings for problematic data
- Continue processing even if some fields fail

## Performance Considerations

### Memory Usage

The conversion process loads CSV files into memory using pandas. For large files, this can consume significant memory. Consider:

- Processing files in batches
- Using data chunking
- Limiting concurrent processing

### Optimizing Converters

For performance-critical converters:

- Pre-compile regular expressions
- Minimize string operations
- Cache repeated calculations
- Use efficient data structures

### Batch Processing

The pipeline supports batch processing through the `batch_size` configuration parameter. This allows processing large files in manageable chunks:

```python
pipeline = CitationConverterPipeline()
pipeline.convert_csv_file(input_file, output_file, batch_size=1000)
```

## Contribution Guidelines

### Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests
5. Run the test suite
6. Update documentation
7. Submit a pull request

### Code Review Process

All code changes should go through a review process:

1. Another developer reviews the code
2. The reviewer checks for:
   - Correct functionality
   - Adherence to coding standards
   - Comprehensive tests
   - Updated documentation
3. The reviewer approves or requests changes
4. Once approved, the changes are merged

### Documentation Updates

When making code changes, be sure to update the relevant documentation:

- Update in-code docstrings
- Update the Developer Guide (this document) if needed
- Update schema documentation if schema changes are involved
- Add examples for new functionality

### Versioning

The project follows semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Incompatible API changes
- MINOR: Backwards-compatible functionality additions
- PATCH: Backwards-compatible bug fixes