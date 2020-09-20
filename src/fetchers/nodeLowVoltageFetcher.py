import datetime as dt
from src.typeDefs.systemConstraintsSummary import IConstraintSummary
from typing import List
import os
import pandas as pd

def getLowVoltageNodeFilePath(lowNodeFolderPath: str) -> str:
    """get the file path of Low Voltage Node excel file from an input folder

    Args:
        lowNodeFolderPath (str): path of folder to search for

    Returns:
        str: file path of desired excel file that contains Low Voltage Node Data
    """
    # sample excel filename - Nodes Experiencing Low Voltage.xlsx
    targetFilename = 'Nodes Experiencing Low Voltage.xlsx'
    targetFilePath = os.path.join(lowNodeFolderPath, targetFilename)

    return targetFilePath

def fetchLowVoltageForDate(targetFilePath: str) -> List[IConstraintSummary]:
    """fetched Low Voltage Node data for a quarter
    Args:
        targetFilePath (str): date for which quarter is to be extracted
    Returns:
        List[IConstraintSummary]: list of Low Voltage Node records fetched from the excel data
    """
    if isinstance(targetFilePath, str) and (targetFilePath == ''):
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