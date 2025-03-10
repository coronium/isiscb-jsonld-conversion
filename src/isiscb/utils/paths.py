# src/isiscb/utils/paths.py
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
    # (3 levels up from this utility file: utils -> isiscb -> src -> project_root)
    return str(current_path.parents[2])

def ensure_project_in_path():
    """Ensure the project root is in the Python path."""
    project_root = get_project_root()
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    return project_root

def get_data_paths():
    """Get standard data directory paths."""
    project_root = get_project_root()
    return {
        'raw': os.path.join(project_root, 'data', 'raw'),
        'raw_samples': os.path.join(project_root, 'data', 'raw', 'samples'),
        'processed': os.path.join(project_root, 'data', 'processed'),
    }

def find_data_file(filename, subdirs=None):
    """
    Find a data file in the data directories.
    
    Args:
        filename: Name of the file to find
        subdirs: List of subdirectories to search (default: ['raw/samples', 'raw'])
        
    Returns:
        Full path to the file if found, None otherwise
    """
    if subdirs is None:
        subdirs = ['raw/samples', 'raw']
        
    project_root = get_project_root()
    
    # Try each subdirectory
    for subdir in subdirs:
        filepath = os.path.join(project_root, 'data', subdir, filename)
        if os.path.exists(filepath):
            return filepath
    
    # If not found in specific directories, do a general search in data dir
    data_dir = os.path.join(project_root, 'data')
    for root, _, files in os.walk(data_dir):
        if filename in files:
            return os.path.join(root, filename)
            
    return None