# !/usr/bin/python
# random_forest.py
# Author: Nati Ramos
# Date: 25-March-2018
# About: Implementing Random Forest classifier to predict new Operators for Atmosphere

# Required Python Packages:
import json
import os
import io

from pyflightdata import FlightData

from main import data_stored
from main import pre_machine_learning
from main import random_forest_classifier

# File paths and conditions of the study
data_dir = "/home/atm-wessling2/Desktop/Short term tareas/ADSB/ADSB_v.0.2/"
name_file = "France_july"
vv_countries = "Switzerland"
military = "n"

# longitude_min = input("Min Long :: ")
# longitude_max = input("Max Long :: ")
# latitude_min = input("Min Lat :: ")
# latitude_max = input("Max Lat :: ")

VECTOR_DAYS = [
    "2017-07-01", "2017-07-02", "2017-07-03", "2017-07-04", "2017-07-05",
    "2017-07-06", "2017-07-07", "2017-07-08", "2017-07-09", "2017-07-10", "2017-07-11",
    "2017-07-12", "2017-07-13", "2017-07-14", "2017-07-15", "2017-07-16", "2017-07-17",
    "2017-07-18", "2017-07-19", "2017-07-20", "2017-07-21", "2017-07-22", "2017-07-23",
    "2017-07-24", "2017-07-25", "2017-07-26", "2017-07-27", "2017-07-28", "2017-07-29",
    "2017-07-30", "2017-07-31"
]

# Creation of a list of airlines from FR24
fr = FlightData()
all_airlines = fr.get_airlines()
airlines_list = []
for airline_info in all_airlines:
    airlines_list.append(airline_info['title'])

helicopter_list = []
aircraft_list = []

for day in VECTOR_DAYS:
    data_dir2 = data_dir + "JUL_2017/" + day + "/"
    data_stored(data_dir2, name_file, vv_countries, military)
    try:
        pre_machine_learning(name_file)
        random_forest_classifier(name_file)
        file_to_study = io.open("surveil_final_" + name_file + ".txt" , 'r', encoding='utf8')
        data_to_study_json = file_to_study.read()
        data_to_study = json.loads(data_to_study_json)
        file_to_study.close()
        for aircraft in data_to_study.keys():
            if data_to_study[aircraft]['Species'] == 4 :
                if (data_to_study[aircraft]['Operator'] not in helicopter_list) :
                    helicopter_list.append(data_to_study[aircraft]['Operator'])
        for aircraft in data_to_study.keys():
            if data_to_study[aircraft]['Species'] == 1 :
                if (data_to_study[aircraft]['Operator'] not in aircraft_list) :
                    aircraft_list.append(data_to_study[aircraft]['Operator'])
        os.remove(name_file + '_ML.txt')
        os.remove(name_file + '.txt')
    except ValueError:
        continue

with open("helicopter_" + name_file + ".txt","w") as file_helicopter_july:
    for item in helicopter_list:
        if item not in airlines_list:
            file_helicopter_july.write('%s\n'% item)

with open("aircraft_" + name_file + ".txt","w") as file_aircraft_july:
    for item in aircraft_list:
        if item not in airlines_list:
            file_aircraft_july.write('%s\n'% item)
