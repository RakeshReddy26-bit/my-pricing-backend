# Notebook Cleanup Tools

This directory contains utility scripts for cleaning and fixing Jupyter notebooks.

## fix_notebook.py

A Python script that fixes malformed widget metadata in Jupyter notebooks that prevents proper rendering on GitHub and nbviewer.

### Problem

Jupyter notebooks saved from Google Colab sometimes include widget metadata entries that are missing the required 'state' key. This causes GitHub and nbviewer to fail rendering the notebook with an error like:

```
the 'state' key is missing from 'metadata.widgets'
```

### Solution

This script detects and removes malformed `metadata.widgets` entries from notebooks while preserving all other content and creating timestamped backups.

### Usage

```bash
python3 tools/fix_notebook.py <path-to-notebook.ipynb>
```

#### Example

```bash
python3 tools/fix_notebook.py machine-learning-with-tensorflow/week-02/Week2_Notebook1_Cats_and_Dogs.ipynb
```

### Features

- ✅ Automatically detects malformed widget metadata at notebook and cell levels
- ✅ Creates timestamped backups before making changes (`.bak-YYYYMMDD_HHMMSS`)
- ✅ Preserves all notebook content except the problematic metadata
- ✅ Safe error handling with backup restoration on failure
- ✅ Clear console output showing what was changed

### Output

When the script successfully fixes a notebook, it will:

1. Report which metadata was removed (notebook-level or cell-level)
2. Create a backup file with timestamp
3. Write the cleaned notebook back to the original path
4. Exit with code 0 on success, 1 on failure

### Example Output

```
Removing malformed widgets metadata at notebook level
Created backup: notebook.ipynb.bak-20251106_142511
Successfully fixed: notebook.ipynb
```

If no issues are found:

```
No malformed widget metadata found in: notebook.ipynb
```

### Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)
