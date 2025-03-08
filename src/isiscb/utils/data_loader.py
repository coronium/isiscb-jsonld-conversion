"""
IsisCB Conversion Utilities

This module provides utility functions for the IsisCB JSON-LD conversion project.
"""

import yaml
import pandas as pd
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: str = '../config.yml') -> Dict[str, Any]:
    """
    Load the project configuration from config.yml
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        # Default configuration if config file is not found
        return {
            'environment': {'current': 'development'},
            'paths': {
                'development': {
                    'raw': '../data/raw/samples/',
                    'processed': '../data/processed/',
                    'schemas': '../src/schemas/'
                }
            }
        }

def get_paths(config_path: str = '../config.yml') -> Dict[str, str]:
    """
    Get the relevant file paths from the configuration
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        Dict[str, str]: Dictionary of paths
    """
    config = load_config(config_path)
    env = config['environment']['current']
    paths = config['paths'][env]
    return paths

def load_citation_data(file_name: str = "IsisCB citation sample.csv", config_path: str = '../config.yml') -> pd.DataFrame:
    """
    Load the citation data from the CSV file
    
    Args:
        file_name (str): Name of the CSV file containing citation data
        config_path (str): Path to the configuration file
        
    Returns:
        pd.DataFrame: DataFrame containing the citation data
    """
    paths = get_paths(config_path)
    file_path = Path(paths['raw']) / file_name
    return pd.read_csv(file_path, encoding='utf-8', low_memory=False)

def load_authorities_data(file_name: str = "CB Authoritiesall2024.10.16.sample_1000.csv", config_path: str = '../config.yml') -> pd.DataFrame:
    """
    Load the authorities data from the CSV file
    
    Args:
        file_name (str): Name of the CSV file containing authority data
        config_path (str): Path to the configuration file
        
    Returns:
        pd.DataFrame: DataFrame containing the authority data
    """
    paths = get_paths(config_path)
    file_path = Path(paths['raw']) / file_name
    return pd.read_csv(file_path, encoding='utf-8', low_memory=False)