import asyncio
import aiohttp
import json
from pathlib import Path

async def test_analyze_api():
    """Test the complete analyze API flow"""
    base_url = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        print("🧪 Testing Complete Analyze API Flow")
        print("=" * 50)
        
        # Step 1: Upload a sample dataset
        print("\n📤 Step 1: Uploading sample dataset...")
        
        csv_file_path = Path("sample_sales_data.csv")
        if not csv_file_path.exists():
            print("❌ sample_sales_data.csv not found!")
            return
        
        # Read the CSV file
        with open(csv_file_path, 'rb') as f:
            csv_data = f.read()
        
        # Upload the file
        upload_data = aiohttp.FormData()
        upload_data.add_field('file', csv_data, 
                             filename='sample_sales_data.csv', 
                             content_type='text/csv')
        
        try:
            async with session.post(f"{base_url}/files/upload", data=upload_data) as upload_response:
                if upload_response.status == 200:
                    upload_result = await upload_response.json()
                    dataset_id = upload_result.get('dataset_id')
                    print(f"✅ Dataset uploaded successfully!")
                    print(f"   Dataset ID: {dataset_id}")
                    print(f"   Filename: {upload_result.get('filename')}")
                else:
                    print(f"❌ Upload failed: {upload_response.status}")
                    upload_error = await upload_response.text()
                    print(f"   Error: {upload_error}")
                    return
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return
        
        # Step 2: Test the analyze endpoint with various queries
        print("\n🔍 Step 2: Testing analyze endpoint...")
        
        test_queries = [
            "Show me a bar chart of sales by region",
            "What is the total profit by state?", 
            "Create a pie chart showing profit distribution across regions",
            "Which states have the highest sales?",
            "Compare profit vs sales in a scatter plot"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n   Test {i}: {query}")
            
            analyze_payload = {
                "dataset_id": dataset_id,
                "query": query
            }
            
            try:
                async with session.post(
                    f"{base_url}/api/analyze", 
                    params={"dataset_id": dataset_id, "question": query}
                ) as analyze_response:
                    
                    if analyze_response.status == 200:
                        result = await analyze_response.json()
                        print(f"   ✅ Success!")
                        
                        # Check response structure
                        if 'text' in result:
                            print(f"   📝 Text: {result['text'][:100]}...")
                        
                        if 'chart' in result:
                            chart_data = result['chart']
                            print(f"   📊 Chart generated: {chart_data.get('type', 'unknown')}")
                            if 'data' in chart_data:
                                print(f"   📈 Data points: {len(chart_data['data'])}")
                        
                        if 'metadata' in result:
                            print(f"   🏷️  Metadata: {result['metadata']}")
                            
                    else:
                        print(f"   ❌ Failed: {analyze_response.status}")
                        error_text = await analyze_response.text()
                        print(f"   Error: {error_text}")
                        
            except Exception as e:
                print(f"   ❌ Request error: {e}")
        
        # Step 3: Test error cases
        print("\n🚨 Step 3: Testing error cases...")
        
        # Test with invalid dataset ID
        print("\n   Testing invalid dataset ID...")
        try:
            async with session.post(
                f"{base_url}/api/analyze",
                params={"dataset_id": "invalid_id", "question": "Show me sales"}
            ) as error_response:
                print(f"   Status: {error_response.status}")
                if error_response.status != 200:
                    error_data = await error_response.json()
                    print(f"   ✅ Expected error: {error_data.get('detail', 'Unknown error')}")
                else:
                    print("   ⚠️  Unexpected success")
        except Exception as e:
            print(f"   ❌ Error test failed: {e}")
        
        # Test with missing query
        print("\n   Testing missing parameters...")
        try:
            async with session.post(
                f"{base_url}/api/analyze"
            ) as error_response:
                print(f"   Status: {error_response.status}")
                if error_response.status != 200:
                    error_data = await error_response.json()
                    print(f"   ✅ Expected error: {error_data.get('detail', 'Unknown error')}")
                else:
                    print("   ⚠️  Unexpected success")
        except Exception as e:
            print(f"   ❌ Error test failed: {e}")
        
        print("\n🎉 API testing completed!")

if __name__ == "__main__":
    print("🚀 Starting Analyze API Tests...")
    print("Make sure the backend server is running on http://localhost:8000")
    asyncio.run(test_analyze_api())
