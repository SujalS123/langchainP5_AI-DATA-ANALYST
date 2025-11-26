import asyncio
from app.services.dataset_service import get_user_datasets

async def check_datasets():
    datasets = await get_user_datasets('test_user')
    print('Available datasets:')
    for dataset in datasets:
        print(f'  ID: {dataset["_id"]}, Name: {dataset.get("name", "N/A")}, Filename: {dataset["filename"]}')

if __name__ == "__main__":
    asyncio.run(check_datasets())
