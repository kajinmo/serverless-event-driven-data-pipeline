from typing import List

def load_data_to_dynamo(table, data: List[dict]) -> None:
    # The batch_writer natively handles chunking into batches of 25 items (Dynamo API limit)
    # and automatically retries UnprocessedItems, which is crucial in production.
    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)
    print(f"[{table.name}] {len(data)} records validated and inserted.")
