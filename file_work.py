import os
import pandas as pd
from datetime import date
import csv
import sys
import secret

try:
    def Save_Log_To_File(status,message,now):
        directory = secret.rootPath+'/DataExtracter/LogData'
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

    def Get_Statistics():
        path = secret.rootPath+'/DataExtracter/EmployeeImport/DataToImport.csv'
        df = pd.read_csv(path)
        min_salary = df['Salary'].min()
        max_salary = df['Salary'].max()
        sum_salary = df['Salary'].sum()
        num_records = df['Salary'].count()
        avg_salary = sum_salary/num_records
        dict = [{'MinSalary':min_salary},
            {'MaxSalary':max_salary},
            {'AverageSalary':avg_salary},
            {'NumberOfRecords':num_records}]
        today = date.today()
        now = today.strftime("%m/%d/%Y").replace('/','-')
        fields = ['MinSalary','MaxSalary','AverageSalary','NumberOfRecords']
        file = secret.rootPath+'/DataExtracter/Report/Report2'+now+'.csv'
        with open(file,'w') as csvFile:
            writer = csv.DictWriter(csvFile,fieldnames=fields)
            writer.writeheader()
            writer.writerows(dict)
        print('Report2 Created')
        Save_Log_To_File('Success','Report2 Created',now)
except Exception as e:
    print(e)
    sys.exit()
