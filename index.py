'''
This script creates the data mart for system constraints data in weekly report
## Steps
* read data from excel files
* transform it to fit the local raw data table and push into it
'''

import argparse
import datetime as dt
from src.config.appConfig import getConfig
from src.fetchers.transmissionConstraintFetcher import fetchTransmissionConstraintForDate
from src.fetchers.ictConstraintFetcher import fetchICTconstraintForDate
from src.fetchers.nodeHighVoltageFetcher import fetchHighVoltageForDate
from src.fetchers.nodeLowVoltageFetcher import fetchLowVoltageForDate
from src.repos.insertTransmissionRecord import TransmissionSummaryRepo
from src.repos.insertIctRecord import IctSummaryRepo
from src.repos.insertHighVoltageRecord import HighVoltageSummaryRepo
from src.repos.insertLowVoltageRecord import LowVoltageSummaryRepo

'''# get an instance of argument parser from argparse module
parser = argparse.ArgumentParser()

# get start date from command line
startDate = dt.datetime.now()
parser.add_argument('--start_date', help="Enter Start date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(startDate, '%Y-%m-%d'))
# get the dictionary of command line inputs entered by the user
args = parser.parse_args()

# access each command line input from the dictionary

startDate = dt.datetime.strptime(args.start_date, '%Y-%m-%d')
print(type(startDate))
'''
# get application config inn the form of dictionary
appConfig = getConfig()
print(appConfig)
# create outages raw data between start and end dates
systemConstraintFolderPath = appConfig['systemConstraintFolderPath']
appDbConnStr = appConfig['appDbConStr']

# transmission constraints data fetcher
transmissionData= fetchTransmissionConstraintForDate(systemConstraintFolderPath)
#print(type(transmissionData))

# ict constraints data fetcher
ictData= fetchICTconstraintForDate(systemConstraintFolderPath)

# node experiencing high voltage data fetcher
highVoltageData= fetchHighVoltageForDate(systemConstraintFolderPath)

# node experiencing high voltage data fetcher
lowVoltageData= fetchLowVoltageForDate(systemConstraintFolderPath)


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
 