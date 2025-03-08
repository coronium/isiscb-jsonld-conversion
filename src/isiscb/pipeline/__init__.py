"""
Pipeline modules for orchestrating the conversion process.

This package contains pipeline classes that coordinate the conversion
of complete records using the individual field converters.
"""

from .citation_pipeline import CitationConverterPipeline, convert_citations_to_jsonld
