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

# get an instance of argument parser from argparse module
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

# get application config inn the form of dictionary
appConfig = getConfig()
print(appConfig)
# create outages raw data between start and end dates
systemConstraintFolderPath = appConfig['systemConstraintFolderPath']
appDbConnStr = appConfig['appDbConStr']

# transmission constraints data fetcher
transmissionData= fetchTransmissionConstraintForDate(systemConstraintFolderPath, startDate)
print(type(transmissionData))

# ict constraints data fetcher
ictData= fetchICTconstraintForDate(systemConstraintFolderPath, startDate)

# node experiencing high voltage data fetcher
highVoltageData= fetchHighVoltageForDate(systemConstraintFolderPath, startDate)

# node experiencing high voltage data fetcher
lowVoltageData= fetchLowVoltageForDate(systemConstraintFolderPath, startDate)
