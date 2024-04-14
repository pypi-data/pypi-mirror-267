from collections import OrderedDict
from typing import Self
import polars as pl
from polars import DataType
from ..schedule import Schedule


class MarketData(pl.DataFrame):

	@staticmethod
	def _validate_schema(schema: OrderedDict[str, DataType]) -> None:
		required_cols = {
			'stock': pl.Categorical, 'date': pl.Date, 'time': pl.Time,
			'mid': pl.Float64, 'trade': pl.Int32
		}
		for col, type_ in required_cols.items():
			assert schema.pop(col) == type_, f'Column {col} should be of type {type_}'
		assert len(schema) == 0, f'Extra columns found: {list(schema.keys())}'

	@staticmethod
	def _enforce_schedule(df: pl.DataFrame, schedule: Schedule) -> pl.DataFrame:
		...

	def validate_schedule(self): ...

	def __new__(cls, df: pl.DataFrame, schedule: Schedule) -> Self:
		MarketData._validate_schema(df.schema)
		df = MarketData._enforce_schedule(df, schedule)
		return super().__new__(cls, df)