from asyncio import events
from operator import index
from re import S
from unittest import result
import fastf1
from fastf1 import plotting
import glob
import os
import pandas as pd
from requests import session

fastf1.Cache.enable_cache('/home/nickolas/Documents/VSCode/Python/cache')   

# Add new race names into this list, then run the program again, to update the data. 
race_names = (
    "FORMULA 1 GULF AIR BAHRAIN GRAND PRIX 2022",
    "FORMULA 1 STC SAUDI ARABIAN GRAND PRIX 2022",
    "FORMULA 1 HEINEKEN AUSTRALIAN GRAND PRIX 2022",
    "FORMULA 1 ROLEX GRAN PREMIO DEL MADE IN ITALY E DELL'EMILIA-ROMAGNA 2022",
    "FORMULA 1 CRYPTO.COM MIAMI GRAND PRIX 2022",
    "FORMULA 1 PIRELLI GRAN PREMIO DE ESPAÑA 2022",
    "FORMULA 1 GRAND PRIX DE MONACO 2022",
    "FORMULA 1 AZERBAIJAN GRAND PRIX 2022",
    "FORMULA 1 AWS GRAND PRIX DU CANADA 2022",
    "FORMULA 1 LENOVO BRITISH GRAND PRIX 2022",
    "FORMULA 1 ROLEX GROSSER PREIS VON ÖSTERREICH 2022",
    "FORMULA 1 LENOVO GRAND PRIX DE FRANCE 2022",
    "FORMULA 1 ARAMCO MAGYAR NAGYDÍJ 2022",
    "FORMULA 1 ROLEX BELGIAN GRAND PRIX 2022",
    "FORMULA 1 HEINEKEN DUTCH GRAND PRIX 2022",
    "FORMULA 1 PIRELLI GRAN PREMIO D’ITALIA 2022",
    "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2022",
    "FORMULA 1 HONDA JAPANESE GRAND PRIX 2022",
    "FORMULA 1 ARAMCO UNITED STATES GRAND PRIX 2022",
    "FORMULA 1 GRAN PREMIO DE LA CIUDAD DE MÉXICO 2022"
)

def raceScraper(year, race_names, type):
    raceItr = 1
    for x in race_names:
     race = fastf1.get_session(year, x, type)
     race.load()
     results = race.results
     results.drop(labels = ['BroadcastName', 'Abbreviation', 'TeamColor', 'FullName', 'GridPosition', 'Q1', 'Q2', 'Q3'], axis = 1, inplace = True)
     results.to_csv('Race ' + x + '.csv', index = False)
     results.head()
     results.insert(5,column="RaceID", value=raceItr)
     results.head()
     results.to_csv('Race ' + x + '.csv', index = False)
     raceItr = raceItr + 1

raceScraper(2022, race_names, 'R')

def qualifyingScraper(year, race_names, type):
    qualItr = 1
    for x in race_names:
     race = fastf1.get_session(year, x, type)
     race.load()
     results = race.results
     results.drop(labels = ['BroadcastName', 'Abbreviation', 'TeamColor', 'FullName', 'GridPosition', 'Time', 'Status', 'Points'], axis = 1, inplace = True)
     results.head()
     results.insert(5,column="RaceID", value=qualItr)
     results.head()
     results.to_csv('Qualifying ' + x + '.csv', index = False)
     qualItr = qualItr + 1

qualifyingScraper(2022, race_names, 'Q')

def p1Scraper(year, race_names, type):
    p1Itr = 1
    for x in race_names:
     race = fastf1.get_session(year, x, type)
     race.load()
     results = race.results
     results.drop(labels = ['BroadcastName', 'Abbreviation', 'TeamColor', 'FullName', 'Position', 'GridPosition', 'Q1', 'Q2', 'Q3', 'Status', 'Points'], axis = 1, inplace = True)
     results.to_csv('P1 ' + x + '.csv', index = False)
     results.insert(5, column="SessionID", value="1")
     results.insert(6,column="RaceID", value=p1Itr)
     results.head()
     results.to_csv('P1 ' + x + '.csv', index = False)
     p1Itr = p1Itr + 1
 
