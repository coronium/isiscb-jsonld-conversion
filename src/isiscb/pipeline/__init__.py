"""
Pipeline modules for orchestrating the conversion process.

This package contains pipeline classes that coordinate the conversion
of complete records using the individual field converters.
"""

# Import the class directly without the function which might not exist
from .citation_pipeline import CitationConverterPipeline