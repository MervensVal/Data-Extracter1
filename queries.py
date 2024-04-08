#All Records are test records. Mo live data used.

Create_Table_Employee = '''
if(exists (select * from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'dbo' and TABLE_NAME = 'Employee'))
	begin
		truncate table Employee
	end
else
	begin
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
			Salary int not null,
            CitizenshipCountryID int not null 
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
values(?,?,?,?,?,?,?,?,?,?,?,?)
'''

Create_LogData_Table = '''
if(exists (select * from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'dbo' and TABLE_NAME = 'LogData'))
	begin
		print 'table already exists'
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
    	truncate table CountryInfo
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
		Landlocked varchar(50),
		Currency varchar(150))
	end
'''

insertCountryInfo = '''
insert into CountryInfo
values(?,?,?,?,?,?)
'''

getStateSalaryInfo = '''
select 
Count(EmployeeID) as Number_Of_Employees, 
Avg(salary) as Average_Salary,
Max(Salary) as Highest_Salary, 
Min(Salary) as Lowest_Salary, 
State from Employee group by State 
order by State asc
'''

getCountryData = '''
select distinct
c.CountryName as Country,
ci.Capital,
substring(ci.Currency,3,3) as Currency,
ci.Landlocked,
c.YearlyRevenue,
(select count(EmployeeID) from Employee 
where CitizenshipCountryID = e.CitizenshipCountryID
) as NumberOfCitizens,
ci.Region,
ci.Subregion,
l.Timestamp as LastUpdatedDate
from Country c
join CountryInfo ci on c.CountryName = ci.CountryName 
join Employee e on e.CitizenshipCountryID = c.CountryID
join LogData l on l.Message like concat('%',c.CountryName,'%')
order by c.YearlyRevenue desc
'''

getRevenueSubRegion = '''
select 
ci.Subregion,sum(c.YearlyRevenue) as TotalRevenue
from Country c
join CountryInfo ci 
on c.CountryName = ci.CountryName
group by ci.Subregion
order by  TotalRevenue desc
'''

getCarOwnershipData = '''
select top 20 percent
emp.FirstName, 
emp.LastName, 
emp.Email,
isnull((select (replace(Email,Email,'Yes')) 
from Employee where lower(Email) like'%.gov' 
and EmployeeID = emp.EmployeeID), 'No') as 'Gov Email',
emp.Gender,
emp.State,
emp.Salary,
replace(
c.CountryName,'United States of America','United States'
) as 'Country of Citizenship',
ci.Subregion as 'Citizenship Subregion',
cc.CarMake,
cc.CarModel,
cc.CarModelYear,
isnull((case when cc.CarModelYear < 2000 
then 'Car older than 2000' end),'-') Note
from Employee emp
left join CompanyCars cc on cc.OwnerID = emp.EmployeeID
join Country c on 
emp.CitizenshipCountryID = c.CountryID
join CountryInfo ci on lower(c.CountryName) = lower(ci.CountryName)
where emp.Gender is not null and emp.Gender != ''
order by emp.Salary desc,ci.Region
'''

