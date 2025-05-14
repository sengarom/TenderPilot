import sqlite3
import re
import logging
from modules.pricing import calculate_selling_price

def recommend_items_for_tender(sqlite_db: str, requirements: str, profit_margin_percent: float):
    """
    Recommends items for a tender based on requirements and desired profit margin.
    Args:
        sqlite_db (str): Path to the SQLite database file.
        requirements (str): Statement of requirements (keywords, categories, specs).
        profit_margin_percent (float): Desired profit margin percentage.
    Returns:
        list of dict: Recommended items with description, cost price, and suggested selling price.
        Or a string error message if a database error occurs.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    if not requirements or not requirements.strip():
        logger.warning("No requirements provided, cannot proceed with item recommendation.")
        return "No requirements provided, cannot proceed with item recommendation."
    try:
        logger.info(f"Connecting to SQLite database: {sqlite_db}")
        conn = sqlite3.connect(sqlite_db)
        cursor = conn.cursor()
        # Create indices to improve search performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_master_item_name ON items_master(item_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_items_master_description ON items_master(description)')
        logger.info("Database indices ensured on item_name and description.")
        # Improved keyword extraction using regex to ignore punctuation
        keywords = re.findall(r'\w+', requirements.lower())
        logger.info(f"Extracted keywords for matching: {keywords}")
        query = """
            SELECT item_name, description, cost_price FROM items_master
        """
        cursor.execute(query)
        items = cursor.fetchall()
        recommended = []
        for item_name, description, cost_price in items:
            name_l = item_name.lower() if item_name else ''
            desc_l = description.lower() if description else ''
            if any(kw in name_l or kw in desc_l for kw in keywords):
                # Validate cost_price is a positive float
                try:
                    if cost_price is None or not isinstance(cost_price, (int, float)) or cost_price <= 0:
                        logger.warning(f"Skipping item '{item_name}' due to invalid cost_price: {cost_price}")
                        continue
                    selling_price = calculate_selling_price(cost_price, profit_margin_percent)
                    recommended.append({
                        'item_name': item_name,
                        'description': description,
                        'cost_price': cost_price,
                        'suggested_selling_price': selling_price,
                        'profit_margin_percent': profit_margin_percent
                    })
                    logger.info(f"Recommended item: {item_name} (Cost: {cost_price}, Selling: {selling_price})")
                except Exception as e:
                    logger.error(f"Error calculating selling price for item '{item_name}': {e}")
        logger.info(f"Matched {len(recommended)} items for requirements: {requirements}")
        # Sort by profit margin (highest first)
        recommended.sort(key=lambda x: x['suggested_selling_price'] - x['cost_price'], reverse=True)
        conn.close()
        logger.info("Database connection closed.")
        return recommended
    except Exception as e:
        logger.error(f"Error fetching items from the database: {e}")
        return f"Error fetching items from the database: {e}"