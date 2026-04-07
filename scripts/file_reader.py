import sys
import argparse
import pandas as pd
from pathlib import Path
import logging

# Configure logging for standard output
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

class FileReadError(Exception):
    """Custom exception for file reading and validation errors."""
    pass

def validate_and_get_path(file_path: str) -> Path:
    """
    Validate existence and extension, returning a clean Path object.
    
    Args:
        file_path: String path to the target file.
        
    Returns:
        Path object if valid.
        
    Raises:
        FileNotFoundError: If path doesn't exist.
        FileReadError: If extension is unsupported.
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: '{file_path}'")
    
    # Extension validation
    supported_extensions = ('.csv', '.xlsx')
    if p.suffix.lower() not in supported_extensions:
        raise FileReadError(
            f"Unsupported extension '{p.suffix}'. Only {supported_extensions} are supported."
        )
    
    return p

def read_file(file_path: Path, preview_rows: int = None) -> pd.DataFrame:
    """
    Read a file using pandas with robust encoding fallback and error handling.
    
    Args:
        file_path: Path object of the file.
        preview_rows: If set, only read up to this many rows (for performance).
        
    Returns:
        pd.DataFrame if successful.
        
    Raises:
        FileReadError: For empty files, parsing errors, or decoding issues.
    """
    suffix = file_path.suffix.lower()
    
    try:
        if suffix == '.csv':
            # Attempt multi-encoding fallback strategy
            # utf-8-sig handles BOM, latin1/cp1252 handles traditional Excel CSV exports
            encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
            
            for enc in encodings:
                try:
                    return pd.read_csv(file_path, encoding=enc, nrows=preview_rows)
                except UnicodeDecodeError:
                    continue
            
            # Final fallback: read with 'utf-8' and replace corrupt characters
            logging.warning("All primary encodings failed. Falling back to 'replace' mode.")
            return pd.read_csv(file_path, encoding='utf-8', errors='replace', nrows=preview_rows)
            
        elif suffix == '.xlsx':
            # Requires 'openpyxl' installed
            try:
                return pd.read_excel(file_path, engine='openpyxl', nrows=preview_rows)
            except ImportError:
                raise FileReadError("Missing dependency: 'openpyxl' is required to read .xlsx files.")

    except pd.errors.EmptyDataError:
        raise FileReadError("The file is empty.")
    except pd.errors.ParserError as e:
        raise FileReadError(f"Failed to parse file: {e}")
    except Exception as e:
        raise FileReadError(f"Unexpected data handling error: {str(e)}")

def display_summary(df: pd.DataFrame, file_info: Path):
    """
    Display a clean, formatted summary of the file contents.
    
    Args:
        df: Loaded DataFrame.
        file_info: Path object of the source file.
    """
    header = f" SUCCESS: {file_info.name} "
    print(f"\n{header.center(64, '=')}")
    print(f"File Path: {file_info.absolute()}")
    print(f"Format:    {file_info.suffix.upper()}")
    print(f"Dimensions: {df.shape[0]} rows x {df.shape[1]} columns")
    print("-" * 64)
    
    print("\nColumns:")
    print(", ".join(df.columns))
    
    print("\nPreview (First 5 Rows):")
    print(df.head())
    
    print("\nColumn Data Types:")
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        print(f" - {dtype}: {count} column(s)")
    
    print("=" * 64 + "\n")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Robust data loader for CSV and Excel files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("file", help="Path to the file to be read")
    parser.add_argument(
        "--preview", 
        type=int, 
        metavar='N',
        help="Only read and display the first N rows"
    )
    
    args = parser.parse_args()
    
    try:
        # 1. Validate extension and existence
        target_path = validate_and_get_path(args.file)
        
        # 2. Load data with fallbacks
        df = read_file(target_path, preview_rows=args.preview)
        
        # 3. Display result
        if df is not None:
            display_summary(df, target_path)
            logging.info("File verification passed.")
            
    except (FileNotFoundError, FileReadError) as e:
        logging.error(e)
        sys.exit(1)
    except Exception as e:
        logging.critical(f"A critical error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
