"""
Language field converter for IsisCB JSON-LD conversion.

This module provides converters for Language fields in citation records,
with support for standardizing language names to ISO language codes.
"""

import logging
import pandas as pd
from typing import Dict, List, Any, Optional, Union, Tuple

from ..base import BaseConverter

logger = logging.getLogger('isiscb_conversion')

class LanguageConverter(BaseConverter):
    """Converter for Language fields in citation records."""
    
    def __init__(self, field_name: str = "Language"):
        """Initialize the Language converter."""
        super().__init__(field_name)
        
        # Map common language names to ISO 639-1 codes
        # This could be expanded to a more comprehensive mapping
        self.language_code_map = {
            "english": "en",
            "french": "fr",
            "german": "de",
            "spanish": "es",
            "italian": "it",
            "latin": "la",
            "greek": "el",
            "arabic": "ar",
            "russian": "ru",
            "chinese": "zh",
            "japanese": "ja",
            "portuguese": "pt",
            "dutch": "nl",
            "swedish": "sv",
            "danish": "da",
            "norwegian": "no",
            "polish": "pl",
            "czech": "cs",
            "hungarian": "hu",
            "finnish": "fi",
            "turkish": "tr",
            "hebrew": "he",
            "korean": "ko",
            "thai": "th",
            "hindi": "hi",
            "bengali": "bn",
            "urdu": "ur",
            "persian": "fa",
            "indonesian": "id",
            "malay": "ms",
            "vietnamese": "vi",
            "tagalog": "tl",
            "tamil": "ta",
            "telugu": "te",
            "marathi": "mr",
            "punjabi": "pa",
            "gujarati": "gu",
            "malayalam": "ml",
            "kannada": "kn",
            "catalan": "ca",
            "basque": "eu",
            "galician": "gl",
            "irish": "ga",
            "welsh": "cy",
            "albanian": "sq",
            "armenian": "hy",
            "georgian": "ka",
            "ukrainian": "uk",
            "belarusian": "be",
            "bulgarian": "bg",
            "croatian": "hr",
            "serbian": "sr",
            "slovenian": "sl",
            "slovak": "sk",
            "romanian": "ro",
            "lithuanian": "lt",
            "latvian": "lv",
            "estonian": "et",
            "icelandic": "is",
            "faroese": "fo",
            "maltese": "mt",
            "luxembourgish": "lb",
        }
        
    def _convert_impl(self, value: Any, record_id: str) -> Dict:
        """
        Convert language field to JSON-LD format with ISO language codes.
        
        Args:
            value: The language value(s)
            record_id: The record identifier for logging purposes
            
        Returns:
            Dict with JSON-LD representation of the language(s)
        """
        # Handle empty, None, or NaN values
        if value is None or pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
            return {}
        
        # Ensure string format
        if not isinstance(value, str):
            value = str(value)
        
        lang_str = value.strip()
        result = {}
        
        # Parse multiple languages
        # Split by common separators (comma, semicolon, and/or)
        separators = [',', ';', ' and ', ' or ']
        
        # Replace all separators with a common one (comma) for easier processing
        for sep in separators:
            lang_str = lang_str.replace(sep, ',')
        
        # Split by comma and clean up
        languages = [lang.strip() for lang in lang_str.split(',')]
        languages = [lang for lang in languages if lang]  # Remove empty strings
        
        # Process each language
        processed_langs = []
        for lang in languages:
            language_obj = self._process_language(lang)
            if language_obj:
                processed_langs.append(language_obj)
        
        # Add to result
        if processed_langs:
            # For a single language, use a simple structure
            if len(processed_langs) == 1:
                result["dc:language"] = processed_langs[0]
            # For multiple languages, use an array
            else:
                result["dc:language"] = processed_langs
        
        return result
    
    def _process_language(self, language: str) -> Optional[Dict]:
        """
        Process a single language string to a structured object with ISO code.
        
        Args:
            language: The language name or code
            
        Returns:
            Structured language object with name and code
        """
        if not language:
            return None
        
        # Clean up the language name
        lang_name = language.strip().lower()
        
        # Get ISO code if available
        iso_code = self.language_code_map.get(lang_name)
        
        # If no direct match, try partial match
        if not iso_code:
            for name, code in self.language_code_map.items():
                if name in lang_name or lang_name in name:
                    iso_code = code
                    break
        
        # Create language object
        lang_obj = {
            "@value": language,  # Original language name
        }
        
        # Add ISO code if available
        if iso_code:
            lang_obj["@language"] = iso_code
        
        return lang_obj