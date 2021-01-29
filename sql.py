import pyodbc
import sys
import traceback

<<<<<<< HEAD
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
=======
class DB_function:

    def __init__(self):
        server = 'db-chatbot.database.windows.net'
        database = 'restaurant_DB'
        username = 'rest-admin'
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
>>>>>>> fbca40141bb08f9e2de9482aaaaa1dc7ff5e06cc

def DB_insert(query):
    # server = 'db-chatbot.database.windows.net'
    # database = 'restaurant_DB'
    # username = 'rest-admin'
    # password = 'Chatbot4'   
    # # driver= '{ODBC Driver 17 for SQL Server}'
    # cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    # cursor = cnxn.cursor()
    cursor.execute(query)

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

server = 'db-chatbot.database.windows.net'
database = 'restaurant_DB'
username = 'rest-admin'
password = 'Chatbot4'   
# driver= '{ODBC Driver 17 for SQL Server}'
try:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
except Exception as e:
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    print(errMsg)
