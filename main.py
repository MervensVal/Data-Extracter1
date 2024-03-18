from datetime import date
import db
import file_work
import request_work
import sys

try:
    print('Program Started')
    request_work.test()
    db.save_Employee_Data()
    db.Get_Statistics_DB()
    file_work.Get_Statistics()
    db.InsertCountryInfo()
    print('Program Finished')
except Exception as e:
    print('Program terminated')
    print(e)