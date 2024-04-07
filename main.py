import db
import file_work 

try:
    print('Program Started')
    db.save_Employee_Data()
    file_work.Create_Report_Folder()
    file_work.GetRevenueSubRegion2()
    db.InsertCountryInfo()
    db.GetRevenueSubRegion()
    db.Get_Country_Statistics()
    db.Get_CountryRevenue_Statistics()
    db.Get_carOwnership_Statistics()
    print('Program Finished')
except Exception as e:
    print('Program terminated')
    print(e)
    print(type(e).__name__)