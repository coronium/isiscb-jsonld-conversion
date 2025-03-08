from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, IO

class BaseExporter(ABC):
    """Base class for exporting JSON-LD to other bibliographic formats."""
    
    @abstractmethod
    def export_record(self, jsonld_record: Dict[str, Any]) -> str:
        """
        Export a single JSON-LD record to the target format.
        
        Args:
            jsonld_record: A JSON-LD record dictionary
            
        Returns:
            String representation in the target format
        """
        pass
    
    @abstractmethod
    def export_records(self, jsonld_records: List[Dict[str, Any]]) -> str:
        """
        Export multiple JSON-LD records to the target format.
        
        Args:
            jsonld_records: List of JSON-LD record dictionaries
            
        Returns:
            String representation in the target format
        """
        pass
    
    @abstractmethod
    def export_to_file(self, jsonld_records: List[Dict[str, Any]], 
                      output_file: str) -> None:
        """
        Export JSON-LD records to a file in the target format.
        
        Args:
            jsonld_records: List of JSON-LD record dictionaries
            output_file: Path to the output file
        """
        pass