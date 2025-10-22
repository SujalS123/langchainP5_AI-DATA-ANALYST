import re
from typing import Dict, Any, Optional

def parse_chart_query(question: str, available_columns: list) -> Optional[Dict[str, Any]]:
    """
    Parse chart queries to extract chart parameters directly.
    This bypasses the AI agent for common patterns.
    """
    question_lower = question.lower().strip()
    
    # Default values
    result = {
        "chart_type": "bar",
        "x_col": None,
        "y_col": None,
        "n": 7,
        "title": None
    }
    
    # Extract chart type
    if "pie chart" in question_lower or "pie" in question_lower:
        result["chart_type"] = "pie"
    elif "line chart" in question_lower or "line" in question_lower or "trend" in question_lower or "over time" in question_lower:
        result["chart_type"] = "line"
    
    # Extract number (top N, first N, etc.)
    number_patterns = [
        r"top (\d+)",
        r"first (\d+)",
        r"bottom (\d+)",
        r"(\d+) top",
        r"(\d+) first",
        r"(\d+) states",
        r"(\d+) customers",
        r"(\d+) items"
    ]
    
    for pattern in number_patterns:
        match = re.search(pattern, question_lower)
        if match:
            try:
                result["n"] = int(match.group(1))
                break
            except (ValueError, IndexError):
                continue
    
    # Extract columns based on available columns
    available_lower = [col.lower() for col in available_columns]
    
    # Y-axis column (metric)
    y_keywords = {
        "profit": ["profit"],
        "sales": ["sales"],
        "revenue": ["revenue", "revenues"],
        "cost": ["cost", "costs"],
        "quantity": ["quantity", "quantities"],
        "amount": ["amount", "amounts"],
        "price": ["price", "prices"],
        "total": ["total", "totals"]
    }
    
    for metric, keywords in y_keywords.items():
        if any(keyword in question_lower for keyword in keywords):
            # Find matching column in available columns
            for i, col_lower in enumerate(available_lower):
                if any(keyword in col_lower for keyword in keywords):
                    result["y_col"] = available_columns[i]
                    break
            if result["y_col"]:
                break
    
    # X-axis column (category)
    x_keywords = {
        "state": ["state", "states"],
        "region": ["region", "regions"],
        "country": ["country", "countries"],
        "city": ["city", "cities"],
        "customer": ["customer", "customers"],
        "product": ["product", "products"],
        "category": ["category", "categories"],
        "date": ["date", "dates", "time", "times"],
        "month": ["month", "months"],
        "year": ["year", "years"]
    }
    
    for category, keywords in x_keywords.items():
        if any(keyword in question_lower for keyword in keywords):
            # Find matching column in available columns
            for i, col_lower in enumerate(available_lower):
                if any(keyword in col_lower for keyword in keywords):
                    result["x_col"] = available_columns[i]
                    break
            if result["x_col"]:
                break
    
    # Generate title if not provided
    if not result["title"]:
        if result["chart_type"] == "pie":
            result["title"] = f"{result['y_col'] or 'Value'} Distribution by {result['x_col'] or 'Category'}"
        else:
            if result["n"] and result["n"] != 7:
                # Handle pluralization for better grammar
                x_col_name = result['x_col'] or 'Items'
                if result['n'] == 1:
                    x_display = x_col_name
                else:
                    # Simple pluralization - just add 's' for most cases
                    x_display = x_col_name + 's' if not x_col_name.endswith('s') else x_col_name
                result["title"] = f"Top {result['n']} {x_display} by {result['y_col'] or 'Value'}"
            else:
                result["title"] = f"{result['y_col'] or 'Value'} by {result['x_col'] or 'Category'}"
    
    # Validate that we have essential columns
    if not result["x_col"] or not result["y_col"]:
        return None
    
    return result

def should_use_direct_parsing(question: str) -> bool:
    """
    Determine if we should use direct parsing instead of AI agent.
    Use direct parsing for common, straightforward chart requests.
    """
    question_lower = question.lower().strip()
    
    # Exclude non-chart queries
    non_chart_patterns = [
        r"what are the columns",
        r"what columns",
        r"list the columns",
        r"show me the columns",
        r"describe the dataset",
        r"what is in the dataset",
        r"how many columns",
        r"column names",
        r"schema",
        r"structure"
    ]
    
    # If it's a non-chart query, don't use direct parsing
    if any(re.search(pattern, question_lower) for pattern in non_chart_patterns):
        return False
    
    # Patterns that are good candidates for direct parsing
    direct_patterns = [
        r"show me top \d+",
        r"show me the top \d+",
        r"top \d+ .* by",
        r"create a .* chart of",
        r"bar chart of",
        r"pie chart of", 
        r"line chart of",
        r"visualize .* by",
        r"show me .* by",
        r"graph of",
        r"plot of",
        r"chart of"
    ]
    
    return any(re.search(pattern, question_lower) for pattern in direct_patterns)
