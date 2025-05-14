import pandas as pd
import sqlite3
from difflib import get_close_matches
import logging

def connect_sqlite_db(sqlite_db: str):
    """
    Connects to a SQLite database and returns the connection object.
    Raises an error with a clear message if the connection fails.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Connecting to SQLite database: {sqlite_db}")
        conn = sqlite3.connect(sqlite_db)
        logger.info("Database connection opened.")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to SQLite database: {e}")
        raise RuntimeError(f"Error connecting to SQLite database: {e}")

def map_excel_columns(excel_file: str):
    """
    Reads the first row of the Excel file, displays column names, and prompts the user to map columns for
    'Item Name', 'Description', and 'Cost Price'. Returns a mapping dict or an error message if mapping fails.
    """
    logger = logging.getLogger(__name__)
    import pandas as pd
    from difflib import get_close_matches

    required = ['Item Name', 'Description', 'Cost Price']
    try:
        df = pd.read_excel(excel_file, nrows=0)
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        return None, f"Error reading Excel file: {e}"
    columns = list(df.columns)
    logger.info(f"Excel columns found: {columns}")
    print(f"Excel columns found: {columns}")

    mapping = {}
    for req in required:
        if req in columns:
            mapping[req] = req
        else:
            # Try fuzzy match
            match = get_close_matches(req, columns, n=1, cutoff=0.7)
            if match:
                logger.info(f"Suggested column for '{req}': {match[0]}")
                print(f"Suggested column for '{req}': {match[0]}")
                use_suggested = input(f"Use '{match[0]}' for '{req}'? (y/n): ").strip().lower()
                if use_suggested == 'y':
                    mapping[req] = match[0]
                    continue
            logger.warning(f"Column for '{req}' not found.")
            print(f"Column for '{req}' not found.")
            print(f"Available columns: {columns}")
            user_col = input(f"Please enter the column name to use for '{req}' (or leave blank to skip): ").strip()
            if user_col in columns:
                mapping[req] = user_col
            else:
                logger.error(f"Essential column '{req}' could not be mapped. Aborting.")
                return None, f"Essential column '{req}' could not be mapped. Aborting."
    return mapping, None

def is_valid_row(row, cost_price_col):
    """
    Checks if the cost price in the row is valid (not NaN and > 0).
    Returns True if valid, False otherwise.
    """
    value = row[cost_price_col]
    if pd.isna(value) or value <= 0:
        logging.warning(f"Invalid cost price detected: {value}")
        return False
    return True

def load_excel_with_column_mapping(excel_file: str, sqlite_db: str):
    """
    Loads data from an Excel file into a SQLite database table named 'items'.
    
    Purpose:
        - Reads the Excel file and allows the user to map columns if the required names differ.
        - Validates the 'Cost Price' column for missing or invalid values (must be > 0).
        - Skips rows with invalid cost price and prints an error message for each.
        - Creates the 'items' table in the SQLite database if it does not exist.
        - Inserts valid rows into the database using bulk insert for performance.
    
    Args:
        excel_file (str): Path to the Excel file to be loaded. The file should contain columns for item name, description, and cost price (names can be mapped interactively).
        sqlite_db (str): Path to the SQLite database file where the data will be inserted.
    
    Returns:
        None on success. Prints error messages for invalid rows or mapping issues. Raises exceptions for connection errors.
    """
    logger = logging.getLogger(__name__)
    required = {
        'Item Name': None,
        'Description': None,
        'Cost Price': None
    }
    df = pd.read_excel(excel_file)
    columns = list(df.columns)

    # Try to auto-map columns using fuzzy matching
    for req in required:
        match = get_close_matches(req, columns, n=1, cutoff=0.7)
        if match:
            required[req] = match[0]

    # Prompt user for any unmapped columns
    for req in required:
        if required[req] is None:
            logger.warning(f"Column for '{req}' not found.")
            print(f"Column for '{req}' not found.")
            print(f"Available columns: {columns}")
            user_col = input(f"Please enter the column name to use for '{req}': ")
            while user_col not in columns:
                logger.warning(f"Invalid column name entered: {user_col}")
                print("Invalid column name. Try again.")
                user_col = input(f"Please enter the column name to use for '{req}': ")
            required[req] = user_col

    # Connect to SQLite and create table if needed
    conn = connect_sqlite_db(sqlite_db)
    cursor = conn.cursor()
    logger.info("Database connection established for loading Excel data.")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            description TEXT,
            cost_price REAL
        )
    ''')
    logger.info("Ensured 'items' table exists.")

    # Prepare valid rows for bulk insert
    rows_to_insert = []
    for idx, row in df.iterrows():
        if not is_valid_row(row, required['Cost Price']):
            logger.warning(f"Invalid cost price in row {idx + 2}: {row[required['Cost Price']]}. Skipping row.")
            print(f"Invalid cost price in row {idx + 2}: {row[required['Cost Price']]}. Skipping row.")
            continue
        rows_to_insert.append(
            (
                row[required['Item Name']],
                row[required['Description']],
                row[required['Cost Price']]
            )
        )
    if rows_to_insert:
        cursor.executemany(
            'INSERT INTO items (item_name, description, cost_price) VALUES (?, ?, ?)',
            rows_to_insert
        )
        logger.info(f"Inserted {len(rows_to_insert)} valid rows into 'items' table.")
    else:
        logger.warning("No valid rows to insert into 'items' table.")
    conn.commit()
    conn.close()
    logger.info("Database connection closed after loading Excel data.")

def create_items_master_table(sqlite_db: str, column_mapping: dict = None):
    """
    Connects to a SQLite database and creates the 'items_master' table if it does not exist.
    
    Purpose:
        - Establishes a connection to the specified SQLite database.
        - Creates a table named 'items_master' with columns: id (primary key), item_name (text), description (text), and cost_price (real).
        - Allows for custom column names by providing a column_mapping dictionary that maps logical names ('item_name', 'description', 'cost_price') to actual column names.
    
    Args:
        sqlite_db (str): Path to the SQLite database file.
        column_mapping (dict, optional): Dictionary mapping logical column names to custom column names. Defaults to None (uses standard names).
    
    Returns:
        None. Raises an exception if the database connection fails.
    """
    logger = logging.getLogger(__name__)
    logical_names = {
        'item_name': 'item_name',
        'description': 'description',
        'cost_price': 'cost_price'
    }
    if column_mapping:
        logical_names.update(column_mapping)

    conn = connect_sqlite_db(sqlite_db)
    cursor = conn.cursor()
    logger.info("Database connection established for creating 'items_master' table.")
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS items_master (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {logical_names['item_name']} TEXT,
            {logical_names['description']} TEXT,
            {logical_names['cost_price']} REAL
        )
    ''')
    logger.info("Ensured 'items_master' table exists.")
    conn.commit()
    conn.close()
    logger.info("Database connection closed after creating 'items_master' table.")
