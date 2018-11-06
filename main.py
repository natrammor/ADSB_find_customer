import json
import logging
import os
import io
import numpy
import math
import pandas
import re

from pyflightdata import FlightData

from datetime import datetime
from sklearn.ensemble import RandomForestClassifier


def numericalSort(value):
    """

    :param value:
    :return:
    """
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])

    return parts


def data_stored(data_dir, name_file, vv_countries, military):
    """

    :param data_dir:
    :param name_file:
    :param vv_countries:
    :param military:
    :return:
    """
    if military == "y":
        discard_military_flights = False
        discard_civilian_flights = True
    elif military == "n":
        discard_military_flights = True
        discard_civilian_flights = False
    else:
        discard_military_flights = False
        discard_civilian_flights = False

    aircraft_by_icao = {}

    fr = FlightData()
    all_airlines = fr.get_airlines()
    airlines_list = []
    for airline_info in all_airlines:
        airlines_list.append(airline_info['title'])

    for file in sorted(os.listdir(data_dir), key=numericalSort):
        print(file)
        file_adsbexchange = io.open(data_dir + file, 'r', encoding='utf8')
        data_adsbexchange_json = file_adsbexchange.read()

        try:
            data_adsbexchange = json.loads(data_adsbexchange_json)
            file_adsbexchange.close()

        except ValueError:
            data_adsbexchange = {'acList': {}}
            file_adsbexchange.close()
            print("ERROR")

        for aircraft in data_adsbexchange['acList']:
            try:
                if "Op" not in aircraft:
                    continue
                op = aircraft["Op"]
                if any (element.upper() in op.upper() for element in airlines_list):
                #    print(op)
                    continue
                if aircraft.get("Cou", "Unknown country") not in vv_countries:
                    continue
                if any(forbidden_word in op.upper() for forbidden_word in ("AIRLINE", "AIRWAY", "TRAINING")):
                    continue
                is_military = aircraft["Mil"] and aircraft["Mil"] != "false"
                if discard_military_flights and is_military:
                    continue
                if discard_civilian_flights and not is_military:
                    continue
                #if aircraft.get("Lat") < 20: #not in range(latitude_min, latitude_max):
                #    continue
                   # if range_latitudes is not None:
                #    continue
                #if aircraft.get("Long") < longitude_min or aircraft.get("Long") > longitude_max:
                    #if range_longitudes is not None:
                #    continue

                #departure = aircraft.get("From", "Unknown aiport")
                #arrival = aircraft.get("To", "Unknown airport")

                #if any(forbidden_airport in departure or forbidden_airport in arrival
                #       for forbidden_airport in VV_AIRPORTS):
                #    continue

                if aircraft['Icao'] in aircraft_by_icao:
                    record = aircraft_by_icao[aircraft['Icao']]
                else:
                    record = {}
                    aircraft_by_icao[aircraft['Icao']] = record

                record['Model'] = aircraft.get('Mdl', '')
                record['Operator'] = aircraft.get('Op', '')
                record['Species'] = aircraft.get('Species', '')
                record['Interested'] = aircraft.get('Interested', '')
                record['Reg'] = aircraft.get('Reg', '')
                record['Country'] = aircraft.get('Cou', '')

                if 'Positions' not in record:
                    record['Positions'] = []

                record['Positions'].append(
                    {'latitude': aircraft.get('Lat', ''), 'longitude': aircraft.get('Long', ''),
                     'heading': aircraft.get('Trak', ''), 'altitude': aircraft.get('Alt', ''),
                     'time': aircraft.get('PosTime', int(
                         datetime.strptime(os.path.splitext(file)[0], '%Y-%m-%d-%H%MZ').strftime("%s")) * 1000)})

            except Exception as e:
                logging.exception(aircraft)
                pass

    with open(name_file + ".txt", "w") as first_filtered_file:
        json.dump(aircraft_by_icao, first_filtered_file)

    return ()


