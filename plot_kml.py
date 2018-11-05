import simplekml
import json
from datetime import datetime
import sys
import time
import io

#Preparing the structure of the kml file:
kml_file_structure = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" >

<Document>
<name>Tracking</name>
<Style id="position">
    <IconStyle>
        <color>7f00ffff</color>
        <colorMode>normal</colorMode>
        <scale>0.5</scale>
        <Icon>
            <href>http://maps.google.com/mapfiles/kml/pal4/icon25.png</href>
        </Icon>
    </IconStyle>
</Style>
<Style id="traject">
    <LineStyle>
        <color>7f00ffff</color>
        <width>2</width>
    </LineStyle>
    <PolyStyle>
        <color>7f00ff00</color>
    </PolyStyle>
    <IconStyle>
        <scale>1.0</scale>
        <Icon>
            <href>http://maps.google.com/mapfiles/kml/pal2/icon56.png</href>
        </Icon>
    </IconStyle>
</Style>
%s

</Document>
</kml>"""

kml_placemark_structure = """<Placemark>
    <name>%s</name>
    <styleUrl>#traject</styleUrl>
    <gx:balloonVisibility>1</gx:balloonVisibility>
    <gx:Track id="%s">
      <altitudeMode>absolute</altitudeMode>
      <extrude>1</extrude>
      <tessellate>0</tessellate>
      %s
    </gx:Track>
    <ExtendedData>
      <Data name="string">
        <displayName>Operator</displayName>
        <value><![CDATA[%s]]></value>
      </Data>
    </ExtendedData>
</Placemark>"""

#<Data name="string">
#        <displayName>Model</displayName>
#        <value><![CDATA[%s]]></value>
#      </Data>

kml_observation_structure = """<when>%s</when>
      <gx:coord>%s %s %s</gx:coord>
      <gx:angles>%s</gx:angles>"""

# BUILD THE KML FILE:

#Charge the data:
file = raw_input("Directory of the json file to transform to KML:")
f = io.open(file, 'r', encoding='utf8')
data_json = f.read()
aircraft_list = json.loads(data_json)
f.close()

kml_file = io.open(file[0:len(file)-4] + "_kml.kml","w",encoding='utf8')
placemark_buf = ""

count = 0
notrack_icao = 0

for aircraft in aircraft_list.keys():
  #if aircraft_list[aircraft]['Operator'] != "":
    tracking_buf = "--"
    time_list = []
    for obs in aircraft_list[aircraft]['Positions']:
        time_list.append(str(obs['time']/1000))	#seg
        count+=1
        print count
        utc_time = datetime.utcfromtimestamp(obs['time']/1000)
        new_obs =  kml_observation_structure % (utc_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                                str(obs['longitude']), str(obs['latitude']), str(obs['altitude']),
                                                str(obs['heading']))
        tracking_buf += new_obs
    new_placemark = kml_placemark_structure % (aircraft, aircraft, tracking_buf, aircraft_list[aircraft]['Operator'])
                                               #aircraft_list[aircraft]['Model']
    placemark_buf +=  new_placemark
    if len(aircraft_list[aircraft]['Positions']) == 0:
        notrack_icao+=1
kml_file.write(kml_file_structure % placemark_buf)
kml_file.close()

print "Number of Icao without track: %d / %d " % (notrack_icao, len(aircraft_list))

