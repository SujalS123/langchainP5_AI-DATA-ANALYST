import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from app.services.agent_service import analyze_question

async def test_different_queries():
    # Create sample data
    sample_data = {
        'State': ['Indiana', 'Washington', 'Delaware', 'Michigan', 'Minnesota', 'California', 'Texas', 'New York'],
        'Profit': [8399.976, 6719.9808, 5039.9856, 4946.37, 4630.4755, 4000.0, 3500.0, 3000.0],
        'Sales': [15000.0, 12000.0, 9000.0, 8500.0, 8000.0, 7500.0, 7000.0, 6500.0]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Test different queries
    queries = [
        'Show me the top 3 states by profit by pie chart',
        'Show me the top 5 states by profit',
        'Create a bar chart of sales by state'
    ]
    
    for query in queries:
        print(f'\n=== Testing: {query} ===')
        result = await analyze_question(df, query)
        if result.get('chart_specification'):
            chart_spec = result['chart_specification']
            print(f'Chart Type: {chart_spec.get("type")}')
            print(f'Title: {chart_spec.get("options", {}).get("plugins", {}).get("title", {}).get("text", "No title")}')
            print(f'Labels: {chart_spec.get("data", {}).get("labels", [])}')
            print(f'Data Points: {len(chart_spec.get("data", {}).get("datasets", [{}])[0].get("data", []))}')
        else:
            print('No chart specification found')

if __name__ == "__main__":
    asyncio.run(test_different_queries())
