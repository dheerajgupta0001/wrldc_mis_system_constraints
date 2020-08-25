from typing import TypedDict
import datetime as dt


class IConstraintSummary(TypedDict):
    StartDate: dt.datetime
    EndDate: dt.datetime
    corridor: str
    seasonAntecedent: str
    description: str