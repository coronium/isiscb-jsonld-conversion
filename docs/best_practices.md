# Python Import Path Management Guide
## Overview

This guide outlines best practices for managing Python import paths in the IsisCB JSON-LD Conversion project. Proper path management is essential for ensuring that modules can find and import each other correctly regardless of where scripts are executed from.

## Project Structure

The IsisCB Conversion project follows this directory structure:

```
isiscb-jsonld-conversion/           # Project root
│
├── src/                           # Source code directory
│   ├── __init__.py               # Makes src a package
│   ├── isiscb/                   # Main package
│   │   ├── __init__.py           # Package initialization
│   │   ├── converters/           # Converter modules
│   │   ├── pipeline/             # Pipeline modules
│   │   └── utils/                # Utility modules
│   └── scripts/                  # Executable scripts
│
├── data/                          # Data files
│   ├── raw/                      # Raw input data
│   └── processed/                # Processed output data
│
└── tests/                         # Test scripts
```

## Common Import Issues

1. **Relative vs. Absolute Imports**: Scripts may fail when running from different directories
2. **Missing `__init__.py` Files**: Required to make Python recognize directories as packages
3. **Module Not Found Errors**: Scripts can't find modules in the project structure
4. **Circular Imports**: Modules attempting to import each other

## Best Practices for Imports

### 1. Always Use Absolute Imports

**Preferred Approach**:
```python
# In src/isiscb/pipeline/citation_pipeline.py
from src.isiscb.converters.common.identifier import RecordIdConverter
from src.isiscb.utils.data_loader import load_citation_data
```

**Avoid Relative Imports**:
```python
# These are prone to error depending on where code is run from
from ...converters.common.identifier import RecordIdConverter
from ..utils.data_loader import load_citation_data
```

### 2. Properly Add Project Root to Python Path

For scripts that need to be run directly, ensure the project root is in the Python path:

```python
import os
import sys

# Get the project root
script_path = os.path.abspath(__file__)  # Path to the current script
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))  # Adjust based on script location

# Add project root to Python path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now you can use absolute imports from the project root
from src.isiscb.converters.base import BaseConverter
```

### 3. Create and Use a Path Utility Function

Add a utility function in `src/isiscb/utils/paths.py` to standardize path handling:

```python
import os
import sys
from pathlib import Path

def get_project_root():
    """Return the absolute path to the project root directory."""
    # Start with the current file and navigate up to find project root
    current_path = Path(os.path.abspath(__file__))
    
    # Navigate up until we find the project root (where config.yml exists)
    for parent in [current_path, *current_path.parents]:
        if (parent / 'config.yml').exists():
            return str(parent)
    
    # If not found by config.yml, use a default assumption
    # (3 levels up from this utility file)
    return str(current_path.parents[2])

def ensure_project_in_path():
    """Ensure the project root is in the Python path."""
    project_root = get_project_root()
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    return project_root
```

Then use this in all scripts:

```python
from src.isiscb.utils.paths import ensure_project_in_path

# Add project root to path
project_root = ensure_project_in_path()

# Now import project modules
from src.isiscb.pipeline.citation_pipeline import CitationConverterPipeline
```

### 4. Use `__init__.py` Files Strategically

Every directory that needs to be a package should have an `__init__.py` file. Use these files to export commonly used classes and functions:

```python
# src/isiscb/__init__.py
from .converters.base import BaseConverter
from .pipeline.citation_pipeline import CitationConverterPipeline

# This allows imports like:
# from src.isiscb import CitationConverterPipeline
```

### 5. Use a Wrapper Script for Running Code

For command-line scripts, create a wrapper that handles path setup:

```python
#!/usr/bin/env python
"""
Wrapper script that sets up Python paths before running code.

Usage:
    python run_converter.py input_file.csv output_file.json
"""
import os
import sys
import subprocess

def main():
    # Project root is where this script is located
    project_root = os.path.abspath(os.path.dirname(__file__))
    
    # Set PYTHONPATH environment variable
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root
    
    # Path to the actual script
    script_path = os.path.join(project_root, 'src', 'scripts', 'cb_to_json.py')
    
    # Command and arguments
    cmd = [sys.executable, script_path] + sys.argv[1:]
    
    # Run the script with the proper environment
    subprocess.run(cmd, env=env, check=True)

if __name__ == "__main__":
    main()
```
