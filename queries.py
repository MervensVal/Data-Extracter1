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
			Race varchar(100) null,
			City varchar(40) not null,
			State varchar(40) not null,
			StreetAddress varchar(100) not null,
			JobTitle varchar(100) not null,
			Salary int not null
		)
end
'''
#Number of placeholders matches your table and CSV file format
Insert_Employee_Data = '''
insert into Employee({0})
values({1})
'''

#2nd method for inserting data
Insert_Employee_Data2 = '''
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
			Message varchar(300),
			Timestamp datetime
		)
end
'''

Insert_LogData = '''
insert into LogData
values(?,?,?)
'''

Get_Statistics1 = '''
select Count(EmployeeID) as Number_Of_Employees, Avg(salary) as Average_Salary,
Max(Salary) as Highest_Salary, Min(Salary) as Lowest_Salary, 
State from Employee group by State order by State asc
'''

createInsertCountry = '''
if((select count(*) from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'dbo'and TABLE_NAME = 'Country') > 0)
	begin 
		print 'table exists already'
	end
else 
	begin
		print 'creating table Country'
		Use Company
		create table Country(
		CountryID int identity(1000,1) primary key not null,
		CountryName varchar(100) not null,
		YearlyRevenue bigint)
		insert into Country
		values('United States of America',70000000),
		('Canada',500000),
		('Mexico',600000),
		('Brazil',810000),
		('Peru',970000),
		('Chile',784000),
		('Austria',7500000),
		('Hungary',900000),
		('Ghana',8400000),
		('Senegal',875000),
		('Mali',74000),
		('Japan',780090),
		('India',7810000)
	end

'''

createTableCountryInfo = '''
if((select count(*) from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'dbo'and TABLE_NAME = 'CountryInfo') > 0)
	begin 
		print 'table exists already'
	end
else 
	begin
		print 'creating table CountryInfo'
		Use Company
		create table CountryInfo(
		CountryInfoID int identity(1000,1) primary key not null,
		CountryName varchar(50),
		Capital varchar(50),
		Region varchar(50),
		Subregion varchar(50),
		Landlocked varchar(10),
		Currency varchar(150),
		)
	end
'''

insertCountryInfo = '''
insert into CountryInfo
values(?,?,?,?,?,?)
'''