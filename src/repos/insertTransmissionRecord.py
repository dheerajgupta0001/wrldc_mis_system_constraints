from typing import List, Tuple, TypedDict
import cx_Oracle
from src.typeDefs.systemConstraintsSummary import IConstraintSummary


class Outages(TypedDict):
    columns: List[str]
    rows: List[Tuple]


class TransmissionSummaryRepo():
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

    def pushTransmissionRecord(self, transmissionDataRecords: List[IConstraintSummary]) -> bool:
        """inserts angles date of station pairs into the app db
        Args:
            transmissionDataRecords (List[IConstraintSummary]): daywise angle data to be inserted
        Returns:
            bool: returns true if process is ok
        """
        # get connection with raw data table
        connection= cx_Oracle.connect(self.localConStr)

        isInsertSuccess = True
        if len(transmissionDataRecords) == 0:
            return isInsertSuccess
        try:
            # keyNames names of the raw data
            keyNames = ['corridor', 'seasonAntecedent', 'description', 'dataDate']
            colNames = ['CORRIDOR', 'SEASON_ANTECEDENT', 'DESCRIPTION_CONSTRAINTS','DATA_DATE']
            # get cursor for raw data table
            cursor=connection.cursor()
            print("connection version :{0}".format(connection.version))

            # text for sql place holders
            sqlPlceHldrsTxt = ','.join([':{0}'.format(x+1)
                                        for x in range(len(keyNames))])

            # delete the rows which are already present
            existingTransmissionData = [(x['dataDate'])
                                  for x in transmissionDataRecords]
            #print(transmissionDataRecords)
            cursor.executemany(
                "delete from mis_warehouse.transmission_constraint_data where DATA_DATE=:1", existingTransmissionData)

            # insert the raw data
            sql_insert = "insert into mis_warehouse.transmission_constraint_data({0}) values ({1})".format(
                ','.join(colNames), sqlPlceHldrsTxt)
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            cursor.executemany(sql_insert, [tuple(
                [r[col] for col in keyNames]) for r in transmissionDataRecords])

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