p1Scraper(2022, race_names, 'FP1')

def p2Scraper(year, race_names, type):
    p2Itr = 1
    for x in race_names:
     race = fastf1.get_session(year, x, type)
     race.load()
     results = race.results
     results.drop(labels = ['BroadcastName', 'Abbreviation', 'TeamColor', 'FullName', 'Position', 'GridPosition', 'Q1', 'Q2', 'Q3', 'Status', 'Points'], axis = 1, inplace = True)
     results.head()
     results.insert(5, column="SessionID", value="2")
     results.insert(6,column="RaceID", value=p2Itr)
     results.head()
     results.to_csv('P2 ' + x + '.csv', index = False)
     p2Itr = p2Itr + 1

p2Scraper(2022, race_names, 'FP2')

def p3Scraper(year, race_names, type):
    p3Itr = 1
    for x in race_names:
     if x == "FORMULA 1 ROLEX GRAN PREMIO DEL MADE IN ITALY E DELL'EMILIA-ROMAGNA 2022":
        continue
     elif x == "FORMULA 1 ROLEX GROSSER PREIS VON ÖSTERREICH 2022":
        continue
     race = fastf1.get_session(year, x, type)
     race.load()
     results = race.results
     results.drop(labels = ['BroadcastName', 'Abbreviation', 'TeamColor', 'FullName', 'Position', 'GridPosition', 'Q1', 'Q2', 'Q3', 'Status', 'Points'], axis = 1, inplace = True)
     results.head()
     results.insert(5, column="SessionID", value="3")
     results.insert(6,column="RaceID", value=p3Itr)
     results.head()
     results.to_csv('P3 ' + x + '.csv', index = False)
     p3Itr = p3Itr + 1

p3Scraper(2022, race_names, 'FP3')

def combineRace():
    raceTable = os.path.join("", "Race *.csv")
    raceTable = glob.glob(raceTable)
    df = pd.concat(map(pd.read_csv, raceTable))
    df['TeamName'] = df['TeamName'].str.replace("Red Bull Racing", "0")
    df['TeamName'] = df['TeamName'].str.replace("Ferrari", "1")
    df['TeamName'] = df['TeamName'].str.replace("Mercedes", "2")
    df['TeamName'] = df['TeamName'].str.replace("Alpine", "3")
    df['TeamName'] = df['TeamName'].str.replace("McLaren", "4")
    df['TeamName'] = df['TeamName'].str.replace("Alfa Romeo", "6")
    df['TeamName'] = df['TeamName'].str.replace("Aston Martin", "6")
    df['TeamName'] = df['TeamName'].str.replace("Haas F1 Team", "7")
    df['TeamName'] = df['TeamName'].str.replace("AlphaTauri", "8")
    df['TeamName'] = df['TeamName'].str.replace("Williams", "9")
    df['Time'] = df['Time'].str.replace("0 days ","")
    df = df.rename(columns={'TeamName': 'ConstructorID'})
    df = df.rename(columns={'Time': 'RaceTime'})
    df.to_csv("tables/raceResults.csv", sep=',', encoding='utf-8', index=False)

combineRace()

def combinePractice():
    raceTable = os.path.join("", "P*.csv")
    raceTable = glob.glob(raceTable)
    df = pd.concat(map(pd.read_csv, raceTable))
    df['TeamName'] = df['TeamName'].str.replace("Red Bull Racing", "0")
    df['TeamName'] = df['TeamName'].str.replace("Ferrari", "1")
    df['TeamName'] = df['TeamName'].str.replace("Mercedes", "2")
    df['TeamName'] = df['TeamName'].str.replace("Alpine", "3")
    df['TeamName'] = df['TeamName'].str.replace("McLaren", "4")
    df['TeamName'] = df['TeamName'].str.replace("Alfa Romeo", "6")
    df['TeamName'] = df['TeamName'].str.replace("Aston Martin", "6")
    df['TeamName'] = df['TeamName'].str.replace("Haas F1 Team", "7")
    df['TeamName'] = df['TeamName'].str.replace("AlphaTauri", "8")
    df['TeamName'] = df['TeamName'].str.replace("Williams", "9")
    df = df.rename(columns={'TeamName': 'ConstructorID'})
    df.to_csv("tables/practiceResults.csv", sep=',', encoding='utf-8', index=False)

