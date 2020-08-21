from typing import TypedDict
import datetime as dt


class IConstraintSummary(TypedDict):
    dataDate: dt.datetime
    corridor: str
    seasonAntecedent: str
    description: str