"""
Base converter components for IsisCB JSON-LD conversion.

This module provides base classes and utilities for field converters.
"""

import logging
from typing import Dict, Any, Optional, Union, List

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('isiscb_conversion')

class ConverterException(Exception):
    """Exception raised for errors in the converter."""
    pass

class BaseConverter:
    """Base class for all field converters."""
    
    def __init__(self, field_name: str):
        """
        Initialize the converter.
        
        Args:
            field_name: Name of the field being converted
        """
        self.field_name = field_name
    
    def convert(self, value: Any, record_id: str = "unknown", **kwargs) -> Dict:
        """
        Convert a field value to its JSON-LD representation.
        
        Args:
            value: The raw value to convert
            record_id: Record identifier for logging purposes
            **kwargs: Additional keyword arguments that may be used by subclasses
            
        Returns:
            Dict containing the JSON-LD representation
        
        Raises:
            ConverterException: If conversion fails
        """
        try:
            return self._convert_impl(value, record_id, **kwargs)
        except Exception as e:
            logger.error(f"Error converting {self.field_name} for record {record_id}: {str(e)}")
            if isinstance(e, ConverterException):
                raise
            raise ConverterException(f"Failed to convert {self.field_name}: {str(e)}") from e
    
    def _convert_impl(self, value: Any, record_id: str, **kwargs) -> Dict:
        """
        Implementation of the conversion logic.
        
        Args:
            value: The raw value to convert
            record_id: Record identifier for logging purposes
            **kwargs: Additional keyword arguments that may be used by subclasses
            
        Returns:
            Dict containing the JSON-LD representation
        """
        raise NotImplementedError("Subclasses must implement _convert_impl")