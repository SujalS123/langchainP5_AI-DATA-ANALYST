import asyncio
import aiohttp
import os

async def upload_sample_dataset():
    """Upload the sample sales dataset"""
    url = "http://localhost:8000/files/upload"
    
    # Check if the file exists
    file_path = "sample_sales_data.csv"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return
    
    async with aiohttp.ClientSession() as session:
        # Create form data
        data = aiohttp.FormData()
        data.add_field('file', open(file_path, 'rb'), filename='sample_sales_data.csv', content_type='text/csv')
        data.add_field('name', 'Sample Sales Data')
        data.add_field('user_id', 'test_user')
        
        try:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"Upload successful!")
                    print(f"Dataset ID: {result.get('dataset_id')}")
                    print(f"Filename: {result.get('filename')}")
                else:
                    error_text = await response.text()
                    print(f"Upload failed with status {response.status}: {error_text}")
        except Exception as e:
            print(f"Error uploading file: {e}")

if __name__ == "__main__":
    asyncio.run(upload_sample_dataset())
