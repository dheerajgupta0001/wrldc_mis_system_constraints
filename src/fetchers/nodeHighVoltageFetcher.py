import datetime as dt
from src.typeDefs.systemConstraintsSummary import IConstraintSummary
from typing import List
import os
import pandas as pd

def getHighVoltageNodeFilePath(highNodeFolderPath: str) -> str:
    """get the file path of High Voltage Node excel file from an input folder

    Args:
        highNodeFolderPath (str): path of folder to search for

    Returns:
        str: file path of desired excel file that contains High Voltage Node Data
    """
    # sample excel filename - Nodes Experiencing High Voltage.xlsx
    targetFilename = 'Nodes Experiencing High Voltage.xlsx'
    targetFilePath = os.path.join(highNodeFolderPath, targetFilename)

    return targetFilePath

def fetchHighVoltageForDate(targetFilePath: str) -> List[IConstraintSummary]:
    """fetched High Voltage Node data for a quarter
    Args:
        targetFilePath (str): date for which quarter is to be extracted
    Returns:
        List[IConstraintSummary]: list of High Voltage Node records fetched from the excel data
    """
    if isinstance(targetFilePath, str) and not(targetFilePath == ''):
        return []

    # read excel file
    excelDf = pd.read_excel(targetFilePath)
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
    #print(highVoltageRecords)

    return highVoltageRecords