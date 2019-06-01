#Libraries

#Python Libs
import sys
import os
import glob
from datetime import datetime
import json
import urllib2
import time

#Data Analysis Libs
import pandas as pd
import numpy as np

#Constants
MIN_NUM_ARGS = 4 
first_cols = ['cardNum', 'boarding_datetime','gps_datetime','route','busCode','stopPointId']
boarding_key_cols = ['cardNum','boarding_datetime']
gps_key_cols = ['route','busCode','tripNum','stopPointId']
sort_cols = boarding_key_cols + gps_key_cols[:-1] + ['gps_datetime']
max_match_diff = 1800

#Functions
def get_otp_itineraries(otp_url,o_lat,o_lon,d_lat,d_lon,date,time,verbose=False):
    otp_http_request = 'routers/{}/plan?fromPlace={},{}&toPlace={},{}&mode=TRANSIT,WALK&date={}&time={}&numItineraries=10&maxWalkingDistance=1000'
	
    
    otp_request_url = otp_url + otp_http_request.format(o_lat,o_lon,d_lat,d_lon,date,time)
    if verbose:
        print otp_request_url
    return json.loads(urllib2.urlopen(otp_request_url).read())

def get_otp_suggested_trips(od_matrix,otp_url):
	req_duration = []
	trips_otp_response = {}
	counter = 0
	for index, row in od_matrix.iterrows():
		id=float(row['stopPointId'])
		date = row['gps_datetime'].strftime('%d-%m-%Y')
		start_time = (row['gps_datetime']-pd.Timedelta('2 min')).strftime('%H:%M:%S')
		req_start_time = time.time()
		#UFCG -7.217167, -35.908995
		trip_plan = get_otp_itineraries(otp_url,row['shapeLat'], row['shapeLon'], '-7.217167', '-35.908995', date,start_time)
		req_end_time = time.time()
		req_time = req_end_time - req_start_time
		req_duration.append((id,req_time))
		#print "OTP request took ", req_end_time - req_start_time,"seconds."
		trips_otp_response[id] = trip_plan
		counter+=1

	req_dur_df = pd.DataFrame().from_records(req_duration,columns=['id','duration'])
	print req_dur_df.duration.describe()	

	return trips_otp_response
	

def extract_otp_trips_legs(otp_trips):
	trips_legs = []

	for trip in otp_trips.keys():
		if 'plan' in otp_trips[trip]:
			itinerary_id = 1
			for itinerary in otp_trips[trip]['plan']['itineraries']:
				date = otp_trips[trip]['plan']['date']/1000
				leg_id = 1
				for leg in itinerary['legs']:
					route = leg['route'] if leg['route'] != '' else None
					fromStopId = leg['from']['stopId'].split(':')[1] if leg['mode'] == 'BUS' else None
					toStopId = leg['to']['stopId'].split(':')[1] if leg['mode'] == 'BUS' else None
					start_time = long(leg['startTime'])/1000
					end_time = long(leg['endTime'])/1000
					duration = (end_time - start_time)/60
					trips_legs.append((date,trip,itinerary_id,leg_id,start_time,end_time,leg['mode'],route,fromStopId,toStopId, duration))
					leg_id += 1
				itinerary_id += 1
	return trips_legs

def prepare_otp_legs_df(otp_legs_list):
	labels=['date','user_trip_id','itinerary_id','leg_id','otp_start_time','otp_end_time','mode','route','from_stop_id','to_stop_id','otp_duration_mins']
	return pd.DataFrame.from_records(data=otp_legs_list, columns=labels) \
                    .assign(date = lambda x: pd.to_datetime(x['date'],unit='s').dt.strftime('%Y-%m-%d'),
                            otp_duration_mins = lambda x : (x['otp_end_time'] - x['otp_start_time'])/60,
                            route = lambda x : pd.to_numeric(x['route'],errors='coerce'),
                            from_stop_id = lambda x : pd.to_numeric(x['from_stop_id'],errors='coerce'),
                            to_stop_id = lambda x : pd.to_numeric(x['to_stop_id'],errors='coerce')) \
                    .assign(otp_start_time = lambda x : pd.to_datetime(x['otp_start_time'], unit='s'),
                            otp_end_time = lambda x : pd.to_datetime(x['otp_end_time'], unit='s')) \
                    .sort_values(by=['date','user_trip_id','itinerary_id','otp_start_time'])

	
	
#Main
if __name__ == "__main__":
    if len(sys.argv) < MIN_NUM_ARGS:
        print "Error: Wrong Usage!"
        printUsage()
        sys.exit(1)

user_trips_file = sys.argv[1]
output_folder_path = sys.argv[2]
otp_server_url = sys.argv[3]

print "Processing file", user_trips_file
file_name = user_trips_file.split('/')[-1].replace('.csv','')
file_date = pd.to_datetime(file_name.split('_user_trips_')[0],format='%Y_%m_%d')
if (file_date.dayofweek == 6):
	print "File date is sunday. File will not be processed."
else:
	try:
                
		user_trips = pd.read_csv(user_trips_file, parse_dates=['gps_datetime'])
		# Filtering just trips starting from Hector's home (bus stop)
                gps_trips = user_trips.loc[user_trips['stopPointId'] == '491551']
		otp_suggestions = get_otp_suggested_trips(gps_trips,otp_server_url)
		otp_legs_df = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions))

		otp_legs_df.to_csv(output_folder_path + '/' + file_name + '_otp_itineraries.csv',index=False)
	except Exception as e:
		print e
		print "Error in processing file " + file_name

