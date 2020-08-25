import datetime as dt
from src.typeDefs.systemConstraintsSummary import IConstraintSummary
from typing import List
import os
import pandas as pd


def fetchLowVoltageForDate(LowNodeFolderPath: str) -> List[IConstraintSummary]:
    """fetched transmission constraint data for a quarter
    Args:
        targetDt (dt.datetime): date for which quarter is to be extracted
    Returns:
        List[IPairAngleSummary]: list of transmission records fetched from the excel data
    """
    # sample excel filename - Nodes Experiencing Low Voltage.xlsx
    targetFilename = 'Nodes Experiencing Low Voltage.xlsx'
    targetFilePath = os.path.join(LowNodeFolderPath, targetFilename)

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
        return []

    # read excel file
    excelDf = pd.read_excel(targetFilePath)
    del excelDf['Sl. No']
    
    # rename columns to suite output requirements
    excelDf.rename(columns={
        "Nodes": "corridor",
        "Season/ Antecedent Conditions": "seasonAntecedent",
        "Description of the constraints": 'description'
    }, inplace=True)

    # convert nan to None
    excelDf = excelDf.where(pd.notnull(excelDf), None)

    # convert dataframe to list of dictionaries
    lowVoltageRecords = excelDf.to_dict('records')
    #print(lowVoltageRecords)

    return lowVoltageRecords