'''
This is the web server that acts as a service that creates raw/derived data of voltage and frequency
'''
import datetime as dt
from flask import Flask, request, jsonify
from src.config.appConfig import getConfig
from src.fetchers.transmissionConstraintFetcher import fetchTransmissionConstraintForDate
from src.fetchers.ictConstraintFetcher import fetchIctConstraintForDate
from src.fetchers.nodeHighVoltageFetcher import fetchHighVoltageForDate
from src.fetchers.nodeLowVoltageFetcher import fetchLowVoltageForDate
from src.repos.insertTransmissionRecord import TransmissionSummaryRepo
from src.repos.insertIctRecord import IctSummaryRepo
from src.repos.insertHighVoltageRecord import HighVoltageSummaryRepo
from src.repos.insertLowVoltageRecord import LowVoltageSummaryRepo
from src.typeDefs.systemConstraintsSummary import IConstraintSummary

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

appDbConnStr = appConfig['appDbConStr']


@app.route('/')
def hello():
    return "This is the web service that acts as a service that creates system constraints messages"


@app.route('/transmission_constraints', methods=['POST'])
def transmissionConstraints():
    try:
        reqFile = request.files.get('inpFile')
        transmissionConstraintsData = fetchTransmissionConstraintForDate(reqFile)

        # get the instance of Transmission repository
        transmisssionDataRepo = TransmissionSummaryRepo(appDbConnStr)
        # pushing Transmission constraints Data to database
        isInsSuccess = transmisssionDataRepo.pushTransmissionRecord(transmissionConstraintsData)
        if isInsSuccess:
            return jsonify({'message': 'Transmission Constraints Data insertion successful!!!'})
    except Exception as ex:
        return jsonify({'message': 'some error occured...'}), 400
    return jsonify({'message': 'some error occured...'}), 400


@app.route('/createIctConstraints', methods=['POST'])
def ictConstraints():
    try:
        reqFile = request.files.get('inpFile')
        ictConstraintsData = fetchIctConstraintForDate(reqFile)

        # get the instance of Transmission repository
        ictDataRepo = IctSummaryRepo(appDbConnStr)
        # pushing Transmission constraints Data to database
        isInsSuccess = ictDataRepo.pushIctRecord(ictConstraintsData)
        if isInsSuccess:
            return jsonify({'message': 'Ict Constraints Data insertion successful!!!'})
    except Exception as ex:
        return jsonify({'message': 'some error occured...'}), 400
    return jsonify({'message': 'some error occured...'}), 400


@app.route('/highVoltageNode', methods=['POST'])
def highVoltageNode():
    try:
        reqFile = request.files.get('inpFile')
        highVoltageNodeData = fetchHighVoltageForDate(reqFile)

        # get the instance of Transmission repository
        highVoltageDataRepo = HighVoltageSummaryRepo(appDbConnStr)
        # pushing Transmission constraints Data to database
        isInsSuccess = highVoltageDataRepo.pushHighVoltageRecord(highVoltageNodeData)
        if isInsSuccess:
            return jsonify({'message': 'Nodes experiencing high Voltage data insertion successful!!!'})
    except Exception as ex:
        return jsonify({'message': 'some error occured...'}), 400
    return jsonify({'message': 'some error occured...'}), 400


@app.route('/lowVoltageNode', methods=['POST'])
def lowVoltageNode():
    try:
        reqFile = request.files.get('inpFile')
        lowVoltageNodeData = fetchLowVoltageForDate(reqFile)

        # get the instance of Transmission repository
        lowVoltageDataRepo = LowVoltageSummaryRepo(appDbConnStr)
        # pushing Transmission constraints Data to database
        isInsSuccess = lowVoltageDataRepo.pushLowVoltageRecord(lowVoltageNodeData)
        if isInsSuccess:
            return jsonify({'message': 'Nodes experiencing low Voltage data insertion successful!!!'})
    except Exception as ex:
        return jsonify({'message': 'some error occured...'}), 400
    return jsonify({'message': 'some error occured...'}), 400


if __name__ == '__main__':
    app.run(debug=True)