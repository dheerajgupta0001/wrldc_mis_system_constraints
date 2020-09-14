import datetime as dt
from src.typeDefs.systemConstraintsSummary import IConstraintSummary
from typing import List
import os
import pandas as pd

def getIctConstraintFilePath(ictConstraintFolderPath: str) -> str:
    """get the file path of Ict Constraints excel file from an input folder

    Args:
        ictConstraintFolderPath (str): path of folder to search for

    Returns:
        str: file path of desired excel file that contains ICT Constraints Data
    """
    # sample excel filename - ICT Constraints.xlsx
    targetFilename = 'ICT Constraints.xlsx'
    targetFilePath = os.path.join(ictConstraintFolderPath, targetFilename)

    return targetFilePath


def fetchIctConstraintForDate(targetFilePath: str) -> List[IConstraintSummary]:
    """fetched ict constraint data for a quarter
    Args:
        targetFilePath (str): date for which quarter is to be extracted
    Returns:
        List[IConstraintSummary]: list of ict records fetched from the excel data
    """
    if isinstance(targetFilePath, str) and not(targetFilePath == ''):
        return []

    # read excel file
    excelDf = pd.read_excel(targetFilePath)
    del excelDf['Sl. No']
    # rename columns to suite output requirements
    excelDf.rename(columns={
        "ICT": "corridor",
        "Season/ Antecedent Conditions": "seasonAntecedent",
        "Description of the constraints": 'description'
    }, inplace=True)

    # convert nan to None
    excelDf = excelDf.where(pd.notnull(excelDf), None)

    # convert dataframe to list of dictionaries
    ictRecords = excelDf.to_dict('records')
    #print(ictRecords)
    
    return ictRecords