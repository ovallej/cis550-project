import sys
import csv
import optparse

check = "does_the_article_describe_gun_violence_required"
i = "url"
true = 'yes_the_article_is_about_gun_violence'
false = 'no_the_article_is_not_about_gun_violence'
worker = '_worker_id'
test = '_golden'
missed = '_missed'

def print_majority_labels(file) : 
	'''
	prints labels based on majority from full set
	'''
	dt = {}
	#x = 0
	for row in csv.DictReader(open(file)) :
		#print x
		if row[i] not in dt:
			dt[row[i]] = 0
		if row[check] == true:
			dt[row[i]] += 1 
		#x+=1

	for url in dt:
		val = true if dt[url] >= 2 else false
		print url, '\t', val


def print_labels(file) : 
	'''
	prints labels from aggreated set
	'''
	li = set()
	for row in csv.DictReader(open(file)) : 
		if row['url'] not in li:
			print row['url'], '\t', row['does_the_article_describe_gun_violence_required']
		li.add(row['url'])
		
def print_majority_qualities(file) : 
	'''
	prints qualities based on majority data
	'''
	dt = {}
	#x = 0
	for row in csv.DictReader(open(file)) :
		if row[i] not in dt:
			dt[row[i]] = 0
		if row[check] == true:
			dt[row[i]] += 1 
	labels = {}
	for url in dt:
		labels[url] = true if dt[url] >= 2 else false
    
	qualities = {}
	res = {}
	# makes dictionary that tells you what each user responded to each article
	for row in csv.DictReader(open(file)) : 
		if row[worker] not in res:
			res[row[worker]] = {}
		res[row[worker]][row[i]] = row[check]

	#calculates quality from dictionary we just created
	for person in res:
		count = 0
		responses = len(res[person])
		for resp in res[person]:
			if res[person][resp] == labels[resp]:
				count += 1;
		qualities[person] = count/float(responses)
		print person, '\t', qualities[person] 

	#print qualities

def print_weighted_qualities(file) : 
	'''
	prints weighted qualities for each user
	'''
	dt = {}
	#x = 0
	correct = {}
	total = {}
	for row in csv.DictReader(open(file)) :
		if row[worker] not in total:
			correct[row[worker]] = 0
			total[row[worker]] = 0
		#print row[test]
		if row[test] == 'true':
			total[row[worker]] += 1
			if row[missed] != 'true':
				correct[row[worker]] += 1
	#print correct
	#print total
	
	for user in total:
		quality = correct[user]/float(total[user])
		print user, '\t', quality
	
def print_weighted_labels(file) : 
	'''
	prints weighted labels from full set
	'''
	dt = {}
	#x = 0
	correct = {}
	total = {}
	for row in csv.DictReader(open(file)) :
		if row[worker] not in total:
			correct[row[worker]] = 0
			total[row[worker]] = 0
		#print row[test]
		if row[test] == 'true':
			total[row[worker]] += 1
			if row[missed] != 'true':
				correct[row[worker]] += 1
	qualities = {}
	for user in total:
		qualities[user] = correct[user]/float(total[user])
	votes = {}
	for row in csv.DictReader(open(file)) :
		if row[i] not in votes:
			votes[row[i]] = [0,0]
		if row[check] == true:
			votes[row[i]][0] += qualities[row[worker]]
		else:
			votes[row[i]][1] += qualities[row[worker]]
	for page in votes:
		if votes[page][0] >= votes[page][1]:
			print page, '\t', true
		else:
			print page, '\t', false


def print_qualities(file) : 
	'''
	using this list to bypass the workers not included in fullset vs contributor set issue
	'''
	li = ["35039517", "36066082", "29429601", "16854635", "20161225", "15607357", "21425499",
	"27165514", "36233712", "32932483", "13581319", "31792500"]
	for row in csv.DictReader(open(file)) : 
		if float(row['judgments_count']) > 0 and row['worker_id'] in li: 
			print '%s\t%s'%(row['worker_id'], row['trust_overall'])

if __name__ == '__main__' : 

	optparser = optparse.OptionParser()
	optparser.add_option("-d", dest="data_file", help="Crowdflower csv file.")
	optparser.add_option("-m", dest="mode", help="Worker quality ('worker') or data quality ('data')")
	
	(opts, _) = optparser.parse_args()

	#if opts.mode == 'worker' : print_qualities(opts.data_file)
	if opts.mode == 'worker' : print_majority_qualities(opts.data_file)
	#if opts.mode == 'worker' : print_weighted_qualities(opts.data_file)
	elif opts.mode == 'data' : print_majority_labels(opts.data_file)
	#elif opts.mode == 'data' : print_labels(opts.data_file)
	#elif opts.mode == 'data' : print_weighted_labels(opts.data_file)
