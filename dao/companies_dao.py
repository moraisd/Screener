from pymongo.database import Database

from util.constants import symbol_exists_filter, return_tickers_only


class CompaniesDao:

    def __init__(self, database: Database):
        self.database = database

    def insert_one(self, data) -> None:
        self.database['companies'].insert_one(data)

    def insert_tickers(self, tickers: set) -> None:
        self.database['companies'].insert_many([{'Symbol': ticker} for ticker in tickers])

    def update_one(self, ticker, data) -> None:
        self.database['companies'].update_one({'Symbol': ticker}, {"$set": data})

    def find_one(self, ticker) -> dict:
        return self.database['companies'].find_one({'Symbol': ticker})

    def find_all_tickers(self) -> set:
        return {field.get('Symbol') for field in
                self.database['companies'].find(symbol_exists_filter, return_tickers_only)}

    def delete_delisted(self, delisted_tickers: set) -> None:
        self.database['companies'].delete_many({'Symbol': {'$in': list(delisted_tickers)}})
