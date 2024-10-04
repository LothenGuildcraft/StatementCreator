import oracledb
from DatabaseConnection.Credentials import Credentials
#from Credentials import Credentials

class Connect:
    def __init__(self):
        oracledb.init_oracle_client(lib_dir='DatabaseConnection/Dependencies/instantclient_21_14')
        #Remove the old dependency instantclient from the Dependency folder
        
        credentials = Credentials()

        #Initial Login Screen
        credentials.popupmsg()

        #Connects to the database
        self.connection = oracledb.connect(user=credentials.user, password=credentials.password, dsn=credentials.dsn)
        self.cursor = self.connection.cursor()
    
    def runQuery(self, sql):
        r = self.cursor.execute(sql)
        rows = r.fetchall()
        return rows
    
    def isConnectionOpen(self):
        try:
            return self.connection.ping() is None
        except:
            return False
    
    def closingConnection(self):
        self.cursor.close()
        self.connection.close()