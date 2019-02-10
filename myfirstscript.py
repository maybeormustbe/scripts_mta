
import re
import json
import itertools
import time
import requests

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

# function to build list of values for place

def get_place_data(url, name):
	r = requests.get(url)
	f = re.search('var data = (.*)', r.text, re.MULTILINE)
	value = json.loads(f.group(1)[:-1])
	values = [merge_two_dicts(a, {'place':name}) for sublist in value for a in sublist['values'] ];
	return values

def groupBy(thelist, thelambda):
	retval = {}
	for k, g in itertools.groupby(thelist, thelambda):
		if k in retval : 
			retval[k].append(list(g))
		else : 
			retval[k] = list(g)
	return retval

# TODO 
# sort days 
# present values
# limit to 5 days

def make_alerts():

	# data = {'title':'mon titre', 'array':[{'name':'nom1', 'content':'contenu 1'}, {'name':'nom2', 'content':'contenu 2'}]}
	places = [
		('https://www.surf-report.com/meteo-surf/saint-gilles-croix-vie-s1082.html', 'Saint Gilles'),
	    # ('https://www.surf-report.com/meteo-surf/la-baule-escoublac-s1033.html', 'la baule'),
    	('https://www.surf-report.com/meteo-surf/la-govelle-s1036.html', 'la govelle'),
    	('https://www.surf-report.com/meteo-surf/vert-bois-grand-village-plage-s1088.html','vert bois a Oleron')]
	value = [get_place_data(*a) for a in places]
	value = [a for sublist in value for a in sublist]
	value = [ merge_two_dicts(a, {'hour' : time.strftime('%H', time.strptime(a['dateHour'], '%Y-%m-%d %H:%M:%S')),'date' : time.strftime('%Y%m%d', time.strptime(a['dateHour'], '%Y-%m-%d %H:%M:%S'))}) for a in value]
	value = [merge_two_dicts(a, {'font':'bold' if (int(a['wind'])<20 and float(a['houlePrimaire']>0.8) and float(a['houlePrimaire'])<2.5) else 'normal'}) for a in value]
	value = sorted(value, key=lambda a : a['date'])
	value = groupBy(value, lambda x : x['date']).items()
	value = [(a[0], groupBy(a[1], lambda b : b['place']).items()) for a in value]
	value = [(a[0], [(b[0], sorted(b[1], key=lambda c : c['hour'])) for b in a[1]]) for a in value]
	value = sorted(value, key = lambda a : a[0])
	value = [(time.strftime('%A<br>%d %B', time.strptime(a[0], '%Y%m%d')), a[1]) for a in value]
	return value
	# value = sorted([item for sublist in value for item in sublist], key=lambda x : x['dateKey'])
    # i do it to test push






