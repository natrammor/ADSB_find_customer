# !/usr/bin/python
# random_forest.py
# Author: Nati Ramos
# Date: 25-March-2018
# About: Implementing Random Forest classifier to predict new Operators for Atmosphere

# Required Python Packages:
import json
import urllib
import urllib2
import logging
import os
import time
import io
import sys
import numpy
import math
import matplotlib.pyplot as plt
import pandas
import scipy
import seaborn as sns
import re

from datetime import datetime
from sklearn import model_selection, metrics, preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score

from main import numericalSort
from main import data_stored
from main import pre_machine_learning
from main import random_forest_classifier

# File paths and conditions of the study
data_dir = "/home/atm-wessling2/Desktop/adsb_code/"
name_file = "Japan_may"
vv_countries = "Japan"
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
    "2017-05-01", "2017-05-02", "2017-05-03", "2017-05-04", "2017-05-05",
    "2017-05-06", "2017-05-07", "2017-05-08", "2017-05-09", "2017-05-10", "2017-05-11",
    "2017-05-12", "2017-05-13", "2017-05-14", "2017-05-15", "2017-05-16", "2017-05-17",
    "2017-05-18", "2017-05-19", "2017-05-20", "2017-05-21", "2017-05-22", "2017-05-23",
    "2017-05-24", "2017-05-25", "2017-05-26", "2017-05-27", "2017-05-28", "2017-05-29",
    "2017-05-30", "2017-05-31"
]
VECTOR_DAYS = ["2017-05-01"]
helicopter_list = []
aircraft_list = []

for day in VECTOR_DAYS:
	data_dir2 = data_dir + "MAY_2017/" + day + "/"
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
				if data_to_study[aircraft]['Operator'] not in aircraft_list:
					aircraft_list.append(data_to_study[aircraft]['Operator'])
		os.remove(name_file + '_ML.txt')
		os.remove(name_file + '.txt')
	except ValueError:
		continue

with io.open("helicopter.txt","w", encoding='utf8') as file_helicopter_may:
	for item in helicopter_list:
		file_helicopter_may.write('%s\n'% item)

with io.open("aircraft.txt","w", encoding='utf8') as file_aircraft_may:
	for item in aircraft_list:
		file_aircraft_may.write('%s\n'% item)
