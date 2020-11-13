#Libraries

#Python Libs
import sys
import os
import glob
from datetime import datetime
import json
import urllib.request
import time
import os
import requests
import http.client
import threading
import concurrent.futures
import traceback
import logging



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
def printUsage():
	print ("Usage: " + sys.argv[0] + " <enhanced-buste-folder-path> <output-folder-path> <otp-server-url> <initial-date> <final-date>")
	
def get_otp_itineraries(otp_url,o_lat,o_lon,d_lat,d_lon,date,time,route,verbose=False):
	otp_http_request = 'routers/cg/plan?fromPlace={},{}&toPlace={},{}&mode=TRANSIT,WALK&date={}&time={}&numItineraries=500&maxWalkingDistance=1000'
	
	
	otp_request_url = otp_url + otp_http_request.format(o_lat,o_lon,d_lat,d_lon,date.strip(),time,route)
	print(otp_request_url)

	if verbose:
		print (otp_request_url)

	return json.loads(urllib.request.urlopen(otp_request_url).read())

def get_otp_suggested_trips(od_matrix,otp_url,coords_list):
	

	req_duration = []
	trips_otp_response = {}
	counter = 0
	for index, row in od_matrix.iterrows():
		id=float(row['stopPointId'])
		date = row['gps_datetime'].strftime('%Y-%m-%d ')
		
		start_time = (row['gps_datetime']-pd.Timedelta('3 h')-pd.Timedelta('2 min')).strftime('%H:%M:%S')
		
		req_start_time = time.time()
		#UFCG -7.217167, -35.908995
		#print(row['gpsLat'])
		#print(row['gpsLon'])
		#trip_plan = get_itineraries(otp_url,row['shapeLat'], row['shapeLon'], date,start_time, row['route'],bus_matrix)
		trip_plan = get_otp_itineraries(otp_url,row['shapeLat'], row['shapeLon'], coords_list[0], coords_list[1], date,start_time, row['route'])
		#print(trip_plan) 
		req_end_time = time.time()
		req_time = req_end_time - req_start_time
		req_duration.append((id,req_time))
		print("OTP request took ", req_end_time - req_start_time,"seconds.")
		trips_otp_response[id] = trip_plan
		counter+=1

		req_dur_df = pd.DataFrame().from_records(req_duration,columns=['id','duration'])
	#print (req_dur_df.duration.describe())  

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
					start_time = int(leg['startTime'])/1000
					end_time = int(leg['endTime'])/1000
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
							route = lambda x : (x['route']),
							from_stop_id = lambda x : pd.to_numeric(x['from_stop_id'],errors='coerce'),
							to_stop_id = lambda x : pd.to_numeric(x['to_stop_id'],errors='coerce')) \
					.assign(otp_start_time = lambda x : pd.to_datetime(x['otp_start_time'], unit='s'),
							otp_end_time = lambda x : pd.to_datetime(x['otp_end_time'], unit='s')) \
					.sort_values(by=['date','user_trip_id','itinerary_id','otp_start_time'])
					
#Main
#if __name__ == "__main__":
	#if len(sys.argv) < MIN_NUM_ARGS:
	   # print "Error: Wrong Usage!"
		#printUsage()
		#sys.exit(1)

#user_trips_file = sys.argv[1]
#output_folder_path = sys.argv[2]
#otp_server_url = sys.argv[3]

	
user_trips_folder = os.getcwd() + "/data/input/bus_trips/january/"
output_folder_path = os.getcwd() + "/data/output/" 
otp_server_url = "http://localhost:5601/otp/"
#Teste para verificar a montagem de itinerarios para todos onibus da cidade
#user_trips_file = os.getcwd() + "/data/input/2019_02_10_bus_trips.csv"
output_folder_path = os.getcwd() + "/data/output/january" 
otp_server_url = "http://localhost:5601/otp/"
#bus_trips = pd.read_csv('/home/hector/TCC/bulma_matching/february/BuLMABusTE_10-02-2019/2019_02_10_bus_trip_perpoint.csv')
coords_trauma = ['-7.24124', '-35.93233']
coords_partage = ['-7.23629', '-35.87106']
coords_upa = ['-7.19992', '-35.87708']
coords_uepb = ['-7.20878', '-35.91624']
coords_detran = ['-7.25186', '-35.93079']
coords_catolezf = ['-7.27533', '-35.91504']
coords_pcabandeira = ['-7.21989', '-35.88455']
coords_campos_sales = ['-7.22530', '-35.87253']
coords_pqcrianca = ['7.22667', '-35.87705']
coords_campestre = ['-7.24817', '-35.87298']
coords_mirante = ['-7.23518', '-35.86544']
coords_raulc = ['-7.25184', '-35.90702)']

num_empty_files = 0
list_empty_files = []


