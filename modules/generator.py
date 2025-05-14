import pandas as pd
import logging
import datetime

def generate_tender_excel(recommended_items, output_filename):
    """
    Generates or updates an Excel file for the final tender document.
    Args:
        recommended_items (list of dict): List of items with keys 'item_name', 'description', 'cost_price', 'suggested_selling_price', 'profit_margin_percent'.
        output_filename (str): Name of the Excel file to create or update (e.g., 'Tender_ABC.xlsx').
    Returns:
        None
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    if not recommended_items:
        logger.warning("No recommended items to generate the tender")
        print("No recommended items to generate the tender")
        return
    try:
        logger.info(f"Generating tender Excel file: {output_filename}")
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df = pd.DataFrame([
            {
                'Item Name': item['item_name'],
                'Description': item['description'],
                'Cost Price': item['cost_price'],
                'Selling Price': item['suggested_selling_price'],
                'Profit Margin': item['profit_margin_percent'],
                'Timestamp': timestamp
            }
            for item in recommended_items
        ])
        logger.info(f"Writing {len(df)} items to Excel file.")
        # Write to Excel with formatting
        with pd.ExcelWriter(output_filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            # Format for currency columns
            currency_format = workbook.add_format({'num_format': '"₹"#,##0.00'})
            # Find column indices
            cost_col = df.columns.get_loc('Cost Price')
            sell_col = df.columns.get_loc('Selling Price')
            worksheet.set_column(cost_col, cost_col, 15, currency_format)
            worksheet.set_column(sell_col, sell_col, 15, currency_format)
            # Optionally, set width for other columns
            worksheet.set_column(0, len(df.columns)-1, 20)
        logger.info(f"Tender Excel file '{output_filename}' generated successfully.")
    except Exception as e:
        logger.error(f"Error generating tender Excel file: {e}")
        print(f"Error generating tender Excel file: {e}")