import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.matcher import recommend_items_for_tender
from modules.generator import generate_tender_excel

def main():
    print("=== Tender Recommendation System ===")
    requirements = input("Enter tender requirements (keywords, specs, etc.): ").strip()
    if not requirements:
        print("No requirements provided. Exiting.")
        return
    try:
        profit_margin = float(input("Enter desired profit margin percentage (e.g., 20): ").strip())
    except ValueError:
        print("Invalid profit margin. Exiting.")
        return
    db_path = os.path.join('db', 'items.db')
    recommended_items = recommend_items_for_tender(db_path, requirements, profit_margin)
    if isinstance(recommended_items, str):
        print(f"Error: {recommended_items}")
        return
    if not recommended_items:
        print("No items matched the requirements.")
        return
    print(f"{len(recommended_items)} items recommended. Generating Excel file...")
    os.makedirs('data', exist_ok=True)
    output_file = os.path.join('data', 'Tender_Output.xlsx')
    generate_tender_excel(recommended_items, output_file)
    print(f"Tender document saved to {output_file}")

if __name__ == "__main__":
    main()
