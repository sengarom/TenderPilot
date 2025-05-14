import logging

def calculate_selling_price(cost_price: float, profit_margin_percent: float) -> float:
    """
    Calculates the selling price based on cost price and desired profit margin percentage.
    Args:
        cost_price (float): The cost price of the item.
        profit_margin_percent (float): The desired profit margin as a percentage (e.g., 20 for 20%).
    Returns:
        float: The calculated selling price.
    Raises:
        ValueError: If cost_price is less than or equal to zero.
    """
    if cost_price <= 0:
        logging.error("Cost price must be a positive number.")
        raise ValueError("Cost price must be a positive number.")
    selling_price = cost_price * (1 + profit_margin_percent / 100)
    logging.info(f"Calculated selling price: {selling_price} (Cost: {cost_price}, Margin: {profit_margin_percent}%)")
    return selling_price

def suggest_items_with_pricing(items, requirements, profit_margin_percent):
    """
    Suggests items that best fit the tender's requirements and calculates their selling prices.
    Args:
        items (list of dict): List of items, each with 'name', 'description', and 'cost_price'.
        requirements (str): Statement of requirements (e.g., text or Excel content).
        profit_margin_percent (float): Desired profit margin percentage.
    Returns:
        list of dict: Suggested items with their selling prices and profit margins.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    req_keywords = set(word.lower() for word in requirements.split())
    suggested = []
    for item in items:
        name = item.get('name', '').lower()
        desc = item.get('description', '').lower()
        if any(keyword in name or keyword in desc for keyword in req_keywords):
            try:
                selling_price = calculate_selling_price(item['cost_price'], profit_margin_percent)
                suggested.append({
                    'name': item['name'],
                    'description': item['description'],
                    'cost_price': item['cost_price'],
                    'profit_margin_percent': profit_margin_percent,
                    'selling_price': selling_price
                })
                logger.info(f"Recommended item: {item['name']} (Cost: {item['cost_price']}, Selling: {selling_price})")
            except Exception as e:
                logger.error(f"Error recommending item '{item['name']}': {e}")
    return suggested