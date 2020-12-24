from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import csv
import datetime
import re

engine = create_engine('sqlite:///../db/data.db', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()
class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin2 = Column(String)
    state = Column(String)
    country = Column(String)
    country_code = Column(String)
    date = Column(DateTime)
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)
    active = Column(Integer)
    key = Column(String)

Base.metadata.create_all(engine)

#Let us first build the country code map
country_codes = {}
with open('maps\\country.txt') as country_map_file:
    country_csv_reader = csv.reader(country_map_file, delimiter=',')
    for row in country_csv_reader:
        country_codes[row[0]] = row[1]
print(country_codes)

files = os.listdir(os.path.dirname(os.path.realpath('__file__')) + '\\..\\data\\johns_hopkins\\csse_covid_19_data\\csse_covid_19_daily_reports') # Get list of files in daily reports dir
for file in files:
    if file.endswith(".csv"):
        month = int(file[0:2])
        day=int(file[3:5])
        year=int(file[6:10])
        filedate=datetime.datetime(year,month,day)
        print("File:" + file)
        data_add = None
        with open('..\\data\\johns_hopkins\\csse_covid_19_data\\csse_covid_19_daily_reports\\' + file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[0] != 'FIPS' and row[0] != 'Province/State':
                    if len(row) == 6 and row[2].split()[0] != 'Last':
                        data_add= Data(
                            admin2='',
                            state=row[0],
                            country=row[1],
                            date=filedate,
                            confirmed = row[3],
                            deaths = row[4],
                            recovered = row[5],
                            active=0,
                            key = row[0] + ' ' + row[1] + ' ' + row[2]
                        )
                        #session.add(data_add)
                    elif len(row) == 8:
                        data_add= Data(
                            admin2='',
                            state=row[0],
                            country=row[1],
                            date=filedate,
                            confirmed = row[3],
                            deaths = row[4],
                            recovered = row[5],
                            active=0,
                            key = row[0] + ' ' + row[1] + ' ' + row[2]
                        )
                        #session.add(data_add)
                    elif len(row) == 12:
                        data_add = Data(
                            admin2 = row[1],
                            state = row[2],
                            country = row[3],
                            date = filedate,
                            confirmed= row[7],
                            deaths = row[8],
                            recovered = row[9],
                            active = row[10],
                            key = row[11] + ' ' + row[4]
                        )
                    elif len(row) == 14:
                        data_add = Data(
                            admin2 = row[1],
                            state = row[2],
                            country = row[3],
                            date = filedate,
                            confirmed= row[7],
                            deaths = row[8],
                            recovered = row[9],
                            active = row[10],
                            key = row[11] + ' ' + row[4]
                        )
                    else:
                        print("Unexpected length")
                    country_code = ''
                    if data_add != None:
                        data_add.country = data_add.country.strip()
                        if data_add.country in country_codes:
                            country_code = country_codes[data_add.country]
                        data_add.country_code = country_code
                        session.add(data_add)
                    
                    #if data_add == None: session.add(data_add)
            session.commit()