execution_time = time.time()

for file in os.listdir(user_trips_folder):
	user_trips_file = os.getcwd() + "/data/input/bus_trips/january/" + file
	print ("Processing file", user_trips_file)
	file_name = user_trips_file.split('/')[-1].replace('.csv','')
	file_date = pd.to_datetime(file_name.split('_bus_trips')[0],format='%Y_%m_%d')
	if (file_date.dayofweek == 6):
		print ("File date is sunday. File will not be processed.")
	else:
		try:

			user_trips = pd.read_csv(user_trips_file, low_memory=False)
			if(len(user_trips) == 0):
				num_empty_files += 1
				list_empty_files.append(file_name)

			user_trips = user_trips.loc[(user_trips['stopPointId'] == 491551)]
			#gps_trips = gps_trips.loc[(gps_trips['gps_datetime'] != '-')] 
			# Filtering just trips starting from Hector's home (bus stop)
			user_trips = user_trips.loc[(user_trips['gps_datetime'] != '-')]
			user_trips['gps_datetime'] = pd.to_datetime(user_trips['gps_datetime'], format='%d-%m-%Y %H:%M:%S')
			#gps_trips['gps_datetime'] = pd.to_datetime(gps_trips['gps_datetime'], format='%d-%m-%Y %H:%M:%S')

			#with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
				#future = executor.submit(get_otp_suggested_trips, user_trips,otp_server_url,bus_trips)
			otp_suggestions_trauma = get_otp_suggested_trips(user_trips,otp_server_url,coords_trauma)
			otp_suggestions_partage =(get_otp_suggested_trips(user_trips,otp_server_url,coords_partage))
			otp_suggestions_upa =(get_otp_suggested_trips(user_trips,otp_server_url,coords_upa))
			otp_suggestions_uepb =(get_otp_suggested_trips(user_trips,otp_server_url,coords_uepb))
			otp_suggestions_detran =(get_otp_suggested_trips(user_trips,otp_server_url,coords_detran))
			otp_suggestions_catolezf =(get_otp_suggested_trips(user_trips,otp_server_url,coords_catolezf))
			otp_suggestions_campestre =(get_otp_suggested_trips(user_trips,otp_server_url,coords_campestre))
			otp_suggestions_pcabandeira =(get_otp_suggested_trips(user_trips,otp_server_url,coords_pcabandeira))
			otp_suggestions_pqcrianca = (get_otp_suggested_trips(user_trips,otp_server_url,coords_pqcrianca))
			otp_suggestions_campos_sales = (get_otp_suggested_trips(user_trips,otp_server_url,coords_campos_sales))
			otp_suggestions_mirante = (get_otp_suggested_trips(user_trips,otp_server_url,coords_mirante))
			otp_suggestions_raulc = (get_otp_suggested_trips(user_trips,otp_server_url,coords_raulc))

				#otp_suggestions = future.result()
			otp_legs_df_trauma = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_trauma))
			otp_legs_df_partage = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_partage))
			otp_legs_df_upa = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_upa))
			otp_legs_df_uepb = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_uepb))
			otp_legs_df_detran = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_detran))
			otp_legs_df_catolezf = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_catolezf))
			otp_legs_df_campestre = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_campestre))
			otp_legs_df_pcabandeira = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_pcabandeira))
			otp_legs_df_pqcrianca = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_pqcrianca))
			otp_legs_df_campos_sales = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_campos_sales))
			otp_legs_df_mirante = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_mirante))
			otp_legs_df_raulc = prepare_otp_legs_df(extract_otp_trips_legs(otp_suggestions_raulc))
			result_df = otp_legs_df_trauma.append(otp_legs_df_partage) \
						.append(otp_legs_df_upa).append(otp_legs_df_uepb).append(otp_legs_df_detran) \
						.append(otp_legs_df_catolezf).append(otp_legs_df_campestre).append(otp_legs_df_pcabandeira) \
						.append(otp_legs_df_pqcrianca).append(otp_legs_df_campos_sales).append(otp_legs_df_mirante) \
						.append(otp_legs_df_raulc)

			result_df.drop_duplicates(subset=['date','user_trip_id','leg_id','otp_end_time','mode', 'route','otp_duration_mins', 'from_stop_id', 'to_stop_id'], inplace=True)


			result_df.to_csv(output_folder_path + '/' + file_name + '_otp_itineraries.csv',index=False)
			print("--- %s seconds ---" % (time.time() - execution_time))
			print ("Number of empty_files " + (str(num_empty_files)))
			print (list_empty_files)
			#otp_suggestions = get_otp_suggested_trips(user_trips,otp_server_url)
			
		except Exception as e:
			traceback.print_exc()
			print (e)
			print ("Error in processing file " + file_name)
			print("--- %s seconds ---" % (time.time() - execution_time))