combinePractice()

def combineQualifying():
    raceTable = os.path.join("", "Qualifying *.csv")
    raceTable = glob.glob(raceTable)
    df = pd.concat(map(pd.read_csv, raceTable))
    df['TeamName'] = df['TeamName'].str.replace("Red Bull Racing", "0")
    df['TeamName'] = df['TeamName'].str.replace("Ferrari", "1")
    df['TeamName'] = df['TeamName'].str.replace("Mercedes", "2")
    df['TeamName'] = df['TeamName'].str.replace("Alpine", "3")
    df['TeamName'] = df['TeamName'].str.replace("McLaren", "4")
    df['TeamName'] = df['TeamName'].str.replace("Alfa Romeo", "6")
    df['TeamName'] = df['TeamName'].str.replace("Aston Martin", "6")
    df['TeamName'] = df['TeamName'].str.replace("Haas F1 Team", "7")
    df['TeamName'] = df['TeamName'].str.replace("AlphaTauri", "8")
    df['TeamName'] = df['TeamName'].str.replace("Williams", "9")
    df['Q1'] = df['Q1'].str.replace("0 days ","")
    df['Q2'] = df['Q2'].str.replace("0 days ","")
    df['Q3'] = df['Q3'].str.replace("0 days ","")
    df = df.rename(columns={'TeamName': 'ConstructorID'})
    df.to_csv("tables/qualifyingResults.csv", sep=',', encoding='utf-8', index=False)

combineQualifying()

def combineDrivers():
    dfRace = pd.read_csv('tables/raceResults.csv')
    dfQualifying = pd.read_csv('tables/qualifyingResults.csv')
    dfPractice = pd.read_csv('tables/practiceResults.csv')
    list=[dfRace,dfQualifying,dfPractice]
    result = pd.concat(list)
    result = result.drop_duplicates(subset=['FirstName','LastName'])
    result.drop(labels=['Position', 'Time', 'Status', 'Q1', 'Q2', 'Q3', 'Points'], axis = 1, inplace = True)
    result.to_csv("tables/drivers.csv", sep=',', encoding='utf-8', index=False)

combineDrivers()

# Edited out because it is easier to copy from Formula1.com
# def combineConstructors():
#     dfRace = pd.read_csv('tables/raceResults.csv')
#     dfQualifying = pd.read_csv('tables/qualifyingResults.csv')
#     dfPractice = pd.read_csv('tables/practiceResults.csv')
#     list=[dfRace,dfQualifying,dfPractice]
#     result = pd.concat(list)
#     result = result.drop_duplicates(subset=['TeamName'])
#     result.drop(labels=['Position', 'Time', 'Status', 'Q1', 'Q2', 'Q3', 'DriverNumber', 'Points', 'FirstName', 'LastName', ], axis = 1, inplace = True)
#     result.to_csv("tables/constructors.csv", sep=',', encoding='utf-8', index=False)

#combineConstructors()

def eventScraper(year, race_names):
    eventDictionary = {"RoundNumber":[], "OfficialName":[], "Country":[], "Location":[], "EventDate":[]}
    for x in race_names:
     event = fastf1.get_event(year, x)
     eventDictionary["RoundNumber"].append(event[0])
     eventDictionary["OfficialName"].append(event[3])
     eventDictionary["Country"].append(event[1])
     eventDictionary["Location"].append(event[2])
     eventDictionary["EventDate"].append(event[4])
    
    df = pd.DataFrame(data=eventDictionary)
    df.to_csv("tables/events.csv", sep=',', encoding='utf-8', index=False)

#eventScraper(2022, race_names)
