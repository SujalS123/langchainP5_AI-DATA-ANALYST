import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from app.services.tools import prepare_bar_chart_data

def test_direct_chart_generation():
    # Create sample data
    sample_data = {
        'State': ['Indiana', 'Washington', 'Delaware', 'Michigan', 'Minnesota', 'California', 'Texas', 'New York'],
        'Profit': [8399.976, 6719.9808, 5039.9856, 4946.37, 4630.4755, 4000.0, 3500.0, 3000.0],
        'Sales': [15000.0, 12000.0, 9000.0, 8500.0, 8000.0, 7500.0, 7000.0, 6500.0]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Test different chart configurations directly
    test_cases = [
        {"x_col": "State", "y_col": "Profit", "n": 3, "title": "Top 3 States by Profit"},
        {"x_col": "State", "y_col": "Sales", "n": 5, "title": "Top 5 States by Sales"},
        {"x_col": "State", "y_col": "Profit", "n": 7, "title": "Profit by State"}
    ]
    
    for i, params in enumerate(test_cases, 1):
        print(f'\n=== Test Case {i}: {params["title"]} ===')
        chart_spec = prepare_bar_chart_data(df, **params)
        
        if chart_spec.get('error'):
            print(f'Error: {chart_spec["error"]}')
        else:
            print(f'Chart Type: {chart_spec.get("type")}')
            print(f'Title: {chart_spec.get("options", {}).get("plugins", {}).get("title", {}).get("text", "No title")}')
            print(f'Labels: {chart_spec.get("data", {}).get("labels", [])}')
            print(f'Data Points: {len(chart_spec.get("data", {}).get("datasets", [{}])[0].get("data", []))}')
            print(f'Y-axis label: {chart_spec.get("data", {}).get("datasets", [{}])[0].get("label", "No label")}')

if __name__ == "__main__":
    test_direct_chart_generation()
