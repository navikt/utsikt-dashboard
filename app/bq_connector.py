from dataclasses import dataclass, field
from typing import Any

from google.cloud import bigquery

@dataclass
class BigQueryConnector:
    client: bigquery.Client = field(init=False)


    def __post_init__(self):
        self.client = bigquery.Client()

    def get_rows(self, query) -> list[dict[str, Any]]:
        query_job = self.client.query(query=query)
        results = query_job.result()
        return [{key:value for key, value in row.items()} for row in results]
