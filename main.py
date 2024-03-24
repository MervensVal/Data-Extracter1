from datetime import date
import db
import file_work 

try:
    print('Program Started')
    db.save_Employee_Data()
    file_work.Create_Report_Folder()
    db.Get_Statistics_DB()
    file_work.Get_Statistics()
    db.InsertCountryInfo()
    db.Get_Country_Statistics()
    db.Get_CountryRevenue_Statistics()
    print('Program Finished')
except Exception as e:
    print('Program terminated')
    print(e)