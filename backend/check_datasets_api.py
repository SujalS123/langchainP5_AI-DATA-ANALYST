import asyncio
import aiohttp

async def check_datasets_api():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8000/files/list') as response:
                if response.status == 200:
                    data = await response.json()
                    print('Available datasets:')
                    if data.get('datasets'):
                        for dataset in data['datasets']:
                            print(f'  ID: {dataset["_id"]}, Filename: {dataset["filename"]}')
                    else:
                        print('  No datasets found')
                else:
                    print(f'Error: {response.status}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    asyncio.run(check_datasets_api())
