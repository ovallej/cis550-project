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
		"""
		if row[city] not in cities:
			cities.append(row[city])
		if row[year] not in years:
			years.append(row[year])
		if row[sport] not in sports:
			sports.append(row[sport])
		if row[discipline] not in disciplines:
			disciplines.append(row[discipline])
		"""
		#print("HEREHREHERHERHRHHEHEHR")
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

		"""
		if row[gender] not in genders:
			genders.append(row[gender])
		if row[event] not in events:
			events.append(row[event])
		if row[event_gender] not in event_genders:
			event_genders.append(row[event_gender])
		if row[medal] not in medals:
			medals.append(row[medal])
		"""
		#//print("HEREHREHERHERHEREHREHERHERHRHHEHEHRHEREHREHERHERHRHHEHEHRHRHHEHEHR")
		event_obj = [row[sport], row[discipline], curr_gender, row[event]]

		if(str(event_obj) not in event_dict):
			event_dict[str(event_obj)] = {"_id": event_id, "Sport": row[sport], "Discipline": row[discipline], "Event": row[event], "event_gender":curr_gender}
			event_id+=1

		medal_obj = [row[sport], row[discipline], curr_gender, row[event], row[medal], row[year]]

		if(str(medal_obj) not in medal_dict):
			medal_obj = [row[sport], row[discipline], row[medal], row[year],]
			#event id?
			medal_dict[str(medal_obj)] = {"_id": medal_id, "Medal_color":row[medal], "Year":row[year], "Athlete_id":athlete_id, "Event_id":event_dict[str(event_obj)]}
			medal_id+=1

	print("HEREHREHERHERHEREHREHERHERHRHHEHEHRHEREHREHERHERHRHHEHEHRHRHHEHEHR")
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	print("MEDALS")
	print(medal_dict)
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	print("MEDALS")
	print(event_dict)
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	print("ATHLETES")
	print(athlete_dict)

	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")





"""
	print cities
	print len(cities)
	print years
	print len(years)
	print sports
	print len(sports)
	print medals
	print len(medals)
	print events
	print len(events)
	print disciplines
	print len(disciplines)
	print event_genders
	print len(event_genders)
	print athletes
	print len(athletes)
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
