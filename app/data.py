from dataclasses import dataclass, field

import pandas as pd

from bq_connector import BigQueryConnector


@dataclass
class Table:
    path_to_query: str
    dataframe: pd.DataFrame = field(init=False)
    query: str = field(init=False)

    def __post_init__(self):
        self.query = self._load_query()

    def _load_query(self) -> str:
        with open(self.path_to_query) as file:
            query = file.read()
        return query

    def fetch_data(self, bq_connector: BigQueryConnector) -> None:
        self.dataframe = pd.DataFrame(data=bq_connector.get_rows(query=self.query))


