#!/usr/bin/env python
"""Console scripts for ezinput."""
import json
import sys
from pathlib import Path


def run_notebook():
    """Execute a Jupyter notebook file as a Python script.

    Usage:
        ezinput notebook.ipynb
    """
    if len(sys.argv) < 2:
        print("Usage: ezinput <notebook.ipynb>")
        sys.exit(1)

    notebook_path = Path(sys.argv[1])

    if not notebook_path.exists():
        print(f"Error: File '{notebook_path}' not found.")
        sys.exit(1)

    if not notebook_path.suffix == ".ipynb":
        print(
            f"Error: File '{notebook_path}' is not a Jupyter notebook (.ipynb)"
        )
        sys.exit(1)

    try:
        # Read the notebook file
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = json.load(f)

        # Get all cells
        cells = notebook.get("cells", [])

        if not cells:
            print(f"No cells found in '{notebook_path}'")
            sys.exit(0)

        code_cells = [c for c in cells if c.get("cell_type") == "code"]
        markdown_cells = [c for c in cells if c.get("cell_type") == "markdown"]

        print(
            f"Executing notebook '{notebook_path}' "
            f"({len(code_cells)} code cells, "
            f"{len(markdown_cells)} markdown cells)"
        )
        print("=" * 60)

        # Create a shared namespace for all cells
        global_namespace = {
            "__name__": "__main__",
            "__file__": str(notebook_path.absolute()),
        }

        # Process cells in order
        for cell in cells:
            cell_type = cell.get("cell_type")
            source = cell.get("source", [])

            if isinstance(source, list):
                content = "".join(source)
            else:
                content = source

            if cell_type == "markdown":
                # Print markdown cells
                print(content)
                print()
            elif cell_type == "code":
                # Execute code cells
                if content.strip():
                    exec(content, global_namespace)

        print("=" * 60)
        print(f"Notebook executed successfully: {notebook_path}")

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in notebook file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error executing notebook: {e}")
        raise


if __name__ == "__main__":
    run_notebook()