createInsertDataCompanyCars = '''
if((select count(*) from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'dbo'and TABLE_NAME = 'CompanyCars') > 0)
	begin 
    	print 'table already exists' 
	end
else 
	begin
		create table CompanyCars(
			EmployeeID int identity(1000,1) primary key not null,
			OwnerID int,
			CarMake varchar(100),
			CarModel varchar(100),
			CarModelYear int,
			VIN varchar (40)
		)
		insert into CompanyCars
		values ('1000','GMC','Savana 1500','2003','WDDHF0EB7EB921290'),
		('1001','Lincoln','Mark VIII','1997','5GAKVBED9BJ541211'),
		('1002','Subaru','Loyale','1993','5FRYD3H69EB253665'),
		('1003','Cadillac','CTS','2012','KNDPB3A21D7647076'),
		('1004','Dodge','Dakota','1996','1GKS1GKC4FR981917'),
		('1005','Mitsubishi','Chariot','1989','WBXPA73485W602221'),
		('1006','Subaru','SVX','1997','SCFFDABE4CG950002'),
		('1007','Ford','F150','2008','1FTEX1CM1BK302570'),
		('1008','Bentley','Continental GTC','2011','1N6AD0CU0EN878817'),
		('1009','Toyota','Tacoma','1995','WAULT54B42N168823'),
		('1010','Chevrolet','Silverado 2500','2012','5YMGZ0C55CL696604'),
		('1011','GMC','Rally Wagon 2500','1992','WA1VFAFL3DA836455'),
		('1012','Chevrolet','Malibu','2013','WBAVM1C50FV786575'),
		('1013','Jeep','Grand Cherokee','2010','1C6RD6HT2CS093097'),
		('1014','BMW','X5','2004','WVWGU7ANXCE038851'),
		('1015','Mazda','626','1998','3VW507AT7EM429435'),
		('1016','Ford','Explorer','1999','TRUWT28NX11755851'),
		('1017','Mitsubishi','L300','1987','WA1CMAFE2AD643478'),
		('1018','Dodge','Ram 2500 Club','1996','5TFBW5F17CX718032'),
		('1019','Mercedes-Benz','G-Class','2002','3D4PG9FG2BT157766'),
		('1020','BMW','3 Series','2007','1FTWX3B51AE951485'),
		('1021','Bentley','Brooklands','2010','5TDBK3EH8DS767830'),
		('1022','Mercedes-Benz','S-Class','1999','JTDKDTB33C1019856'),
		('1023','Mitsubishi','Mirage','1989','JM3TB2CA4F0011378'),
		('1024','Ford','Probe','1996','WAURMAFD4EN178819'),
		('1025','BMW','Z8','2000','WBAWV1C5XAP782130'),
		('1026','Volkswagen','Eurovan','2002','2G4GS5ER7D9333977'),
		('1027','Toyota','MR2','2004','KMHTC6AD4CU428414'),
		('1028','Chevrolet','Monte Carlo','2004','WBAYA8C54FG663154'),
		('1029','Lexus','GS','2011','3VWML7AJ2CM206475'),
		('1030','Cadillac','Escalade','2012','WBA3C3C59EP060190'),
		('1031','Ferrari','612 Scaglietti','2006','JM1NC2JF1B0248319'),
		('1032','Mercedes-Benz','CL-Class','1998','JN8AS5MT5BW480816'),
		('1033','Maserati','Gran Sport','2006','1FMJK1G5XEE526130'),
		('1034','Subaru','Legacy','2008','1FTEW1C83FF757862'),
		('1035','Subaru','B9 Tribeca','2007','WBA3C3G59FN171670'),
		('1036','Oldsmobile','98','1996','5GAKVDKD9DJ388123'),
		('1037','Ford','E150','1984','3MZBM1K70FM450635'),
		('1038','Ford','LTD','1986','1N6AF0KX0EN119106'),
		('1039','Mitsubishi','Eclipse','1992','19UUA8F54DA687596'),
		('1040','Cadillac','Escalade EXT','2002','5GADV23197D082124'),
		('1041','Ford','Aerostar','1996','1GYS4HEF0BR659990'),
		('1042','Ford','Ranger','1994','WAUDH68D21A339128'),
		('1043','GMC','3500','1999','WAUWFBFL1BA914922'),
		('1044','Subaru','Legacy','2011','JH4KB2F65CC848242'),
		('1045','Toyota','Matrix','2010','1GYS4KEF0ER111330'),
		('1046','Toyota','Sienna','2009','JTHBW1GG5F2924350'),
		('1047','Suzuki','Swift','1993','WBALL5C57FP720823'),
		('1048','Ford','Mustang','1990','JN1CV6FEXBM144089'),
		('1049','Ford','Escape','2008','1C3CDZCB0DN404609'),
		('1050','Ford','E150','2008','1GYUKAEF1AR756071'),
		('1051','Acura','Legend','1995','1N6AA0EC9EN633107'),
		('1052','Chevrolet','Corvair 500','1963','5N1AA0NC4BN513256'),
		('1053','Mazda','Mazda6','2008','1C6RD7JT1CS573678'),
		('1054','Mitsubishi','Chariot','1993','1D7RV1CT6BS657077'),
		('1055','Pontiac','Grand Am','2002','5GADT13S542360596'),
		('1056','Subaru','Leone','1989','1HGCR6F32EA669056'),
		('1057','Mazda','B-Series','2009','SALWR2VF7FA384900'),
		('1058','Ford','Aerostar','1997','1FTSW2B58AE828438'),
		('1059','Mercury','Topaz','1985','WBAWL73519P219004'),
		('1060','Nissan','Altima','2001','WBABW53486P712336'),
		('1061','Ford','Flex','2011','YV4952CFXB1409508'),
		('1062','Honda','Ridgeline','2007','1FTWF3A59AE583352'),
		('1063','Ford','Econoline E150','1994','WA1EY94L78D267190'),
		('1064','Buick','Enclave','2009','WVGEF9BP7FD742346'),
		('1065','Toyota','Avalon','2011','1G4HP54K53U645128'),
		('1066','Ford','F350','2012','2C3CA4CGXBH400483'),
		('1067','Chevrolet','S10','1995','2FMGK5BC1AB192731'),
		('1068','Kia','Spectra','2005','1G6YX36D595982122'),
		('1069','Lincoln','MKS','2009','WBA3A5G57EN867959'),
		('1070','Chevrolet','Classic','2004','2C3CDXEJ9CH669254'),
		('1071','GMC','Yukon XL 1500','2006','3GTU1YEJ3BG080357'),
		('1072','Honda','Accord','1996','SCFEFBACXAG282439'),
		('1073','Oldsmobile','88','1996','WAU4FAFR3CA426479'),
		('1074','Chevrolet','Equinox','2012','KL4CJDSB2EB246246'),
		('1075','Mazda','B-Series Plus','1999','1C4RDHAGXDC702725'),
		('1076','Jeep','Patriot','2007','JM3TB2BA9D0741091'),
		('1077','Chevrolet','Suburban 2500','2009','5NPE24AF8FH248972'),
		('1078','Chevrolet','Camaro','1968','WBA3T7C52FP307638'),
		('1079','Dodge','Dakota','2003','JA32X8HW5AU333136'),
		('1080','Mazda','Mazdaspeed 3','2010','KMHEC4A45BA108547'),
		('1081','Subaru','B9 Tribeca','2006','WAUEKBFB9AN232117'),
		('1082','Pontiac','Grand Prix Turbo','1990','WA1CFAFP1FA133708'),
		('1083','Ford','Explorer Sport','2000','1G6DV5EP8C0002561'),
		('1084','Volvo','C70','2009','WDDHF0EB3EB773803'),
		('1085','Audi','Q5','2011','19UYA42521A938997'),
		('1086','Audi','5000S','1984','3D73Y4CL6BG921288'),
		('1087','Chevrolet','Lumina','1999','KL4CJHSBXFB488324'),
		('1088','GMC','Vandura 1500','1992','SCBZB25E72C493925'),
		('1089','BMW','Z3','2002','WBA3B3C51DF429647'),
		('1090','Toyota','Celica','1995','1D7CW3BK3AS975566'),
		('1091','Dodge','Charger','2008','5TDDCRFH2ES330009'),
		('1092','Toyota','Sienna','2006','2B3CA2CV6AH794160'),
		('1093','Audi','Q7','2011','JH4CW2H62EC895446'),
		('1094','Chevrolet','2500','1997','2C3CDXFG5EH892509'),
		('1095','Volkswagen','Cabriolet','2000','WAUEG98E46A524595'),
		('1096','Volvo','960','1995','JM3TB2BV4E0999779'),
		('1097','Spyker','C8 Double 12 S','2006','WBSDE93473C278072'),
		('1098','Volvo','S60','2001','1G6DM57N030909187'),
		('1099','Subaru','Forester','2004','1FTEX1CM5BF156988'),
		('1100','Dodge','Ram 2500 Club','1998','1GYFK66848R416977'),
		('1101','Dodge','Monaco','1992','1C3CDZBG1EN552542'),
		('1102','Dodge','Ram 2500','2000','SCFEFBAC4AG387347'),
		('1103','Plymouth','Fury','1964','5TFBY5F14AX852617'),
		('1104','Jeep','Grand Cherokee','1997','SALFR2BG3DH828162'),
		('1105','Ford','Mustang','2008','1N6AA0EK9FN206003'),
		('1106','Lincoln','Navigator','2006','4JGDA2EB5DA297766'),
		('1107','Ford','Explorer','2008','WAUHGAFC3CN941002'),
		('1108','Hyundai','Accent','2000','1GYFC16219R596173'),
		('1109','BMW','M3','2006','3C3CFFJH6ET123948'),
		('1110','GMC','Savana 2500','2002','JM1NC2LF3C0908410'),
		('1111','Hyundai','Sonata','2012','1G4HK5E97AU983279'),
		('1112','Nissan','Maxima','1995','1C3BCBEB8EN457031'),
		('1113','MINI','Cooper Clubman','2008','1G4CW54K454663135'),
		('1114','Nissan','Altima','1995','2T1BU4EE8DC146232'),
		('1115','Oldsmobile','Silhouette','1994','1C4RDJEG5EC766626'),
		('1116','Volvo','S90','1998','JTEBU4BF7BK076713'),
		('1117','Austin','Mini','1963','WUAW2AFC0FN792483'),
		('1118','Jaguar','XJ Series','1993','WAUVT58E25A275572'),
		('1119','Mitsubishi','GTO','1990','1GKS1AEC6FR393218'),
		('1120','Volkswagen','Jetta','2007','3N6CM0KN5EK712446'),
		('1121','Subaru','Leone','1989','WAUHE98P89A162666'),
		('1122','Volvo','V70','2008','1FMEU8DE6AU750889'),
		('1123','Pontiac','Firefly','1986','WBAXG5C58CC392191'),
		('1124','Mitsubishi','Lancer Evolution','2004','KMHGH4JH6FU889659'),
		('1125','Lincoln','Aviator','2003','5J8TB3H34DL583959'),
		('1126','Mazda','B-Series Plus','1995','1G6KD57Y47U200553'),
		('1127','Buick','LeSabre','1986','1GYUKBEF0AR329793'),
		('1128','Mazda','Navajo','1992','WDDHF2EB3DA508962'),
		('1129','Land Rover','Freelander','2009','1D4RE3GG6BC962692'),
		('1130','Mercedes-Benz','C-Class','2011','1G6ET129X1B659923'),
		('1131','GMC','Yukon XL 2500','2012','SCFEBBAK4DG003610'),
		('1132','Ford','F250','2002','WA1LKAFP2AA441393'),
		('1133','Chevrolet','TrailBlazer','2002','1FMHK7B82CG712751'),
		('1134','Land Rover','LR2','2009','WUAW2BFC2FN542989'),
		('1135','Ford','Mustang','1987','1GKS1AE02BR879315'),
		('1136','Aston Martin','V8 Vantage','2006','1GYFK26209R342480'),
		('1137','Lotus','Elan','1991','4T1BF3EK8AU419044'),
		('1138','Chevrolet','Corvette','1997','1G6DH577580929531'),
		('1139','Ford','E150','2004','1G6DU6EV2A0773215'),
		('1140','Honda','Accord','1984','4T1BD1EB5EU895185'),
		('1141','GMC','Envoy','2008','WBA5A7C50FG071568'),
		('1142','Toyota','T100','1994','WBANF33506C732212'),
		('1143','Land Rover','Defender Ice Edition','2010','YV4902DZ6D2709700'),
		('1144','Mitsubishi','Pajero','1986','1G4GE5EV0AF399729'),
		('1145','Land Rover','Range Rover','2004','1G6DC67A380900318'),
		('1146','Chevrolet','Monte Carlo','1998','1GKKRNED4CJ783916'),
		('1147','Isuzu','Ascender','2005','WBAFR1C54BD103962'),
		('1148','Pontiac','GTO','1967','1G6DL1ED4B0529516'),
		('1149','Pontiac','Firefly','1992','WDDEJ7KB8BA803250'),
		('1150','Pontiac','Grand Am','1989','1GYS3EEJ3DR800088'),
		('1151','Kia','Sedona','2003','SCBZK25E42C097225'),
		('1152','Volkswagen','New Beetle','2003','3C6LD4AT7CG496228'),
		('1153','BMW','7 Series','2010','WBA3B5G54DN035796'),
		('1154','Dodge','Challenger','2011','WAULT58E55A433300'),
		('1155','BMW','3 Series','2008','1G6DC5EG3A0697633'),
		('1156','Pontiac','Gemini','1987','1G6DL8EY5B0188381'),
		('1157','Ford','Festiva','1988','1GYFK63828R129058'),
		('1158','Buick','Electra','1986','WAUGL78E38A553047'),
		('1159','Daewoo','Leganza','1999','WBABS33423P556919'),
		('1160','Chevrolet','Express 3500','1996','WBA3B5C54DJ544395'),
		('1161','Mercury','Grand Marquis','1997','KNDPB3A26D7042972'),
		('1162','Maserati','GranTurismo','2008','KL4CJASB0DB139855'),
		('1163','Porsche','Boxster','2009','4T1BF1FK7FU044936'),
		('1164','Ford','Escape','2002','1G6KD57Y38U729445'),
		('1165','Lincoln','Town Car','2005','5GADT13S872350794'),
		('1166','Chevrolet','Impala','2011','WDDHF5KB7FB786900'),
		('1167','Saturn','Aura','2008','WDCGG0EB8EG202470'),
		('1168','Jeep','Commander','2010','WAUHMBFC2EN401965'),
		('1169','Toyota','Corolla','2011','WAUHF98P97A304680'),
		('1170','Hummer','H1','2006','WAUPFAFM5BA298682'),
		('1171','Ford','F-Series','1985','2D4RN1AG4BR342055'),
		('1172','BMW','7 Series','2008','WAUEH74F26N420809'),
		('1173','Mitsubishi','Diamante','1999','1FTMF1CW5AK283830'),
		('1174','Chevrolet','Blazer','2002','WBAPH5C53BF651258'),
		('1175','Honda','Prelude','1984','WBA3R1C53EF463302'),
		('1176','Dodge','Caliber','2011','WBSBL93421J717927'),
		('1177','Volvo','XC70','2003','1GKS1AE09BR787134'),
		('1178','Jeep','Grand Cherokee','1997','5XXGM4A75CG496146'),
		('1179','Chevrolet','Silverado 2500','2011','WDDEJ7KBXBA384043'),
		('1180','Pontiac','GTO','1967','5LMJJ2H59BE973955'),
		('1181','Oldsmobile','Aurora','2002','1FMJK1H51EE096860'),
		('1182','Dodge','Dakota Club','1996','5N1CR2MM9EC400748'),
		('1183','Isuzu','Hombre','1998','WBAVA37527N326768'),
		('1184','Mercury','Sable','1987','WBAPK7C54BA046532'),
		('1185','Porsche','911','2001','1G4HC5EM7BU333936'),
		('1186','Pontiac','Tempest','1965','JTHBL1EF2E5008869'),
		('1187','Volvo','C30','2010','1G6DS5E32D0400971'),
		('1188','Audi','A6','2006','JTHBE1BL4FA771358'),
		('1189','Chevrolet','Avalanche 2500','2004','2G4GV5GV4D9905122'),
		('1190','GMC','Sonoma Club Coupe','1994','JTEBU4BF8BK822635'),
		('1191','Ford','Explorer Sport','2002','5GADT13S542298410'),
		('1192','Volvo','XC70','2009','WBALW7C58ED338156'),
		('1193','Porsche','928','1986','5FPYK1F52EB212209'),
		('1194','Mercedes-Benz','S-Class','1993','1FBNE3BL5DD415508'),
		('1195','Toyota','Celica','1992','1G6DS1ED6B0831926'),
		('1196','Buick','Regal','1989','WBAVL1C56EV845758'),
		('1197','Dodge','Stratus','2001','TRUTC28N321517019'),
		('1198','Chrysler','Town & Country','1993','1GYS4CEF2DR669717'),
		('1199','Subaru','Loyale','1990','WAUEG78E46A093700'),
		('1200','Lincoln','Town Car','2000','SALVP2BG9FH962131'),
		('1201','Isuzu','Trooper','1994','JM1NC2PF5E0143827'),
		('1202','Chevrolet','S10','1995','WBAVD53517A479366'),
		('1203','Ford','Explorer','1997','4T1BD1FK6CU928299'),
		('1204','Acura','SLX','1996','3GYT4MEF8DG716467'),
		('1205','Ford','Festiva','1993','WVGAV3AX4DW774852'),
		('1206','Subaru','XT','1991','3C6JD6BP3CG640894'),
		('1207','Volkswagen','Scirocco','1985','4A31K2DF2CE742011'),
		('1208','Maybach','Landaulet','2009','WAUJFAFH3DN310347'),
		('1209','Chevrolet','Corvette','2006','19UYA42703A000937'),
		('1210','Jeep','Grand Cherokee','2001','1G6AS5SX7E0209865'),
		('1211','Chrysler','Sebring','2003','WBSVA93528E568238'),
		('1212','Volkswagen','Jetta','2011','WBABW33416P043296'),
		('1213','Ford','Windstar','1995','1GYS4KEF6DR343896'),
		('1214','Chevrolet','Silverado 3500','2005','WBAVT73528F012444'),
		('1215','Mercedes-Benz','GL-Class','2011','3N1CN7AP8FL906723'),
		('1216','Volkswagen','Passat','2008','1FTEX1CM0BF408338'),
		('1217','Mitsubishi','Galant','2012','JN8AE2KP2B9763538'),
		('1218','Mercury','Mariner','2007','1N6AD0CU1FN702716'),
		('1219','Mitsubishi','Pajero','1987','2C3CCARG8FH704031'),
		('1220','Lincoln','Town Car','1991','WP0CB2A8XCS296483'),
		('1221','Volkswagen','Passat','1987','WBA3B5C56EF305824'),
		('1222','Eagle','Summit','1995','WBAUC7C58AV238270'),
		('1223','Nissan','Altima','1995','WAUDGBFL8AA121989'),
		('1224','Mercury','Cougar','1967','WAUKF98E75A798748'),
		('1225','Honda','S2000','2006','WBANB33575C673279'),
		('1226','Pontiac','Sunbird','1986','2C3CDZAG2FH709314'),
		('1227','Ford','Explorer','1998','3N6CM0KN3EK754369'),
		('1228','Ford','Econoline E250','2000','WA1YD64B05N031789'),
		('1229','Subaru','Outback','2007','WAUFFBFL1DN757503'),
		('1230','Mitsubishi','Lancer Evolution','2003','WBAYA8C59FD492869'),
		('1231','Acura','MDX','2008','3GYFNKE67BS621908'),
		('1232','Audi','5000S','1985','WAUKF98E68A121985'),
		('1233','Ford','GT500','2008','1G4HP54K53U347565'),
		('1234','Cadillac','Escalade EXT','2010','4T3BA3BB2BU656897'),
		('1235','Volvo','S40','2010','1G6AB1RX4F0937529'),
		('1236','Maserati','Biturbo','1984','1FTFW1E81AK951789'),
		('1237','Honda','Civic','1980','WAULC58E85A796741'),
		('1238','Chevrolet','Camaro','1975','WAUKFAFL6CA740453'),
		('1239','Acura','NSX','1998','ZFF60FCA3A0577805'),
		('1240','BMW','X5','2000','1D4RD4GG1BC901257'),
		('1241','Chevrolet','Uplander','2006','SCBFC7ZA3EC928268'),
		('1242','GMC','1500 Club Coupe','1994','WDDHF5KB9FB943231'),
		('1243','Lexus','LX','2007','1FTWF3C55AE754692'),
		('1244','GMC','Jimmy','1992','WAUDK78T38A241816'),
		('1245','Cadillac','Eldorado','1994','WAUFEAFM1DA645409'),
		('1246','Pontiac','Grand Prix','1978','WAUSF98E46A522982'),
		('1247','Volkswagen','New Beetle','2010','4A37L2EFXAE222982'),
		('1248','Isuzu','Hombre Space','2000','1FMCU4K30BK155941'),
		('1249','Acura','ZDX','2011','JH4NA21682T525793'),
		('1250','Hyundai','Sonata','1994','3VW1K7AJ8FM288528'),
		('1251','Chevrolet','2500','1999','1N6AF0KY3EN877594'),
		('1252','GMC','Jimmy','1997','1G6DA67V480233476'),
		('1253','Mitsubishi','Challenger','2004','SCBFR7ZA4DC736032'),
		('1254','Lincoln','Continental','1989','5TDBKRFH7FS929080'),
		('1255','Mitsubishi','Precis','1986','2HNYD2H3XDH651827'),
		('1256','GMC','Savana 3500','2009','3TMJU4GN0AM683883'),
		('1257','Buick','Skylark','1994','5GAKRAKDXEJ580588'),
		('1258','Volvo','V40','2003','WBAVM1C52EV658997'),
		('1259','Subaru','Outback','2008','JTHHE5BC3F5560534'),
		('1260','Audi','A3','2009','5N1AR1NB3AC463756'),
		('1261','Porsche','928','1995','3N1CN7AP9EL153654'),
		('1262','Lamborghini','Murciélago','2006','1C4PJLAK9CW182778'),
		('1263','Subaru','Outback','2012','2G4GU5GC7B9309968'),
		('1264','Toyota','Celica','1993','2D4RN7DG4BR131016'),
		('1265','Cadillac','Catera','1998','WAUFL54D51N487564'),
		('1266','Suzuki','Equator','2010','WVWAN7AN1EE486191'),
		('1267','Hummer','H1','1994','WBAPM5C56BF661794'),
		('1268','Suzuki','SJ','1991','WBA3D5C52FK588905'),
		('1269','Ram','C/V','2012','1VWAH7A35DC952668'),
		('1270','Lincoln','Town Car','2006','5UXFG8C58CL502221'),
		('1271','Chevrolet','Blazer','1994','JTEBU5JR8D5743615'),
		('1272','Mitsubishi','Tredia','1987','5J8TB18578A946570'),
		('1273','Pontiac','G3','2009','SCFFDABE9CG826503'),
		('1274','Nissan','300ZX','1991','WBXPA93434W316738'),
		('1275','Mercedes-Benz','400E','1992','2T1BURHE1FC195879'),
		('1276','GMC','Sierra','2009','JN8AZ1FY2DW510080'),
		('1277','Audi','A5','2011','WAUDGBFL3CA956451'),
		('1278','Chrysler','LeBaron','1992','WA1DGAFE8ED323910'),
		('1279','Ford','Expedition','2007','5LMJJ3H58BE128603'),
		('1280','Audi','S8','2009','KMHGN4JE8FU043984'),
		('1281','Bentley','Azure T','2010','WAUVT68E12A397177'),
		('1282','Chevrolet','Citation','1980','1FAHP2DW2BG513100'),
		('1283','Audi','A6','2006','4JGBB9FBXAA158627'),
		('1284','Honda','Odyssey','2003','JN8AE2KPXD9954482'),
		('1285','GMC','Savana 3500','2006','SCFFDCCD3CG699538'),
		('1286','Toyota','Camry','2010','TRUSX28N321278734'),
		('1287','Chevrolet','S10','2003','1G6DK1E34C0975578'),
		('1288','Dodge','Ram Van 3500','2002','JHMZF1C67DS594462'),
		('1289','Eagle','Talon','1991','WBA3V5C53FP199707'),
		('1290','Ford','Taurus','2003','WBA3B1C53EK998884'),
		('1291','Mercury','Grand Marquis','2001','1G6KE57Y12U887058'),
		('1292','Lamborghini','Gallardo','2012','WBA1K5C57FV978703'),
		('1293','Audi','A4','2006','WBA4B3C57FG996656'),
		('1294','Toyota','MR2','1986','JN8AE2KP3F9202240'),
		('1295','Infiniti','G35','2006','WAUCKAFR0AA489821'),
		('1296','Mazda','Mazda6','2006','WBAWB735X8P579602'),
		('1297','Ford','Five Hundred','2005','1N6AA0CC3AN873993'),
		('1298','Lamborghini','Gallardo','2004','WBASP2C56CC319765'),
		('1299','Mazda','MX-3','1992','3VW517AT1EM761772'),
		('1300','Buick','Century','2004','WBA3C3C55EP574182'),
		('1301','Honda','Element','2003','5FPYK1F20EB170886'),
		('1302','Mercedes-Benz','190E','1993','1FTEW1CM2BF163867'),
		('1303','Pontiac','Grand Am','2002','1G6DS5E32C0688893'),
		('1304','Ford','LTD Crown Victoria','1991','1GD020CG3DZ169400'),
		('1305','Buick','LaCrosse','2006','1G6KE57Y45U641092'),
		('1306','Ford','Laser','1986','JTHDU1EF0C5445773'),
		('1307','Chevrolet','Avalanche','2008','WVGEP9BP8FD818900'),
		('1308','Suzuki','Samurai','1992','SAJWA4DB4EL015389'),
		('1309','GMC','Sonoma','2001','5J8TB1H27AA360236'),
		('1310','Ford','Mustang','1998','4USBU53527L126218'),
		('1311','Mitsubishi','Eclipse','2011','1C3ADEBZ0DV258307'),
		('1312','Pontiac','Grand Prix','2002','3N6CM0KN9DK409488'),
		('1313','BMW','M3','2003','1GYEK63NX6R659406'),
		('1314','Buick','Rainier','2004','WAUDV94F88N436905'),
		('1315','BMW','X5','2003','JHMZF1C49DS226010'),
		('1316','Mercedes-Benz','300SD','1992','2C3CDXDT8CH925371'),
		('1317','Infiniti','EX','2011','5J8TB4H34FL640413'),
		('1318','Mercedes-Benz','GLK-Class','2012','1FTEX1EW2AK386346'),
		('1319','Ford','Probe','1993','137ZA84301E558865'),
		('1320','Chevrolet','Corvette','1956','SAJWA1C79D8978107'),
		('1321','Alfa Romeo','Spider','1994','WAUBFAFL4BN212479'),
		('1322','Hyundai','Elantra','2001','3VW517ATXEM767943'),
		('1323','Volkswagen','New Beetle','2006','WBALL5C53FP248698'),
		('1324','Mercedes-Benz','C-Class','2010','2C3CDXJG8EH334693'),
		('1325','GMC','Yukon XL 2500','2004','WAUMR44E16N225640'),
		('1326','Lexus','SC','1999','WBSBR93452E440313'),
		('1327','Chevrolet','S10 Blazer','1992','3C3CFFHH1ET131168'),
		('1328','Subaru','Loyale','1994','WBAKF3C53BE377473'),
		('1329','Dodge','Ram 1500','1997','WDCGG5GBXAF827169'),
		('1330','Honda','Pilot','2011','WBADX7C56BE823886'),
		('1331','Ford','F450','2008','1FMCU5K36AK314823'),
		('1332','Lexus','LS','1994','2G4WY55J621750202'),
		('1333','Volkswagen','CC','2012','3N1CN7AP7DL634551'),
		('1334','Ford','Torino','1970','1C3CCBAB3CN176486'),
		('1335','Kia','Rio','2011','3VWJP7AT9CM424910'),
		('1336','Plymouth','Volare','1976','5GAER13788J665178'),
		('1337','Lotus','Esprit','2003','2C3CDXHG8FH407357'),
		('1338','GMC','Envoy','2003','WAULD64B02N745625'),
		('1339','Ford','Explorer','2003','1G6YX36DX65793459'),
		('1340','Dodge','D150','1993','WAUKFBFL1DA297202'),
		('1341','Mazda','Mazda3','2011','4USCN53422L598498'),
		('1342','Ford','Thunderbird','1984','2HNYD18243H277974'),
		('1343','Dodge','Stratus','2002','WAUMFAFL8AN293025'),
		('1344','Bentley','Azure','2008','SCFAD01E49G568034'),
		('1345','Jeep','Wrangler','2001','WDDGF4HB5DF456434'),
		('1346','Honda','Passport','2000','WAUKF98P19A526493'),
		('1347','Kia','Spectra','2003','JTDZN3EU2E3409032'),
		('1348','Toyota','Tacoma','2004','3C6JD7DP1CG338846'),
		('1349','Mitsubishi','Montero','2000','1D7RW5GK2BS233868'),
		('1350','Mercedes-Benz','E-Class','1996','WA1VMAFP9EA028153'),
		('1351','Mitsubishi','Galant','1986','1VWAS7A35FC731446'),
		('1352','Nissan','Maxima','2000','WBAGJ03471D352848'),
		('1353','Mitsubishi','Chariot','1988','WAUDF58E55A365298'),
		('1354','Acura','ZDX','2011','4USDU53467L542921'),
		('1355','BMW','X6 M','2011','2HNYD18286H030199'),
		('1356','Honda','CR-V','2002','WP0AB2A97BS208357'),
		('1357','Lincoln','Navigator','1999','WAUD2AFD0EN238904'),
		('1358','Infiniti','FX','2004','WA1VYAFE5AD225199'),
		('1359','Mercedes-Benz','E-Class','1987','WAUDH78E27A979475'),
		('1360','Jeep','Grand Cherokee','2009','WAUDK78T79A032287'),
		('1361','Nissan','Altima','2003','WBASN4C5XAC337104'),
		('1362','Audi','80','1991','3FAHP0CG5BR348182'),
		('1363','Audi','80','1989','WAUHFBFL3DN348668'),
		('1364','GMC','1500 Club Coupe','1992','1FTSW3A51AE983940'),
		('1365','Toyota','Paseo','1997','5BZAF0AA6FN725219'),
		('1366','Audi','Allroad','2005','4A4AP3AU2DE452472'),
		('1367','Chevrolet','Avalanche','2009','WA1CFBFP6DA626335'),
		('1368','Dodge','Ram 3500','2006','WBA4A5C55FD352637'),
		('1369','BMW','M3','2006','1N6AA0CH1DN742545'),
		('1370','Chevrolet','Corsica','1996','2G4WB52K321920627'),
		('1371','Plymouth','Breeze','1996','JM1NC2JFXD0865205'),
		('1372','Pontiac','Firebird','1968','WBAYE8C56ED980793'),
		('1373','Ford','LTD','1986','WAUUL78EX7A791110'),
		('1374','BMW','X6','2008','WBA3B3C51EJ937129'),
		('1375','Dodge','Challenger','2008','JN8AE2KP0D9030262'),
		('1376','Volvo','V70','2006','JTDKN3DU0B0209511'),
		('1377','Cadillac','STS-V','2009','SCFBB03B37G557567'),
		('1378','Ford','Explorer','1998','1G4GF5G34EF100287'),
		('1379','Pontiac','Firefly','1995','KMHCT4AE4EU119249'),
		('1380','Ford','Tempo','1989','JM1DE1KY8C0237612'),
		('1381','Ford','Falcon','1967','SALGS2EF5EA106150'),
		('1382','Chevrolet','S10','2003','1FTWW3B59AE909259'),
		('1383','Chevrolet','Express 3500','1998','2G61R5S35E9818466'),
		('1384','Volkswagen','Eos','2010','5N1AA0NCXDN664296'),
		('1385','Pontiac','Bonneville','2004','WBA6B8C51ED194545'),
		('1386','Ford','Econoline E150','1999','JN1AV7AP7FM739851'),
		('1387','Hyundai','Accent','1995','WDDPK4HA6EF558023'),
		('1388','Buick','Riviera','1996','JTHBE5C20B5673590'),
		('1389','Dodge','Caravan','2002','19VDE3F33DE833383'),
		('1390','Volvo','940','1992','1FTSW3B59AE994814'),
		('1391','Kia','Rondo','2010','1FMJU1F56AE413216'),
		('1392','Mercury','Topaz','1988','YV4612HK5F1090593'),
		('1393','Land Rover','Discovery','2000','1C4NJCBA9ED696187'),
		('1394','Mercury','Milan','2008','ZFBCFAAH2EZ524617'),
		('1395','GMC','Savana 2500','2003','WAUHF98P89A730394'),
		('1396','Nissan','Sentra','1991','3C6TD5PT9CG847380'),
		('1397','Porsche','911','2003','WBANE73597C684933'),
		('1398','Volvo','S40','2004','WAUAF78E58A571692'),
		('1399','Hyundai','Sonata','2006','WAUEG94F26N940930'),
		('1400','Jeep','Cherokee','1995','1G4HP54K03U660829'),
		('1401','GMC','3500 Club Coupe','1997','WBAPM5C51BA687622'),
		('1402','Mitsubishi','Pajero','1992','WBA5M4C50FD308101'),
		('1403','Porsche','Boxster','1998','3GYFNEEY8AS333820'),
		('1404','Austin','Mini Cooper','1961','3FAHP0DC5BR007960'),
		('1405','Pontiac','Solstice','2007','19UUA8F21EA138588'),
		('1406','Dodge','Viper','1992','WAUPL58E15A082807'),
		('1407','Jeep','Liberty','2009','WAUJC68EX2A299084'),
		('1408','Land Rover','Range Rover','1993','WBAPM7C56AE999535'),
		('1409','Honda','del Sol','1995','WAUMFAFL1AN897371'),
		('1410','Buick','Riviera','1992','5J8TB3H32GL072528'),
		('1411','Plymouth','Breeze','1997','JN1AZ4FH6FM304128'),
		('1412','Mercury','Villager','1997','1G6KF57995U186648'),
		('1413','Jeep','Liberty','2004','WAUHF78PX8A251901'),
		('1414','Buick','Regal','1999','3VWML7AJ9EM156872'),
		('1415','Ford','Freestar','2006','WAUKF98E08A934366'),
		('1416','Acura','MDX','2004','WAUJFAFH6BN381717'),
		('1417','Ford','GT500','2009','KMHTC6AD1FU571826'),
		('1418','Jeep','Liberty','2007','1G6DK5E35D0030972'),
		('1419','Mercedes-Benz','SLR McLaren','2006','WAUDH94F56N787226'),
		('1420','Buick','Riviera','1987','WAUHF98P46A772511'),
		('1421','Dodge','Grand Caravan','2006','JN1AJ0HPXCM362341'),
		('1422','Kia','Rio','2011','1GD11ZCG7BF738744'),
		('1423','Oldsmobile','Ciera','1993','JTDKN3DU7F0699015'),
		('1424','Buick','LaCrosse','2009','3C4PDDDG4CT461291'),
		('1425','Mercedes-Benz','C-Class','2006','WBA3B9G51EN733405'),
		('1426','Mitsubishi','Galant','2003','WAUHE98P29A049795'),
		('1427','Volkswagen','New Beetle','2006','WBAEN33422E434625'),
		('1428','Ford','Bronco','1989','3D4PH7FG2BT959820'),
		('1429','Mazda','B-Series','1995','1FMCU4K39BK032770'),
		('1430','GMC','1500','1996','WAUJC58E74A142030'),
		('1431','Pontiac','Grand Prix','2005','JM3TB2MA9A0992296'),
		('1432','Chevrolet','Silverado 2500','2003','1G4HP54K44U669535'),
		('1433','Ford','Expedition EL','2010','19VDE3F32DE227136'),
		('1434','Volkswagen','Fox','1992','WA1CKAFP1AA269714'),
		('1435','Honda','del Sol','1995','WBAXH5C57DD774141'),
		('1436','Mazda','626','2000','WDDHF0EB3EA391499'),
		('1437','Infiniti','Q','1994','JN8AZ2KR4AT846086'),
		('1438','Chrysler','Grand Voyager','2000','5FRYD3H21EB662935'),
		('1439','Land Rover','Defender 90','1994','SALFR2BG4EH835316'),
		('1440','Dodge','Viper','2002','JTEBU5JR4E5620959'),
		('1441','Honda','Fit','2012','4T1BD1FK4DU434881'),
		('1442','Chevrolet','Tahoe','2006','WBA3B1C56DF608559'),
		('1443','Acura','RDX','2008','5FRYD4H91GB560217'),
		('1444','Toyota','Sienna','2004','1G6AF5S32E0723821'),
		('1445','Dodge','Viper','2008','WBAVB73518F263426'),
		('1446','GMC','Sonoma Club Coupe','1993','WAUCFAFCXFN283552'),
		('1447','Mitsubishi','Eclipse','2003','1HGCR2E58DA841679'),
		('1448','Audi','4000CS Quattro','1986','JM1NC2EF8A0218078'),
		('1449','Chrysler','Crossfire','2005','1D4RD3GG0BC923504'),
		('1450','Mazda','RX-8','2008','YV1902FHXD1068221'),
		('1451','Ford','Econoline E150','1995','WAUKH78E77A098679'),
		('1452','Mitsubishi','Pajero','1989','5TFCW5F17CX330223'),
		('1453','Chevrolet','G-Series G30','1992','WAU4GBFB3AN795810'),
		('1454','Mercury','Cougar','1968','SCBLC31E72C260805'),
		('1455','Volkswagen','Golf','1993','1GD422CG4EF620981'),
		('1456','Buick','Reatta','1989','1GD02ZCG9DZ677374'),
		('1457','Pontiac','Bonneville','1995','1D7RW3BK8AS932481'),
		('1458','Volkswagen','Type 2','1988','5UXFA53533L095330'),
		('1459','Maybach','57','2004','1N4AB7AP3DN160570'),
		('1460','Hyundai','Elantra','2006','1FTSW3B5XAE920608'),
		('1461','Kia','Sedona','2010','JH4DC23931S912415'),
		('1462','Chevrolet','Cavalier','1995','WA1LGAFE3DD141607'),
		('1463','Mercury','Mountaineer','2002','1G6AJ5SX8D0010857'),
		('1464','Mitsubishi','Outlander Sport','2011','2B3CL3CG8BH757257'),
		('1465','Ford','Mustang','1984','1FTEX1C88AF043487'),
		('1466','Acura','RSX','2005','1B3CB1HA6AD366700'),
		('1467','Cadillac','XLR','2009','1G6DU6EVXA0196448'),
		('1468','Suzuki','XL-7','2005','1FTWW3B53AE680898'),
		('1469','Suzuki','Sidekick','1997','1FMJK1F56AE533958'),
		('1470','BMW','Z4','2011','1G6KS54Y12U214431'),
		('1471','Toyota','Echo','2001','1FTEW1C88FK581222'),
		('1472','Ford','Edge','2012','WAUCVAFR1CA100212'),
		('1473','Honda','CR-Z','2011','2G4WS52J551654104'),
		('1474','Morgan','Aero 8','2006','5UXFE835X8L962624'),
		('1475','Land Rover','Range Rover','2008','WBAEP334X5P180553'),
		('1476','Oldsmobile','Alero','2004','3VW467AT9DM512499'),
		('1477','Volvo','S60','2007','3VWJX7AJ2AM600286'),
		('1478','Subaru','Outback','2002','1HGCR2E38FA900621'),
		('1479','Ford','Crown Victoria','1994','1GYFC332X9R238814'),
		('1480','Nissan','Maxima','1993','WAUKF98E18A552959'),
		('1481','Mazda','626','1995','SALFR2BN2CH645235'),
		('1482','Toyota','Prius','2012','3FA6P0LU7ER597374'),
		('1483','Infiniti','J','1993','KNAFX6A83F5061168'),
		('1484','Suzuki','SJ','1994','3VWC17AU8FM538338'),
		('1485','Mazda','B-Series','2007','YV1902AH7B1179345'),
		('1486','Subaru','Impreza','2009','1N6AD0CW5EN353074'),
		('1487','Suzuki','Grand Vitara','2001','5UXZV4C50BL511005'),
		('1488','Chevrolet','Silverado 1500','2000','JTHBK1EG3B2767958'),
		('1489','Volkswagen','Golf','1993','WA1DGAFP1DA549076'),
		('1490','Audi','Q7','2009','1C6RD6LP0CS883993'),
		('1491','Chrysler','Town & Country','1997','WAUGL78EX5A751801'),
		('1492','Toyota','MR2','1993','1N6AF0KY5FN039486'),
		('1493','Audi','A6','1998','1GYS3FEJ5DR535857'),
		('1494','Oldsmobile','88','1997','NM0AE8F74F1246011'),
		('1495','Ford','Fiesta','2012','1G6KE57Y93U185393'),
		('1496','Chevrolet','Impala','1995','JTHDU1EF4D5923730'),
		('1497','Volkswagen','CC','2013','WBADN534X2G974378'),
		('1498','Chevrolet','G-Series G20','1995','WAUAFAFH4CN010587')
	end
'''