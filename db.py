import sys 
import pyodbc as odbc
import queries as q
import csv
import file_work as fw
import secret
from datetime import date
import request_work as rw

DRIVER = 'SQL SERVER'
SERVER_NAME = '(local)'
DATABASE_NAME = 'Company'

conn_string = f"""
Driver={DRIVER};
Server={SERVER_NAME};
Database={DATABASE_NAME};
Trusted_Connection=yes;
"""

try:
    today = date.today()
    now = today.strftime("%m/%d/%Y")
    conn = odbc.connect(conn_string)
except Exception as e:
    fw.Save_Log_To_File('Failed','Database Connection Failed')
    print(e)
    sys.exit()
else:
    def save_Employee_Data():
        with open (secret.rootPath+'/DataExtracter/EmployeeImport/DataToImport.csv','r') as f:
            reader = csv.reader(f)
            columns = next(reader)
            query = q.Insert_Employee_Data.format(','.join(columns),','.join('?'*len(columns)))
            cursor = conn.cursor()
            cursor.execute(q.Create_Table_Employee)
            cursor.commit()
            for data in reader:
                cursor.execute(query,data)        
            status = 'Success'
            message = 'Records inserted into Employee table'
            cursor.execute(q.Create_LogData_Table)
            cursor.commit()
            cursor.execute("insert into LogData values (?,?,GETDATE())",status,message)
            cursor.commit()
            cursor.close()
            print('employee records inserted')
            fw.Save_Log_To_File('Success','Records inserted into Employee table',now)
            
    def Get_Statistics_DB():
        cursor = conn.cursor()
        cursor.execute(q.Get_Statistics1)
        with open(secret.rootPath+'/DataExtracter/Report/'+
                  'Report_DB'+'_'+now.replace('/','-')+'.csv','w',newline='') as csvFile:
            csv_writer = csv.writer(csvFile)
            csv_writer.writerow([i[0] for i in cursor.description]) #write headers
            csv_writer.writerows(cursor)
            cursor.execute("insert into LogData values (?,?,GETDATE())",'Success','Report Created')
            cursor.commit()
            cursor.close()
            print('Report1 Created')
            fw.Save_Log_To_File('Success','Report1 Created',now)            
    
    def InsertCountryInfo():
        cursor = conn.cursor()
        cursor.execute(q.createTableCountryInfo)
        query =  'select CountryName from Country order by CountryName asc'
        cursor.execute(query)
        result = cursor.fetchall()
        for res in result:  
            country = str(res).replace("('","").replace("',)","")
            response = rw.getCountryInfo(country)     
            data = response.json()
            capital = (str(data[0]['capital']).replace("['","")).replace("']","")
            region = (str(data[0]['region']).replace("['","")).replace("']","")
            subregion = (str(data[0]['subregion']).replace("['","")).replace("']","")
            landlocked = (str(data[0]['landlocked']).replace("['","")).replace("']","")
            currency = (str(data[0]['currencies']))#.replace("{","").replace(":","").replace("'","").replace(",","").replace("}","")
            list = [country,capital,region,subregion,landlocked,currency]
            cursor.execute('insert into CountryInfo values (?,?,?,?,?,?)',(list))
            cursor.commit()
        status = 'Success'
        message = 'Latest country data inserted'
        cursor.execute("insert into LogData values (?,?,GETDATE())",status,message)
        cursor.commit()
        cursor.close()
        print(message)
