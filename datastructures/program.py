from dataclasses import dataclass
from datastructures.intervaltree import IntervalTree
from datastructures.avltree import AVLTree
from typing import Any, Callable, Protocol, TypeVar, Generic, Optional, List, Union, Tuple
import csv

@dataclass(order=True)
class Stock:
    symbol: str
    name: str
    low: int
    high: int
    

class StockManager:
    def __init__(self):
        self._interval_tree = IntervalTree()

        stocks = [
            Stock(
                'GOOGL', 'Alphabet Int.', 173, 213 #example!
            )
        ]
    def stocks_from_csv(self, filepath: str):
        with open(filepath, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:



if __name__ == '__main__':
    the_file = "sample_stock_prices.csv"