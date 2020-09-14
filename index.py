'''
This script creates the data mart for system constraints data in weekly report
## Steps
* read data from excel files
* transform it to fit the local raw data table and push into it
'''

import argparse
import datetime as dt
from src.config.appConfig import getConfig
from src.fetchers.transmissionConstraintFetcher import fetchTransmissionConstraintForDate, getTransmissionConstraintFilePath
from src.fetchers.ictConstraintFetcher import fetchIctConstraintForDate, getIctConstraintFilePath
from src.fetchers.nodeHighVoltageFetcher import fetchHighVoltageForDate, getHighVoltageNodeFilePath
from src.fetchers.nodeLowVoltageFetcher import fetchLowVoltageForDate, getLowVoltageNodeFilePath
from src.repos.insertTransmissionRecord import TransmissionSummaryRepo
from src.repos.insertIctRecord import IctSummaryRepo
from src.repos.insertHighVoltageRecord import HighVoltageSummaryRepo
from src.repos.insertLowVoltageRecord import LowVoltageSummaryRepo

# get application config inn the form of dictionary
appConfig = getConfig()
# print(appConfig)

systemConstraintFolderPath = appConfig['systemConstraintFolderPath']
appDbConnStr = appConfig['appDbConStr']

# transmission constraints data fetcher
transmissionConstraintsFilePath = getTransmissionConstraintFilePath(systemConstraintFolderPath)
transmissionData = fetchTransmissionConstraintForDate(transmissionConstraintsFilePath)
# print(type(transmissionData))

# ict constraints data fetcher
ictConstraintsFilePath = getIctConstraintFilePath(systemConstraintFolderPath)
ictData = fetchIctConstraintForDate(ictConstraintsFilePath)

# node experiencing high voltage data fetcher
highVoltageFilePath = getHighVoltageNodeFilePath(systemConstraintFolderPath)
highVoltageData = fetchHighVoltageForDate(highVoltageFilePath)

# node experiencing high voltage data fetcher
lowVoltageFilePath = getLowVoltageNodeFilePath(systemConstraintFolderPath)
lowVoltageData = fetchLowVoltageForDate(lowVoltageFilePath)


# get the instance of Transmission repository
transmisssionDataRepo = TransmissionSummaryRepo(appDbConnStr)
# pushing Transmission constraints Data to database
isInsSuccess = transmisssionDataRepo.pushTransmissionRecord(transmissionData)
if isInsSuccess:
    print("transmission constraints data insertion successful")
else:
    print("transmission constraints data insertion UNsuccessful")

# get the instance of ICT repository
ictDataRepo = IctSummaryRepo(appDbConnStr)
# pushing ICT constraints Data to database
isInsSuccess = ictDataRepo.pushIctRecord(ictData)
if isInsSuccess:
    print("ict constraints data insertion successful")
else:
    print("ict constraints data insertion UNsuccessful")

# get the instance of Nodes experiencing High Voltage repository
highVoltageDataRepo = HighVoltageSummaryRepo(appDbConnStr)
# pushing Nodes experiencing High Voltage Data to database
isInsSuccess = highVoltageDataRepo.pushHighVoltageRecord(highVoltageData)
if isInsSuccess:
    print("Nodes experiencing high Voltage data insertion successful")
else:
    print("Nodes experiencing high Voltage data insertion UNsuccessful")

# get the instance of Nodes experiencing LOW Voltage repository
lowVoltageDataRepo = LowVoltageSummaryRepo(appDbConnStr)
# pushing Nodes experiencing LOW Voltage Data to database
isInsSuccess = lowVoltageDataRepo.pushLowVoltageRecord(lowVoltageData)
if isInsSuccess:
    print("Nodes experiencing low Voltage data insertion successful")
else:
    print("Nodes experiencing low Voltage data insertion UNsuccessful")
