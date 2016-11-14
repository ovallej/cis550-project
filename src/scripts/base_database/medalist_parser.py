import sys
import csv
import optparse

city = "City"
year = "Edition"
sport = 'Sport'
discipline = 'Discipline'
athlete = 'Athlete'
gender = 'Gender'
event = 'Event'
event_gender = 'Event_gender'
medal = 'Medal'

country = "Country"
ccode = "Int Olympic Committee code"
noc = "NOC"

insert_events = "INSERT INTO Events VALUES (%d, %s, %s, %s, %s)"
insert_events % (2, "'sport'", "'disc'", "'evname'", "'male'")
#EVENT_ID, SPORT,	DISCIPLINE,	 EVENT,	EVENT_GENDER
insert_athletes = "INSERT INTO Athlete VALUES (%d, %s, %s, %s, %d, %s)"
insert_athletes % (2, "'name'", "'ame'", "'count'", 2, "'male'")
#ATHLETE_ID	,LAST_NAME, FIRST_NAME,COUNTRY_NAME	,HOMETOWN_ID.GENDER 
insert_medals = "INSERT INTO Medal VALUES (%d, %d, %d, %d, %s)"
insert_medals % (1, 2, 3, 4, "'gold'")
insert_hometowns = "INSERT INTO HOMETOWN VALUES (%d, %s, %s)"
#MEDAL_ID, YEAR,EVENT_ID, ATHLETE_ID,MEDAL_COLOR

