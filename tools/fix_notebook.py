#!/usr/bin/env python3
"""
Fix Jupyter notebook widget metadata to enable proper rendering on GitHub/nbviewer.

This script removes malformed widget metadata from Jupyter notebooks that causes
rendering failures with errors like "the 'state' key is missing from 'metadata.widgets'".
"""

import json
import sys
import os
from datetime import datetime
import argparse
import shutil


def has_valid_widget_state(widgets_metadata):
    """
    Check if widget metadata has a valid 'state' key structure.
    
    Args:
        widgets_metadata: The metadata.widgets dictionary
        
    Returns:
        bool: True if the structure is valid, False otherwise
    """
    if not isinstance(widgets_metadata, dict):
        return False
    
    # Valid structure should have a 'state' key at the top level
    return 'state' in widgets_metadata


def fix_notebook(notebook_path):
    """
    Fix widget metadata in a Jupyter notebook.
    
    Args:
        notebook_path: Path to the .ipynb file
        
    Returns:
        bool: True if changes were made, False otherwise
    """
    # Check if file exists
    if not os.path.exists(notebook_path):
        print(f"Error: File not found: {notebook_path}")
        return False
    
    # Load the notebook
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in notebook: {e}")
        return False
    except Exception as e:
        print(f"Error reading notebook: {e}")
        return False
    
    changes_made = False
    
    # Check notebook-level metadata.widgets
    if 'metadata' in notebook:
        if 'widgets' in notebook['metadata']:
            widgets = notebook['metadata']['widgets']
            if not has_valid_widget_state(widgets):
                print(f"Removing malformed widgets metadata at notebook level")
                del notebook['metadata']['widgets']
                changes_made = True
    
    # Check cell-level metadata.widgets
    if 'cells' in notebook:
        for i, cell in enumerate(notebook['cells']):
            if 'metadata' in cell and 'widgets' in cell['metadata']:
                widgets = cell['metadata']['widgets']
                if not has_valid_widget_state(widgets):
                    print(f"Removing malformed widgets metadata from cell {i}")
                    del cell['metadata']['widgets']
                    changes_made = True
    
    if changes_made:
        # Create backup with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{notebook_path}.bak-{timestamp}"
        
        try:
            shutil.copy2(notebook_path, backup_path)
            print(f"Created backup: {backup_path}")
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
        
        # Write the fixed notebook
        try:
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=2, ensure_ascii=False)
                f.write('\n')  # Add trailing newline
            print(f"Successfully fixed: {notebook_path}")
            return True
        except Exception as e:
            print(f"Error writing fixed notebook: {e}")
            # Try to restore from backup
            try:
                shutil.copy2(backup_path, notebook_path)
                print(f"Restored from backup due to write error")
            except Exception as restore_error:
                print(f"Error restoring backup: {restore_error}")
            return False
    else:
        print(f"No malformed widget metadata found in: {notebook_path}")
        return True  # Success - no action needed


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Fix Jupyter notebook widget metadata for proper GitHub rendering',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s notebook.ipynb
  %(prog)s path/to/Week2_Notebook1_Cats_and_Dogs.ipynb
        """
    )
    
    parser.add_argument(
        'notebook_path',
        help='Path to the Jupyter notebook (.ipynb file) to fix'
    )
    
    args = parser.parse_args()
    
    # Fix the notebook
    success = fix_notebook(args.notebook_path)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
