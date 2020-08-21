import datetime as dt
from src.typeDefs.systemConstraintsSummary import IConstraintSummary
from typing import List
import os
import pandas as pd


def fetchHighVoltageForDate(HighNodeFolderPath: str, targetDt: dt.datetime) -> List[IConstraintSummary]:
    """fetched transmission constraint data for a quarter
    Args:
        targetDt (dt.datetime): date for which quarter is to be extracted
    Returns:
        List[IPairAngleSummary]: list of transmission records fetched from the excel data
    """
    # sample excel filename - ANGLES__05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d_%m_%Y')
    targetFilename = 'NodesExperiencingHighVoltage__{0}.xlsx'.format(fileDateStr)
    targetFilePath = os.path.join(HighNodeFolderPath, targetFilename)

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
        return []

    # read excel file
    excelDf = pd.read_excel(targetFilePath)
    excelDf['dateDate']=targetDt
    del excelDf['Sl. No']

    # rename columns to suite output requirements
    excelDf.rename(columns={
        "Nodes": "corridor",
        "Season/ Antecedent Conditions": "seasonAntecedent",
        "Description of the Constraints": 'description'
    }, inplace=True)

    # convert nan to None
    excelDf = excelDf.where(pd.notnull(excelDf), None)

    # convert dataframe to list of dictionaries
    highVoltageRecords = excelDf.to_dict('records')

    return highVoltageRecords