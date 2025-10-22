import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from app.services.agent_service import analyze_question

async def test_columns_query():
    # Create sample data with multiple columns
    sample_data = {
        'State': ['Indiana', 'Washington', 'Delaware', 'Michigan', 'Minnesota', 'California', 'Texas', 'New York'],
        'Profit': [8399.976, 6719.9808, 5039.9856, 4946.37, 4630.4755, 4000.0, 3500.0, 3000.0],
        'Sales': [15000.0, 12000.0, 9000.0, 8500.0, 8000.0, 7500.0, 7000.0, 6500.0],
        'Customer_ID': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008'],
        'Order_Date': ['2023-01-15', '2023-01-16', '2023-01-17', '2023-01-18', '2023-01-19', '2023-01-20', '2023-01-21', '2023-01-22'],
        'Region': ['Midwest', 'West', 'East', 'Midwest', 'Midwest', 'West', 'South', 'East']
    }
    
    df = pd.DataFrame(sample_data)
    
    # Test the columns query
    query = 'What are the columns in the dataset?'
    print(f'\n=== Testing: {query} ===')
    print(f'Dataset columns: {list(df.columns)}')
    print(f'Dataset shape: {df.shape}')
    print('')
    
    result = await analyze_question(df, query)
    
    print(f'Final Answer: {result.get("final_answer", "No answer")}')
    print(f'Reasoning: {result.get("reasoning", "No reasoning")}')
    
    if result.get('chart_specification'):
        chart_spec = result['chart_specification']
        print(f'Chart Type: {chart_spec.get("type")}')
        print(f'Title: {chart_spec.get("options", {}).get("plugins", {}).get("title", {}).get("text", "No title")}')
        print(f'Labels: {chart_spec.get("data", {}).get("labels", [])}')
        print(f'Data Points: {len(chart_spec.get("data", {}).get("datasets", [{}])[0].get("data", []))}')
    else:
        print('No chart specification generated (expected for non-chart query)')
    
    # Print the raw response keys for debugging
    print(f'\nRaw response keys: {list(result.keys())}')

if __name__ == "__main__":
    asyncio.run(test_columns_query())
