"""
Common converters used by multiple entity types.

This package contains converters for fields that appear in both
citation and authority records, such as identifiers and record types.
"""

from .identifier import RecordIdConverter, RedirectConverter
from .types import RecordTypeConverter, RecordNatureConverter