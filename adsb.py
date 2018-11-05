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
data_dir = "/home/atm-wessling2/Desktop/adsb_code/MAY_2017/2017-05-25/"
name_file = "Jules"
vv_countries = "France"
military = "n"
model = "DAHER"
#data_dir = raw_input("Which is the directory of the stored data? :: ")
#name_file = raw_input("How do you want to name your output file? :: ")
#vv_countries = raw_input("Write the VECTOR of the desired Registration Countries :: ")
#military = raw_input("Military flight? (y/n) :: ")
longitude_min = -10 #input("Min Long :: ")
longitude_max = 65 #input("Max Long :: ")
#latitude_min = 20 #input("Min Lat :: ")
#latitude_max = input("Max Lat :: ")

data_stored(data_dir, name_file, vv_countries, military, longitude_min, longitude_max, model)#, latitude_min, latitude_max)
#pre_machine_learning(name_file)
#random_forest_classifier(name_file)

#os.remove(name_file + "_ML.txt")
