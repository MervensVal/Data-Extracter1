Create_Table_Employee = '''
if(exists (select * from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'dbo' and TABLE_NAME = 'Employee'))
	begin
		print 'table exists'
	end
else
	begin
		print 'creating table Employee'
		use Company
		create table Employee(
			EmployeeID int identity(1000,1) primary key not null,
			FirstName varchar(40) not null,
			LastName varchar(40) not null,
			Email varchar(40) not null,
			Phone varchar(20) not null,	
			Gender varchar(20) not null,
			Race varchar(40) not null,
			City varchar(40) not null,
			State varchar(40) not null,
			StreetAddress varchar(100) not null,
			JobTitle varchar(100) not null,
			Salary int not null
		)
end
'''

Insert_Employee_Data = '''
insert into Employee
values(?,?,?,?,?,?,?,?,?,?,?)
'''

Create_LogData_Table = '''
if(exists (select * from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'dbo' and TABLE_NAME = 'LogData'))
	begin
		print 'table exists'
	end
else
	begin
		print 'creating table LogData'
		use Company
		create table LogData(
			Log_ID int identity(1000,1) primary key not null,
			Status varchar(10) not null,
			Message varchar(100),
			Timestamp date
		)
end
'''

Insert_LogData = '''
insert into LogData
values(?,?,?)
'''

Get_Employee_Data = '''
select FirstName,LastName,Email,Phone,isnull(Gender,'No Data') as Gender,
Race,City,State,StreetAddress,JobTitle,Salary 
from Employee
'''

Get_LogData = '''
select * from LogData
'''