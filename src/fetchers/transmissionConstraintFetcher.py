import datetime as dt
from src.typeDefs.systemConstraintsSummary import IConstraintSummary
from typing import List
import os
import pandas as pd


def fetchTransmissionConstraintForDate(transmissionConstraintFolderPath: str) -> List[IConstraintSummary]:
    """fetched transmission constraint data for a quarter
    Args:
        targetDt (dt.datetime): date for which quarter is to be extracted
    Returns:
        List[IPairAngleSummary]: list of transmission records fetched from the excel data
    """
    # sample excel filename - Transmission Constraints.xlsx
    #fileDateStr = dt.datetime.strftime(targetDt, '%d_%m_%Y')
    targetFilename = 'Transmission Constraints.xlsx'
    targetFilePath = os.path.join(transmissionConstraintFolderPath, targetFilename)
    #print("transmission file :{0}".format(targetFilePath))

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
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