"""
Authority-specific converters.

This package contains converters for fields that are specific to
authority records, such as names, descriptions, and classifications.
"""

from .name import NameConverter
from .description import DescriptionConverter
from .classification import ClassificationConverter
from .metadata import AuthorityMetadataConverter
from .related_authorities import AuthorityRelatedAuthoritiesConverter