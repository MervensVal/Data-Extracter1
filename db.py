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
        with open (secret.rootPath+'/Data-Extracter1/EmployeeImport/DataToImport.csv','r') as f:
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
            cursor.execute(q.createInsertDataCompanyCars)
            cursor.commit()
            cursor.close()
            fw.Save_Log_To_File('Success','Records inserted into Employee table',now)
            fw.Save_Log_To_File('Success','Records inserted into CompanyCars table',now)
        print('employee records inserted')
            
    def GetRevenueSubRegion():
        cursor = conn.cursor()
        cursor.execute(q.getRevenueSubRegion)
        with open(secret.rootPath+'/Data-Extracter1/Report/'+
                  'Subregion_Revenue_Report'+'_'+now.replace('/','-')+'.csv','w',newline='') as csvFile:
            csv_writer = csv.writer(csvFile)
            csv_writer.writerow([i[0] for i in cursor.description]) #write headers
            csv_writer.writerows(cursor)
            cursor.execute("insert into LogData values (?,?,GETDATE())",'Success','Report Created')
            cursor.commit()
            cursor.close()
            status = 'Success'
            message = 'Subregion_Revenue_Report Created'
            fw.Save_Log_To_File(status,message,now)    
        print('Subregion_Revenue_Report Created')        
    
    def InsertCountryInfo():
        cursor = conn.cursor()
        cursor.execute(q.createInsertCountry)
        cursor.execute(q.createTableCountryInfo)
        cursor.commit()
        cursor.close()
        cursor = conn.cursor()
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
            currency = (str(data[0]['currencies']))
            list = [country,capital,region,subregion,landlocked,currency]
            cursor.execute('insert into CountryInfo values (?,?,?,?,?,?)',(list))
            status = 'Success'
            message = 'Latest country [' + country + '] data inserted'
            cursor.execute("insert into LogData values (?,?,GETDATE())",status,message)
        cursor.commit()
        cursor.close()
        print('Country data inserted')

    def Get_Country_Statistics():
        with open(secret.rootPath+'/Data-Extracter1/Report/'+'Country_General_Report'+'_'
                  +now.replace('/','-')+'.csv','w',newline='')as csvFile1:
            cursor=conn.cursor()
            cursor.execute(q.getCountryData)
            csv_writer = csv.writer(csvFile1)
            csv_writer.writerow([i[0] for i in cursor.description]) #write headers
            csv_writer.writerows(cursor)
            status = 'Success'
            message = 'Country_General_Report created'
            cursor.execute("insert into LogData values(?,?,GETDATE())",status,message)
            cursor.commit()
            cursor.close()
            fw.Save_Log_To_File(status,message,now)
        print('Country_General_Report created')
        
    def Get_CountryRevenue_Statistics():
        with open(secret.rootPath+'/Data-Extracter1/Report/'+'CountryRevenueReport'+'_'
                  +now.replace('/','-')+'.csv','w',newline='')as csvFile1:
            cursor=conn.cursor()
            cursor.execute(q.getRevenueSubRegion)
            csv_writer = csv.writer(csvFile1)
            csv_writer.writerow([i[0] for i in cursor.description]) #write headers
            csv_writer.writerows(cursor)
            status = 'Success'
            message = 'Country revenue created'
            cursor.execute("insert into LogData values(?,?,GETDATE())",status,message)
            cursor.commit()
            cursor.close()
            fw.Save_Log_To_File('Success',message,now)
        print('Country general report created')
        
    def Get_carOwnership_Statistics():
        with open(secret.rootPath+'/Data-Extracter1/Report/'+'CarOwnershipReport'+'_'
                  +now.replace('/','-')+'.csv','w',newline='')as csvFile1:
            cursor=conn.cursor()
            cursor.execute(q.getCarOwnershipData)
            csv_writer = csv.writer(csvFile1)
            csv_writer.writerow([i[0] for i in cursor.description]) #write headers
            csv_writer.writerows(cursor)
            status = 'Success'
            message = 'Car Ownership Report created'
            cursor.execute("insert into LogData values(?,?,GETDATE())",status,message)
            cursor.commit()
            cursor.close()
            fw.Save_Log_To_File('Success',message,now)
        print('Country general report created')


