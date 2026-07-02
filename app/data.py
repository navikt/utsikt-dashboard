from dataclasses import dataclass, field

import pandas as pd

from bq_connector import BigQueryConnector


@dataclass
class Table:
    path_to_query: str
    google_project_id: str
    extra_placeholders: dict = field(default_factory=dict)
    dataframe: pd.DataFrame = field(init=False)
    query: str = field(init=False)
    google_project_id_placeholder: str = field(init=False)

    def __post_init__(self):
        self.google_project_id_placeholder = "<GOOGLE_CLOUD_PROJECT>"
        self.query = self._load_query()

    def _load_query(self) -> str:
        """
        Leser .sql fil og laster som str.
        """
        with open(self.path_to_query) as file:
            query = file.read()

        query = query.replace(
            self.google_project_id_placeholder, self.google_project_id
        )
        for placeholder, value in self.extra_placeholders.items():
            query = query.replace(placeholder, value)
        return query

    def fetch_data(
        self, bq_connector: BigQueryConnector, query_parameters: list | None = None
    ) -> None:
        self.dataframe = pd.DataFrame(
            data=bq_connector.get_rows(
                query=self.query, query_parameters=query_parameters
            )
        )
