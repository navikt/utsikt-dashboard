from dataclasses import dataclass, field

import pandas as pd

@dataclass
class Table:
    name: str
    path_to_query: str
    data: pd.DataFrame
    query: str = field(init=False)

    def __post_init__(self):
        self.query = self._load_query()

    def _load_query(self) -> str:
        with open(self.path_to_query) as file:
            query = file.read()
        return query

    def fetch_data(self, bq_client) -> pd.DataFrame:
        pass

@dataclass
class Data:
    fagomrade: Table
    faggruppe: Table
    ventestatus: Table


    def reload_data(self, bq_client) -> None:
        self.fagomrade.fetch_data(bq_client=bq_client)
        self.faggruppe.fetch_data(bq_client=bq_client)
        self.ventestatus.fetch_data(bq_client=bq_client)