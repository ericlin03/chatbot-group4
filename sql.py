import pyodbc

server = 'db-chatbot.database.windows.net'
database = 'restaurant_DB'
username = 'rest-admin'
password = 'Chatbot4'   
# driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

def DB_query(query):
    cursor.execute(query)
    row = cursor.fetchone()
    result = []
    while row:
        result.append(row)
        row = cursor.fetchone()
    output = []
    for i in range(len(result)):
        row = result[i]
        for j in range(len(row)):
            output.append(row[j])
    return output

class DB_function:

    def __init__(self):
        server = 'dbrestaurantserver.database.windows.net'
        database = 'dbsertaurant'
        username = 'restadmin'
        password = 'Chatbot4'   
        # driver= '{ODBC Driver 17 for SQL Server}'
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        self.cursor = cnxn.cursor()

    # def connect_to_DB():
    #     server = 'db-chatbot.database.windows.net'
    #     database = 'restaurant_DB'
    #     username = 'rest-admin'
    #     password = 'Chatbot4'   
    #     # driver= '{ODBC Driver 17 for SQL Server}'
    #     cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    #     cursor = cnxn.cursor()

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

    def DB_insert(query):
        # server = 'db-chatbot.database.windows.net'
        # database = 'restaurant_DB'
        # username = 'rest-admin'
        # password = 'Chatbot4'   
        # # driver= '{ODBC Driver 17 for SQL Server}'
        # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        # cursor = cnxn.cursor()
        cursor.execute(query)

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

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

# #Sample select query 
# cursor.execute("SELECT * FROM user_info") 
# row = cursor.fetchone() 
# while row: 
#     print(row[0], row[1], row[2])
#     row = cursor.fetchone()

# with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT * FROM user_info")
#         row = cursor.fetchone()
#         while row:
#             print (str(row[0]) + " " + str(row[1]))
#             row = cursor.fetchone()
