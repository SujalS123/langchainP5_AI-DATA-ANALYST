import asyncio
import pandas as pd
import sys
import os

# Add the app directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.agent_service import analyze_question

async def test_chart_generation():
    # Load the sample data
    df = pd.read_csv('sample_sales_data.csv')
    print("Dataset loaded successfully!")
    print(f"Columns: {list(df.columns)}")
    print(f"Data shape: {df.shape}")
    print("\nSample data:")
    print(df.head())
    
    # Test question that should generate a chart
    question = "Show me the most profitable states"
    print(f"\nTesting question: '{question}'")
    
    try:
        result = await analyze_question(df, question)
        print("\nResult:")
        print(f"Final Answer: {result.get('final_answer', 'No answer')}")
        print(f"Chart Image: {'Found' if result.get('chart_image') else 'Not found'}")
        
        if result.get('chart_image'):
            print(f"Chart image length: {len(result['chart_image'])} characters")
            print("Chart generation SUCCESSFUL! ✅")
        else:
            print("Chart generation FAILED! ❌")
            
        if result.get('error'):
            print(f"Error: {result['error']}")
            
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chart_generation())