def parse_medalists(file) :
	cities = []
	years = []
	sports = []
	disciplines = []
	athletes = []
	genders = []
	events = []
	event_genders = []
	medals = []


	dt = {}
	athlete_dict = {}
	medal_dict = {}
	event_dict = {}
	country_csv = csv.DictReader(open("countrycodes.csv"))
	country_codes = {}
	for row in country_csv:
		#print(row)
		country_codes[row[ccode]] = row[country]

	#print(country_codes)
	hometown_dict = {}
	hometown_set = set()
	file_csv = csv.DictReader(open(file))
	su_2016_home = csv.DictReader(open("hometown_2016_clean.csv"))
	su_2016 = csv.DictReader(open("USA_2016_MEDALISTS.csv"))
	athlete_id = 1
	medal_id = 1
	event_id = 1
	for row in su_2016_home:
		city_state = row["HOMETOWN CITY"].upper() + ", " + row["HOMETOWN STATE"].upper()
		hometown_dict[row["FIRST NAME"].upper()+" "+row["LAST NAME"].upper()] = city_state
		hometown_set.add(city_state)
	hometown_unique = list(hometown_set)

	#print hometown_dict
	for row in file_csv :
		if(row[noc] not in country_codes):
		 continue
		curr_gender = "Male" if (row[gender] == "Men") else "Female"
		name = row[athlete];
		split = name.split(', ')
		if(len(split) != 2):
			continue
		fname = split[1].upper()
		lname = split[0].upper()
		fullname = fname + " " + lname
		#create athlete
		if fullname not in athletes:
	
			"""
			name = row[athlete];
			split = name.split(', ')
			if(len(split) != 2):
				continue
			fname = split[1].upper()
			lname = split[0].upper()
			fullname = fname + " " + lname
			
			"""
			#curr_gender = "Male" if (row[gender] == "Men") else "Female"
			athletes.append(fullname)
			country_name = country_codes[row[noc]]
			athlete_dict[athlete_id] = {"First Name" : fname, "Last Name" : lname, "Gender" : curr_gender,
							   "_id" : athlete_id, "Country" : country_name }
			if( fullname in hometown_dict):
				athlete_dict[athlete_id]["hometown_id"] = hometown_unique.index(hometown_dict[fullname])
				#print("WOWOWOOWOWOWOWOWOWOOWO")
			athlete_id+=1

		#create event
		event_obj = [row[sport], row[discipline], curr_gender, row[event]]
		if(str(event_obj) not in event_dict):
			event_dict[str(event_obj)] = {"_id": event_id, "Sport": row[sport], "Discipline": row[discipline], "Event": row[event], "event_gender":curr_gender}
			event_id+=1

		#create medal
		medal_obj = [row[sport], row[discipline], curr_gender, row[event], row[medal], row[year]]
		if(str(medal_obj) not in medal_dict):
			medal_obj = [row[sport], row[discipline], row[medal], row[year],]
			#event id?
			medal_dict[str(medal_obj)] = {"_id": medal_id, "Medal_color":row[medal], "Year":row[year], "Athlete_id":athlete_id, "Event_id":event_dict[str(event_obj)]["_id"]}
			medal_id+=1

	for row in su_2016 :
		name = row["Name"]
		split = name.split(" ")
		if(len(split) != 2):
			continue
		fname = split[0].upper()
		lname = split[1].upper()
		fullname = fname + " " + lname
		counry_name = "United States"
		#create athlete
		if fullname not in athletes:
			curr_gender = "female" if "Women" in row["Event"] else "male"
			athletes.append(fullname)
			athlete_dict[athlete_id] = {"First Name" : fname, "Last Name" : lname, "Gender" : curr_gender,
							   "_id" : athlete_id, "Country" : country_name }
			if( fullname in hometown_dict):
				athlete_dict[athlete_id]["hometown_id"] = hometown_unique.index(hometown_dict[fullname])
				#print("WOWOWOOWOWOWOWOWOWOOWO")
			athlete_id+=1


		#create event
		event_obj = [row[sport], row[event], curr_gender, row[event]]
		if(str(event_obj) not in event_dict):
			event_dict[str(event_obj)] = {"_id": event_id, "Sport": row[sport], "Discipline": row[event], "Event": row[event], "event_gender":curr_gender}
			event_id+=1

		#create medal
		medal_obj = [row[sport], row[event], curr_gender, row[event], row[medal], row["Year"]]
		if(str(medal_obj) not in medal_dict):
			medal_obj = [row[sport], row[event], row[medal], row["Year"],]
			#event id?
			medal_dict[str(medal_obj)] = {"_id": medal_id, "Medal_color":row[medal], "Year":row["Year"], "Athlete_id":athlete_id, "Event_id":event_dict[str(event_obj)]["_id"]}
			medal_id+=1
		#print athlete_dict[athlete_id-1]
		#print medal_dict[str(medal_obj)]
		#print event_dict[str(event_obj)]
		
	

	#2016,Ryan Held,Swimming,4x100m Freestyle Relay Men,Gold,0.002198148,Rio,Brazil,summer,team,
	print("EVENTS")
	#PRINTS ALL EVENT INSERTIONS
	"""
	for key in event_dict:
		#EVENT_ID, SPORT,	DISCIPLINE,	 EVENT,	EVENT_GENDER
		print insert_events % (event_dict[key]["_id"],
								"'" + event_dict[key]["Sport"].upper()+ "'",
								"'" + event_dict[key]["Discipline"].upper()+ "'",
								"'" + event_dict[key]["Event"].upper()+ "'",
								"'" + event_dict[key]["event_gender"].lower() + "'") + ";"
	"""

	print("ATHLETES")
	#PRINTS ALL ATHLETE INSERTIONS
	"""
	for key in athlete_dict:
		#ATHLETE_ID	,LAST_NAME, FIRST_NAME,COUNTRY_NAME	,HOMETOWN_ID.GENDER 
		if "hometown_id" in athlete_dict[key]:
			print athlete_dict[key]["hometown_id"] 
		
		print insert_athletes % (athlete_dict[key]["_id"],
								"'" + athlete_dict[key]["Last Name"]+ "'",
								"'" + athlete_dict[key]["First Name"]+ "'",
								"'" + athlete_dict[key]["Country"]+ "'",
								athlete_dict[key]["hometown_id"] if "hometown_id" in athlete_dict[key] else 0,
								"'" + athlete_dict[key]["Gender"].lower() + "'")
		
	"""
	print("MEDALS")
	#PRINTS ALL MEDAL INSERTIONS
	"""
	for key in medal_dict:
		#MEDAL_ID, YEAR,EVENT_ID, ATHLETE_ID,MEDAL_COLOR
		print insert_medals % (medal_dict[key]["_id"],
								medal_dict[key]["Year"],
								medal_dict[key]["Event_id"],
								medal_dict[key]["Athlete_id"],
								"'" + medal_dict[key]["Medal_color"].lower() + "'")
	"""
	print("HOMETOWNS")
	"""
	for town in hometown_unique:
		split = town.split(", ")
		if(len(split) < 2):
			split.append("")
		print insert_hometowns % (hometown_unique.index(town), "'" + split[0] + "'" , "'" + split[1] + "'")
	"""
	#hometown_unique.sort()
	#print hometown_unique


if __name__ == '__main__' : 

	optparser = optparse.OptionParser()
	optparser.add_option("-d", dest="data_file", help="Crowdflower csv file.")
	#optparser.add_option("-m", dest="mode", help="Worker quality ('worker') or data quality ('data')")
	
	(opts, _) = optparser.parse_args()

	#if opts.mode == 'worker' : print_qualities(opts.data_file)
	#if opts.mode == 'worker' : print_majority_qualities(opts.data_file)
	#if opts.mode == 'worker' : print_weighted_qualities(opts.data_file)
	parse_medalists(opts.data_file)
	#elif opts.mode == 'data' : print_labels(opts.data_file)
	#elif opts.mode == 'data' : print_weighted_labels(opts.data_file)
