# !/usr/bin/python
# random_forest.py
# Author: Nati Ramos
# Date: 25-May-2018
# About: WMO Study ATMOSPHERE

# Required Python Packages:
from wmo_research import data_stored
from wmo_research import data_airports
from wmo_research import main_algorithm
from wmo_research import pour_sophie
from wmo_research import graphicalComparison

# File paths and conditions of the study:
data_dir = "/home/atm-wessling2/Desktop/adsb_code/2018-06-21/"
file_airport = "/home/atm-wessling2/Downloads/madis_airports.txt"
file_airline = "airlines_AUSTRALIA.txt"
name_file = "wmo_study_Australia"  # How I want to name my file with the data from the flights

# Construct the list of airlines under interest:
VV_AIRLINES = []
with open(file_airline, 'r') as file:
    for line in file:
        print line
        index = line.find("\n")
        VV_AIRLINES.append(line[0:index].upper())

# Definition of the geographical region that we will investigate. In this study, USA
latitude_max = 0  #55  #50
latitude_min = -60  #30  #10
longitude_max = 180  #-100  #-45
longitude_min = 100  #-140  #-170

# Launch the files:
# data_stored(data_dir, name_file, latitude_min, latitude_max,
#               longitude_min, longitude_max, VV_AIRLINES) # It generates a file with the information of flights, that
# will be called in the next steps. If the file with the information has already been obtained, this function should
# be commented to save time.
airport_by_icao = data_airports(file_airport) # Build the list of airports, from the file that Sophie gave me
(amdar_report_list, altitude_list) = main_algorithm(airport_by_icao, name_file) # Main algorithm that generates the airports of
# departure and arrival of the airplanes
# pour_sophie(ordered_amdar_by_time) # It generates the json files for Sophie
# graphicalComparison(airport_counter, airport_by_icao)