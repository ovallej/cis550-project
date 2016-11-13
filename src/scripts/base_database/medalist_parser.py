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

	file_csv = csv.DictReader(open(file))
	athlete_id = 1
	medal_id = 1
	event_id = 1
	for row in file_csv :
		if(row[noc] not in country_codes):
		 continue
		curr_gender = "Male" if (row[gender] == "Men") else "Female"

		#create athlete
		if row[athlete] not in athletes:
	
			athletes.append(row[athlete])
			name = row[athlete];
			split = name.split(', ')
			if(len(split) != 2):
				continue
			fname = split[1].upper()
			lname = split[0].upper()
			#curr_gender = "Male" if (row[gender] == "Men") else "Female"
			country_name = country_codes[row[noc]]
			athlete_dict[athlete_id] = {"First Name" : fname, "Last Name" : lname, "Gender" : curr_gender,
							   "_id" : athlete_id, "Country" : country_name }
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


	print("EVENTS")
	#PRINTS ALL EVENT INSERTIONS
	"""
	for key in event_dict:
		#EVENT_ID, SPORT,	DISCIPLINE,	 EVENT,	EVENT_GENDER
		print insert_events % (event_dict[key]["_id"],
								"'" + event_dict[key]["Sport"]+ "'",
								"'" + event_dict[key]["Discipline"]+ "'",
								"'" + event_dict[key]["Event"]+ "'",
								"'" + event_dict[key]["event_gender"].lower() + "'")
	
	"""
	print("ATHLETES")
	#PRINTS ALL ATHLETE INSERTIONS
	"""
	for key in athlete_dict:
		#ATHLETE_ID	,LAST_NAME, FIRST_NAME,COUNTRY_NAME	,HOMETOWN_ID.GENDER 
		print insert_athletes % (athlete_dict[key]["_id"],
								"'" + athlete_dict[key]["Last Name"]+ "'",
								"'" + athlete_dict[key]["First Name"]+ "'",
								"'" + athlete_dict[key]["Country"]+ "'",
								0,
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
