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
import datetime
import calendar
import numpy

from main import data_stored
from main import pre_machine_learning
from main import random_forest_classifier


# File paths and conditions of the study
data_dir = "/media/atm-wessling2/VERBATIM HD/Data ADSBExchange/"
name_file = "France"
vv_countries = "France"
military = "n"

# data_dir = raw_input("Which is the directory of the stored data? :: ")
# name_file = raw_input("How do you want to name your output file? :: ")
# vv_countries = raw_input("Write the VECTOR of the desired Registration Countries :: ")
# military = raw_input("Military flight? (y/n) :: ")

# longitude_min = input("Min Long :: ")
# longitude_max = input("Max Long :: ")
# latitude_min = input("Min Lat :: ")
# latitude_max = input("Max Lat :: ")

Start_day = datetime.datetime(2017,5,1)
VECTOR_DAYS = [Start_day + datetime.timedelta(days=1*x) for x in range(0, 5)]

aircraft_dict = {}
with open('names.csv', 'w') as csvfile:
    fieldnames = ['Operator', 'Country', 'Specie', 'Model', 'Registration', 'Frequency',
                  'Mean duration']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for date in VECTOR_DAYS:
        month = date.strftime("%B").upper()
        day = date.strftime("_%Y/%Y-%m-%d")
        data_dir2 = data_dir + month + day + "/"
        data_stored(data_dir2, name_file, vv_countries, military)
        try:
            pre_machine_learning(name_file)
            random_forest_classifier(name_file)
            file_to_study = io.open("surveil_final_" + name_file + ".txt" , 'r', encoding='utf8')
            data_to_study_json = file_to_study.read()
            data_to_study = json.loads(data_to_study_json)
            file_to_study.close()
            for aircraft in data_to_study.keys():
                if aircraft in aircraft_dict:
                    record = aircraft_dict[aircraft]
                else:
                    record = {}
                    aircraft_dict[aircraft] = record
                for field_name in ['Model', 'Operator', 'Reg', 'Species', 'Country']:
                    record[field_name] = data_to_study[aircraft][field_name]
                    try:
                        record['Duration'].append(data_to_study[aircraft]['Duration'])  # To add the different flights
                    except KeyError:
                        record['Duration'] = [data_to_study[aircraft]['Duration']]
            os.remove(name_file + '_ML.txt')
            os.remove(name_file + '.txt')
        except ValueError:
            continue
    for aircraft in aircraft_dict.keys():
        registration = aircraft_dict[aircraft]['Reg']
        operator = aircraft_dict[aircraft]['Operator']
        model = aircraft_dict[aircraft]['Model']
        species = aircraft_dict[aircraft]['Species']
        country = aircraft_dict[aircraft]['Country']
        if species == 1:
            specie = "A/C"
        elif species == 4:
            specie = "R/C"
        else:
            continue
        frequency = len(aircraft_dict[aircraft]['Duration'])
        mean_duration = numpy.mean(aircraft_dict[aircraft]['Duration'])
        writer.writerow({'Operator': operator, 'Country': country, 'Specie': specie,
                         'Model': model, 'Registration': registration, 'Frequency': frequency,
                         'Mean duration': mean_duration})


