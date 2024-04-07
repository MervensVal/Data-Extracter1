import os
import pandas as pd
from datetime import date
import csv
import sys
import secret

try:
    def Save_Log_To_File(status,message,now):
        directory = secret.rootPath+'/Data-Extracter1/LogData'
        isExist = os.path.exists(directory)
        if not isExist:
            os.mkdir(directory)
        logFileName = 'LogFile.txt'
        logFilePath = directory+'/'+logFileName
        if not os.path.exists(logFilePath):
            f = open(logFilePath,'x')
        f = open(logFilePath,'a')
        f.write('\n'+status +'|' + message + '|' + now + '|' + '(end)')
        f.close

    def GetRevenueSubRegion2():
        path = secret.rootPath+'/Data-Extracter1/EmployeeImport/DataToImport.csv'
        df = pd.read_csv(path)
        min_salary = df['Salary'].min()
        max_salary = df['Salary'].max()
        sum_salary = df['Salary'].sum()
        num_records = df['Salary'].count()
        avg_salary = sum_salary/num_records
        dict = [{'MinSalary':min_salary,'MaxSalary':max_salary,'AverageSalary':avg_salary,'NumberOfRecords':num_records}]
        today = date.today()
        now = today.strftime("%m/%d/%Y").replace('/','-')
        fields = ['MinSalary','MaxSalary','AverageSalary','NumberOfRecords']
        file = secret.rootPath+'/Data-Extracter1/Report/Salary_Summary_Report'+now+'.csv'
        with open(file,'w') as csvFile:
            writer = csv.DictWriter(csvFile,fieldnames=fields)
            writer.writeheader()
            writer.writerows(dict)
        status = 'Success'
        message = 'Salary_Summary_Report Created'
        Save_Log_To_File(status,message,now)
        print(message)
    
    def Create_Report_Folder():
        directory = secret.rootPath+'/Data-Extracter1/Report'
        isExist = os.path.exists(directory)
        if not isExist:
            os.mkdir(directory)
except Exception as e:
    print(e)
    sys.exit()
