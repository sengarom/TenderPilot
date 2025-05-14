import os
import pandas as pd
from modules.matcher import recommend_items_for_tender
from modules.generator import generate_tender_excel

def test_tender_excel_generation():
    # Setup
    db_path = os.path.join('db', 'items.db')
    requirements = "security camera motion detector"
    profit_margin = 15
    output_file = os.path.join('data', 'test_tender_output.xlsx')

    # Remove output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run recommendation and generation
    recommended_items = recommend_items_for_tender(db_path, requirements, profit_margin)
    assert isinstance(recommended_items, list) and len(recommended_items) > 0, "No recommended items returned."
    generate_tender_excel(recommended_items, output_file)

    # Check if file exists
    assert os.path.exists(output_file), f"Excel file was not created: {output_file}"

    # Check columns in the Excel file
    df = pd.read_excel(output_file)
    expected_columns = {'Item Name', 'Description', 'Cost Price', 'Selling Price', 'Profit Margin', 'Timestamp'}
    assert expected_columns.issubset(set(df.columns)), f"Missing columns in Excel file: {expected_columns - set(df.columns)}"
    print("Test passed: Excel file created with expected columns.")

if __name__ == "__main__":
    test_tender_excel_generation()
