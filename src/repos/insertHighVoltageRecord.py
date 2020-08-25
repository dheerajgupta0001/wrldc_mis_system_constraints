from typing import List, Tuple, TypedDict
import cx_Oracle
from src.typeDefs.systemConstraintsSummary import IConstraintSummary


class Outages(TypedDict):
    columns: List[str]
    rows: List[Tuple]


class HighVoltageSummaryRepo():
    """Repository class for transmission data
    """
    localConStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConf (DbConfig): database connection string
        """
        self.localConStr = dbConStr
        #print(dbConStr)

    def pushHighVoltageRecord(self, highVoltageDataRecords: List[IConstraintSummary]) -> bool:
        """inserts Nodes experiencing high Voltage data into the app db
        Args:
            highVoltageDataRecords (List[IConstraintSummary]): Nodes experiencing high Voltage data to be inserted
        Returns:
            bool: returns true if process is ok
        """
        # get connection with raw data table
        connection= cx_Oracle.connect(self.localConStr)

        isInsertSuccess = True
        if len(highVoltageDataRecords) == 0:
            return isInsertSuccess
        try:
            # keyNames names of the raw data
            keyNames = ['StartDate', 'EndDate', 'corridor', 'seasonAntecedent', 'description']
            colNames = ['START_DATE', 'END_DATE', 'NODES', 'SEASON_ANTECEDENT', 'DESCRIPTION_CONSTRAINTS']
            # get cursor for raw data table
            cursor=connection.cursor()
            print("connection version :{0}".format(connection.version))

            # text for sql place holders
            sqlPlceHldrsTxt = ','.join([':{0}'.format(x+1)
                                        for x in range(len(keyNames))])

            # delete the rows which are already present
            existingHighVoltageData = [(x['StartDate'], x['EndDate'])
                                  for x in highVoltageDataRecords]
            cursor.executemany(
                "delete from mis_warehouse.nodes_high_voltage_data where START_DATE=:1 and END_DATE=:2", existingHighVoltageData)
            
            # insert the raw data
            sql_insert = "insert into mis_warehouse.nodes_high_voltage_data({0}) values ({1})".format(
                ','.join(colNames), sqlPlceHldrsTxt)
            
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            cursor.executemany(sql_insert, [tuple(
                [r[col] for col in keyNames]) for r in highVoltageDataRecords])

            # commit the changes
            connection.commit()
        except Exception as e:
            isInsertSuccess = False
            print('Error while bulk insertion of transmission constraints data into database')
            print(e)
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            
        return isInsertSuccess