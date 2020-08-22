import datetime as dt
from src.typeDefs.systemConstraintsSummary import IConstraintSummary
from typing import List
import os
import pandas as pd


def fetchLowVoltageForDate(LowNodeFolderPath: str, targetDt: dt.datetime) -> List[IConstraintSummary]:
    """fetched transmission constraint data for a quarter
    Args:
        targetDt (dt.datetime): date for which quarter is to be extracted
    Returns:
        List[IPairAngleSummary]: list of transmission records fetched from the excel data
    """
    # sample excel filename - ANGLES__05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d_%m_%Y')
    targetFilename = 'NodesExperiencingLowVoltage__{0}.xlsx'.format(fileDateStr)
    targetFilePath = os.path.join(LowNodeFolderPath, targetFilename)

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
        return []

    # read excel file
    excelDf = pd.read_excel(targetFilePath)
    excelDf['dataDate']=targetDt
    del excelDf['Sl. No']
    #print(excelDf)
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

    return lowVoltageRecords