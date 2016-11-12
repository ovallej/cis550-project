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
	file_csv = csv.DictReader(open(file))
	for row in file_csv :
		if row[city] not in cities:
			cities.append(row[city])
		if row[year] not in years:
			years.append(row[year])
		if row[sport] not in sports:
			sports.append(row[sport])
		if row[discipline] not in disciplines:
			disciplines.append(row[discipline])
		if row[athlete] not in athletes:
			athletes.append(row[athlete])
		if row[gender] not in genders:
			genders.append(row[gender])
		if row[event] not in events:
			events.append(row[event])
		if row[event_gender] not in event_genders:
			event_genders.append(row[event_gender])
		if row[medal] not in medals:
			medals.append(row[medal])

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
