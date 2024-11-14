import pandas as pd
import json
import time
import httpx
from httpx import Timeout
from loguru import logger
import requests
from protocol import Page

BASE_URL = "https://api.jamaibase.com/api"


def generate_schema_from_dataset(dataset):
    # Define a mapping for pandas dtypes to your schema types
    dtype_mapping = {
        "int64": "int",
        "float64": "float",
        "object": "string",
        "bool": "bool",
        "datetime64[ns]": "datetime"
    }

    # Generate the schema, excluding any unnamed columns
    schematic = {}
    for col, dtype in dataset.dtypes.items():
        # Exclude unnamed columns (e.g., index column)
        if not col.startswith("Unnamed"):
            # Replace spaces with underscores in the column names
            col_name = col.replace(" ", "_")

            # Check if the column contains only 0's and 1's (Boolean values)
            if set(dataset[col].dropna().unique()) == {0, 1}:
                schematic[col_name] = "bool"  # Treat as boolean
            else:
                schematic[col_name] = dtype_mapping.get(str(dtype), "string")  # Default to string if type is unknown

    return schematic


columns_info = {
    'Clothing_ID': 'int',
    'Age': 'int',
    'Title': 'string',
    'Review_Text': 'string',
    'Rating': 'int',
    'Recommended_IND': 'bool',
    'Positive_Feedback_Count': 'int',
    'Division_Name': 'string',
    'Department_Name': 'string',
    'Class_Name': 'string'
}


class ActionTableCommunicate:
    def __init__(self) -> None:
        self.client = httpx.Client(
            transport=httpx.HTTPTransport(retries=3),
            timeout=Timeout(5 * 60),
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": "Bearer jamai_sk_51cd630a71c10c1d68d56812a9dbcf468c21e01076a3e674",  # replace with your actual API token
                "X-PROJECT-ID": "proj_7bcb34f8831154cb0657c396",  # replace with your actual Project ID
            }
        )

    def create_table(self, table_id: str, cols_info: dict[str, str] = None,):
        schema = {
            "id": table_id,
            "cols": cols_info,
        }
        response = self.client.post(f"https://api.jamaibase.com/api/v1/gen_tables/action", json=schema)
        response.raise_for_status()


x = ActionTableCommunicate()
x.create_table('TEST_TABLE', columns_info)



