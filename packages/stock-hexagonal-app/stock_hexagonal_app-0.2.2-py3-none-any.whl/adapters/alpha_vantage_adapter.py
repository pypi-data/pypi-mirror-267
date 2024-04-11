import requests
import pandas
import io

from ports.stock_data_provider import StockDataProvider


class AlphaVantage(StockDataProvider):
    def __init__(
        self,
        auth_token: str,
        company_symbol: str | None = None,
        time_interval: str | None = None,
        company_data: pandas.DataFrame | None = None,
    ):
        self.auth_token = auth_token
        self.company_symbol = company_symbol
        self.time_interval = time_interval
        self.company_data = company_data

    def _prepare_search_result_data(self, data: dict) -> list[dict]:
        search_result: list[dict] = data["bestMatches"]
        return search_result

    def _prepare_data(self, data: bytes) -> pandas.DataFrame:
        data_str: str = data.decode()
        data_file: io.StringIO = io.StringIO(data_str)
        prepared_data: pandas.DataFrame = pandas.read_csv(data_file)
        return prepared_data

    def search_for_company(self, search_phrase: str) -> list[dict]:
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={search_phrase}&apikey={self.auth_token}"
        res: requests.models.Response = requests.get(url, timeout=10)
        data: dict = res.json()
        search_result: list[dict] = self._prepare_search_result_data(data)
        return search_result

    def get_company_data(self) -> pandas.DataFrame:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.company_symbol}&apikey={self.auth_token}&datatype=csv"
        res: requests.models.Response = requests.get(url, timeout=10)
        data_bytes: bytes = res.content
        prepared_data = self._prepare_data(data_bytes)
        return prepared_data
