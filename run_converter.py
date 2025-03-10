#!/usr/bin/env python
"""
Helper script to run the IsisCB JSON-LD converter with proper path configuration.

Usage:
    python run_converter.py input_file.csv output_file.json
    python run_converter.py -test
    python run_converter.py -test --validate  # Run with validation
"""

import sys
import os
import subprocess
import logging
import datetime
import argparse
from pathlib import Path

def main():
    """Set up the environment and run the converter."""
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('isiscb_runner')
    
    # Get the project root
    project_root = os.path.abspath(os.path.dirname(__file__))
    logger.info(f"Project root: {project_root}")
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run the IsisCB JSON-LD converter')
    parser.add_argument('-test', action='store_true', help='Run with test data')
    parser.add_argument('--validate', action='store_true', help='Enable validation of JSON-LD output')
    parser.add_argument('input_file', nargs='?', help='Input CSV file path')
    parser.add_argument('output_file', nargs='?', help='Output JSON file path')
    
    args = parser.parse_args()
    
    # Check if -test flag is provided
    if args.test:
        # Generate timestamp for output filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Look for input files in various locations
        potential_input_files = [
            os.path.join(project_root, 'data', 'raw', 'samples', 'IsisCB citation sample.csv'),
            os.path.join(project_root, 'data', 'raw', 'IsisCB citation sample.csv'),
            os.path.join(project_root, 'data', 'raw', 'samples', 'citation_sample_133.csv'),
            os.path.join(project_root, 'data', 'raw', 'citation_sample_133.csv')
        ]
        
        input_file = None
        for file_path in potential_input_files:
            if os.path.exists(file_path):
                input_file = file_path
                logger.info(f"Using input file: {input_file}")
                break
                
        if not input_file:
            # Search for any CSV file in data directories
            for root, _, files in os.walk(os.path.join(project_root, 'data')):
                for file in files:
                    if file.endswith('.csv'):
                        input_file = os.path.join(root, file)
                        logger.info(f"Found CSV file: {input_file}")
                        break
                if input_file:
                    break
            
            if not input_file:
                logger.error("No CSV input files found.")
                return 1
        
        output_file = os.path.join(project_root, 'data', 'processed', f'test_citation_{timestamp}.json')
    else:
        # Use command line arguments
        if not args.input_file or not args.output_file:
            parser.print_help()
            return 1
        
        input_file = args.input_file
        output_file = args.output_file
    
    # Convert to absolute paths if they're relative
    if not os.path.isabs(input_file):
        input_file = os.path.abspath(os.path.join(project_root, input_file))
    if not os.path.isabs(output_file):
        output_file = os.path.abspath(os.path.join(project_root, output_file))
    
    logger.info(f"Input file: {input_file}")
    logger.info(f"Output file: {output_file}")
    
    # Check if the input file exists
    if not os.path.exists(input_file):
        logger.error(f"Input file does not exist: {input_file}")
        return 1
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Created output directory: {output_dir}")
    
    # Set environment variables for Python path
    env = os.environ.copy()
    
    # Explicitly set PYTHONPATH to include key directories
    python_paths = [
        project_root,
        os.path.join(project_root, 'src')
    ]
    env['PYTHONPATH'] = os.pathsep.join(python_paths)
    
    # Create a simple wrapper script that we'll run instead
    wrapper_script = os.path.join(project_root, 'run_direct.py')
    with open(wrapper_script, 'w') as f:
        f.write(f"""#!/usr/bin/env python
import sys
import os

# Add project paths
sys.path.insert(0, {repr(project_root)})
sys.path.insert(0, {repr(os.path.join(project_root, 'src'))})

# Now try to import and run
try:
    from src.isiscb.pipeline.citation_pipeline import CitationConverterPipeline
    
    def main():
        input_file = {repr(input_file)}
        output_file = {repr(output_file)}
        validate = {repr(args.validate)}
        
        # Initialize the converter pipeline with validation option
        pipeline = CitationConverterPipeline(validate=validate)
        
        # Convert the citations
        print(f"Converting citations from '{{input_file}}'...")
        results, validation_results = pipeline.convert_csv_file(input_file, output_file)
        
        print(f"Converted {{len(results)}} citation records to JSON-LD")
        
        if validate:
            print(f"Validation results: {{validation_results['valid']}} valid, {{validation_results['invalid']}} invalid")
            if validation_results['invalid'] > 0:
                validation_file = os.path.splitext(output_file)[0] + '_validation.json'
                print(f"Validation errors were found. See {{validation_file}} for details")
        
        print(f"Output saved to: {{output_file}}")
        return 0
        
    if __name__ == "__main__":
        sys.exit(main())
except Exception as e:
    print(f"Error: {{e}}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
""")
    
    logger.info(f"Created wrapper script: {wrapper_script}")
    
    # Run the wrapper script
    command = [sys.executable, wrapper_script]
    logger.info(f"Running command: {' '.join(command)}")
    logger.info(f"PYTHONPATH: {env['PYTHONPATH']}")
    
    try:
        process = subprocess.run(
            command,
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(process.stdout)
        if process.stderr:
            print("ERRORS/WARNINGS:")
            print(process.stderr)
        
        logger.info("Conversion completed successfully")
        
        # Remove the temporary wrapper script
        try:
            os.remove(wrapper_script)
        except:
            pass
            
        return 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Conversion failed with exit code {e.returncode}")
        print(e.stdout)
        print("ERRORS:")
        print(e.stderr)
        
        # Remove the temporary wrapper script
        try:
            os.remove(wrapper_script)
        except:
            pass
            
        return e.returncode

if __name__ == "__main__":
    sys.exit(main())