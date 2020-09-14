import datetime as dt
from src.typeDefs.systemConstraintsSummary import IConstraintSummary
from typing import List
import os
import pandas as pd

def getTransmissionConstraintFilePath(transmissionConstraintFolderPath: str) -> str:
    """get the file path of Transmission Constraints excel file from an input folder

    Args:
        transmissionConstraintFolderPath (str): path of folder to search for

    Returns:
        str: file path of desired excel file that contains Transmission Constraints Data
    """
    # sample excel filename - Transmission Constraints.xlsx
    targetFilename = 'Transmission Constraints.xlsx'
    targetFilePath = os.path.join(transmissionConstraintFolderPath, targetFilename)
    '''# check if excel file is present
    if not os.path.isfile(targetFilePath):
        return []'''

    return targetFilePath


def fetchTransmissionConstraintForDate(targetFilePath: str) -> List[IConstraintSummary]:
    """fetched transmission constraint data for a quarter
    Args:
        targetFilePath (str): date for which quarter is to be extracted
    Returns:
        List[transmissionRecords]: list of transmission records fetched from the excel data
    """
    
    if isinstance(targetFilePath, str) and not(targetFilePath == ''):
        return []

    # read excel file
    excelDf = pd.read_excel(targetFilePath)
    del excelDf['Sl. No']

    # rename columns to suite output requirements
    excelDf.rename(columns={
        "Corridor": "corridor",
        "Season/ Antecedent Conditions": "seasonAntecedent",
        "Description of the constraints": 'description'
    }, inplace=True)

    # convert nan to None
    excelDf = excelDf.where(pd.notnull(excelDf), None)

    # convert dataframe to list of dictionaries
    transmissionRecords = excelDf.to_dict('records')
    #print(transmissionRecords)

    return transmissionRecords