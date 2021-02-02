import pyodbc

class DB_function:

    def __init__(self):
        server = 'dbrestaurantserver.database.windows.net'
        database = 'dbsertaurant'
        username = 'restadmin'
        password = 'Chatbot4'   
        # driver= '{ODBC Driver 17 for SQL Server}'
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        self.cursor = cnxn.cursor()

    def DB_query(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        result = []
        while row:
            result.append(row)
            row = self.cursor.fetchone()
        output = []
        for i in range(len(result)):
            row = result[i]
            for j in range(len(row)):
                output.append(row[j])
        return output

    def DB_insert(self, query):
        # server = 'db-chatbot.database.windows.net'
        # database = 'restaurant_DB'
        # username = 'rest-admin'
        # password = 'Chatbot4'   
        # # driver= '{ODBC Driver 17 for SQL Server}'
        # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        # cursor = cnxn.cursor()
        self.cursor.execute(query)
        return 'OK'
    
    def DB_commit(self):
        # server = 'db-chatbot.database.windows.net'
        # database = 'restaurant_DB'
        # username = 'rest-admin'
        # password = 'Chatbot4'   
        # # driver= '{ODBC Driver 17 for SQL Server}'
        # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        # cursor = cnxn.cursor()
        self.cursor.execute('COMMIT')
