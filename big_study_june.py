# !/usr/bin/python
# random_forest.py
# Author: Nati Ramos
# Date: 25-March-2018
# About: Implementing Random Forest classifier to predict new Operators for Atmosphere

# Required Python Packages:
import json
import os
import io
import csv

from main import data_stored
from main import pre_machine_learning
from main import random_forest_classifier

from pyflightdata import FlightData

# File paths and conditions of the study
data_dir = "/home/atm-wessling2/Desktop/Short term tareas/ADSB/ADSB_v.0.2/"
name_file = "USA_june"
vv_countries = "United States"
military = "n"

# data_dir = raw_input("Which is the directory of the stored data? :: ")
# name_file = raw_input("How do you want to name your output file? :: ")
# vv_countries = raw_input("Write the VECTOR of the desired Registration Countries :: ")
# military = raw_input("Military flight? (y/n) :: ")

# longitude_min = input("Min Long :: ")
# longitude_max = input("Max Long :: ")
# latitude_min = input("Min Lat :: ")
# latitude_max = input("Max Lat :: ")

VECTOR_DAYS = [
    "2017-06-01"]
"""
    , "2017-06-02", "2017-06-03", "2017-06-04", "2017-06-05",
    "2017-06-06", "2017-06-07", "2017-06-08", "2017-06-09", "2017-06-10", "2017-06-11",
    "2017-06-12", "2017-06-13", "2017-06-14", "2017-06-15", "2017-06-16", "2017-06-17",
    "2017-06-18", "2017-06-19", "2017-06-20", "2017-06-21", "2017-06-22", "2017-06-23",
    "2017-06-24", "2017-06-25", "2017-06-26", "2017-06-27", "2017-06-28", "2017-06-29",
    "2017-06-30"
]
"""

# Creation of a list of airlines from FR24
fr = FlightData()
all_airlines = fr.get_airlines()
airlines_list = []
for airline_info in all_airlines:
    airlines_list.append(airline_info['title'])

helicopter_list = []
aircraft_list = []
with open('names.csv', 'w') as csvfile:
    for day in VECTOR_DAYS:
        data_dir2 = data_dir + "JUN_2017/" + day + "/"
        data_stored(data_dir2, name_file, vv_countries, military)
        try:
            pre_machine_learning(name_file)
            random_forest_classifier(name_file)
            file_to_study = io.open("surveil_final_" + name_file + ".txt" , 'r', encoding='utf8')
            data_to_study_json = file_to_study.read()
            data_to_study = json.loads(data_to_study_json)
            file_to_study.close()
            for aircraft in data_to_study.keys():
                if data_to_study[aircraft]['Operator'] in airlines_list:

                        fieldnames = ['Operator', 'Registration', '']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                        writer.writeheader()
                        writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
                        writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
                        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

            os.remove(name_file + '_ML.txt')
            os.remove(name_file + '.txt')
        except ValueError:
            continue


