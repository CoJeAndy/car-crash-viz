regions = {
"/00.csv":	"1214",	# Praha
"/01.csv":	"100", # Středočeský
"/02.csv":	"200", # Jihočeský
"/03.csv":	"300", # Plzeňský
"/04.csv":	"400", # Ústecký
"/05.csv":	"500", # Královéhradecký
"/06.csv":	"600", # Jihomoravský
"/07.csv":	"700", # Moravskoslezský			
"/14.csv":	"1400", # Olomoucký	
"/15.csv":	"1500", # Zlínský		
"/16.csv":	"1600", # Vysočina		
"/17.csv":	"1700",	# Pardubický
"/18.csv":	"1800", # Liberecký	
"/19.csv":	"1900", # Karlovarský	
}

road_type_dict = {
0: 'highway',
1: 'first-class road',
2: 'second-class road',
3: 'third-class road',
4: 'monitored intersection',
5: 'other (parking lot, forest road, etc.)'
}

region_names = {
1214: 'Praha',
100: 'Středočeský',
200: 'Jihočeský',
300: 'Plzeňský',
400: 'Ústecký',
500: 'Královéhradecký',
600: 'Jihomoravský',
700: 'Moravskoslezský',
1400: 'Olomoucký',
1500: 'Zlínský',
1600: 'Vysočina',
1700: 'Pardubický',
1800: 'Liberecký',
1900: 'Karlovarský',
}

severity_dict = {
    3: 'death',
    2: 'heavily injured',
    1: 'lightly injured',
    0: 'no injury'
}


crash_type_dict = {
0: 'other type of accident',
1: 'collision with a moving non-rail vehicle',
2: 'collision with a parked, stopped vehicle',
3: 'collision with a solid obstacle',
4: 'collision with a pedestrian',
5: 'collision with wild animals',
6: 'collision with a domestic animal',
7: 'collision with a train',
8: 'collision with a tram',
9: 'car crash'
}

substance_dict = {
0: 'not determined',
1: 'no',
2: 'alcohol in blood up to 0.24%',
3: 'alcohol in blood from 0.24% to 0.5%',
4: 'alcohol in blood from 0.5% to 0.8%',
5: 'alcohol in blood from 0.8% to 1.0%',
6: 'alcohol in blood from 1.0% to 1.5%',
7: 'alcohol in blood 1.5% and more',
8: 'under the influence of drugs',
9: 'under the influence of alcohol and drugs'
}

weather_dict = {
0: 'other obstructions',
1: 'unobstructed',
2: 'fog',
3: 'beginning of rain, light rain, drizzle, etc.',
4: 'rain',
5: 'snowing',
6: 'frost or ice forming',
7: 'gusty wind (side, whirlwind, etc.)'
}


x_labels = {
    'road_type': ['highway', 'first-class road', 'second-class road', 'third-class road', 'monitored intersection', 'other (parking lot, forest road, etc.)'],
    'substance': ['not determined', 'no', 'alcohol in blood up to 0.24%', 'alcohol in blood from 0.24% to 0.5%', 'alcohol in blood from 0.5% to 0.8%', 'alcohol in blood from 0.8% to 1.0%', 'alcohol in blood from 1.0% to 1.5%', 'alcohol in blood 1.5% and more', 'under the influence of drugs', 'under the influence of alcohol and drugs'],
    'weather': ['other obstructions', 'unobstructed', 'fog', 'beginning of rain, light rain, drizzle, etc.', 'rain', 'snowing', 'frost or ice forming', 'gusty wind (side, whirlwind, etc.)'],
    'crash_type': ['other type of accident', 'collision with a moving non-rail vehicle', 'collision with a parked, stopped vehicle', 'collision with a solid obstacle', 'collision with a pedestrian', 'collision with wild animals', 'collision with a domestic animal', 'collision with a train', 'collision with a tram', 'car crash']
}

legend_dictionaries = {
     'road_type': road_type_dict,
    'substance': substance_dict,
    'weather': weather_dict,
    'crash_type': crash_type_dict,
}