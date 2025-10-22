import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from app.services.agent_service import analyze_question

async def test_chart_extraction():
    # Create sample data similar to what's in the database
    sample_data = {
        'State': ['Indiana', 'Washington', 'Delaware', 'Michigan', 'Minnesota', 'California', 'Texas', 'New York'],
        'Profit': [8399.976, 6719.9808, 5039.9856, 4946.37, 4630.4755, 4000.0, 3500.0, 3000.0],
        'Sales': [15000.0, 12000.0, 9000.0, 8500.0, 8000.0, 7500.0, 7000.0, 6500.0]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Test the chart generation
    question = "Show me the top 5 states by profit"
    result = await analyze_question(df, question)
    
    print("=== CHART EXTRACTION TEST ===")
    print(f"Question: {question}")
    print(f"Final Answer: {result.get('final_answer', 'N/A')}")
    print(f"Chart Specification: {result.get('chart_specification', 'N/A')}")
    
    if result.get('chart_specification'):
        print("✅ SUCCESS: Chart specification extracted!")
        chart_spec = result['chart_specification']
        if isinstance(chart_spec, dict):
            print(f"Chart Type: {chart_spec.get('type', 'N/A')}")
            print(f"Labels: {chart_spec.get('data', {}).get('labels', 'N/A')}")
            print(f"Data Points: {len(chart_spec.get('data', {}).get('datasets', [{}])[0].get('data', []))}")
    else:
        print("❌ FAILED: No chart specification found")
    
    print("\n=== FULL RESPONSE ===")
    import json
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(test_chart_extraction())