def pre_machine_learning(name_file):
    R_EARTH = 6371
    with io.open(name_file + ".txt", 'r', encoding='utf8') as first_filtered_file:
        aircraft_by_icao = json.load(first_filtered_file)
        #print(aircraft_by_icao.keys())

    with io.open(name_file + "_ML.txt", "w", encoding='utf8') as file_machine_learning:
        for aircraft_icao, aircraft in aircraft_by_icao.items():
            #print(aircraft_icao)
            latitude_list = []
            longitude_list = []
            heading_list = []
            altitude_list = []
            time_list = []
            for obs in aircraft['Positions']:
                if obs['latitude'] and obs['longitude'] and obs['altitude'] and obs['heading'] and obs['time']:
                    latitude_list.append(float(obs['latitude']))
                    longitude_list.append(float(obs['longitude']))
                    altitude_list.append(float(obs['altitude']))
                    heading_list.append(float(obs['heading']))
                    time_list.append(float(obs['time']) / 1000.)

            if any(len(list) < 5 for list in (latitude_list, longitude_list, altitude_list, heading_list)):
                continue
            # Definition of the RF parameters:
            min_latitude_radian = min(latitude_list) * math.pi / 180
            max_latitude_radian = max(latitude_list) * math.pi / 180
            min_longitude_radian = min(longitude_list) * math.pi / 180
            max_longitude_radian = max(longitude_list) * math.pi / 180
            box = R_EARTH ** 2 * (max_latitude_radian - min_latitude_radian) \
                  * (max_longitude_radian - min_longitude_radian)
            duration = (float(time_list[-1]) - float(time_list[0])) / 60
            median_alt = numpy.median(altitude_list)
            dev_std_heading = numpy.std(heading_list)
            # Flights that are shorter than 2 hours are not of interest
            if duration < 120:
                continue
            file_machine_learning.write("%s,%s,%s,%s,%s,%s,%s\n" % (
                aircraft['Operator'].replace(",", ""), aircraft_icao, duration,
                box, median_alt, dev_std_heading, 'other'))
    return ()


def random_forest_classifier(name_file):
    names_training = ['operator', 'duration', 'box', 'altitude', 'heading', 'class']
    training_dataset = pandas.read_csv('/home/atm-wessling2/Desktop/ADSB_find_customer/surveil_other_database.csv',
                                       names=names_training)
    parameters = training_dataset.values[:, 1:5]
    classes = training_dataset.values[:, 5]
    RandomForestclf = RandomForestClassifier(n_estimators=250, random_state=0)
    RandomForestclf.fit(parameters, classes)
    names_predicting = ['operator', 'icao', 'duration', 'box', 'altitude', 'heading', 'class']
    predicting_dataset = pandas.read_csv('/home/atm-wessling2/Desktop/ADSB_find_customer/' + name_file + "_ML.txt",
                                         names=names_predicting)
    #print(predicting_dataset)
    parameters_prediction = predicting_dataset.values[:, 2:6]
    classes_prediction = RandomForestclf.predict(parameters_prediction)
    predicting_dataset.values[:, 6] = classes_prediction

    with io.open(name_file + ".txt", 'r', encoding='utf8') as first_filtered_file:
        aircraft_by_icao = json.load(first_filtered_file)

    surveil_list = {}
    for aircraft_icao, aircraft in aircraft_by_icao.items():
        if (aircraft_icao, "surveil") not in predicting_dataset.values[:, (1, 6)]:
            continue
        if aircraft_icao in surveil_list:
            record = surveil_list[aircraft_icao]
        else:
            record = {}
            surveil_list[aircraft_icao] = record
        for field_name in ['Model', 'Operator', 'Reg', 'Species', 'Country']:
            record[field_name] = aircraft[field_name]
        for (surveil_icao, surveil_duration) in predicting_dataset.values[:, (1, 2)]:
            if surveil_icao == aircraft_icao:
                try:
                    record['Duration'].append(surveil_duration)  # To add the different flights
                except KeyError:
                    record['Duration'] = [surveil_duration]

    with open("surveil_final_" + name_file + ".txt", "w") as json_file:
        json.dump(surveil_list, json_file)

    return ()
