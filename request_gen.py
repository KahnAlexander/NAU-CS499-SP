import json
import sys
import requests
import time

if __name__ == "__main__":

	api_key = ""
	if len(sys.argv) != 2:
		print("No.")
		exit(1)
	else:
		api_key = sys.argv[1]

	# Google Distance Matrix base URL to which all other parameters are attached
	base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

	# Google Distance Matrix domain-specific terms: origins and destinations
	origins = []
	destinations = []

        # grocery = high quality food
        # sitdown = medium quality
        # fast food = low quality
        # city included to append to each
	schoolDict = {
		'communityCollege': {
			'Coconino Community College': 'Flagstaff, AZ',
			'Pima Community College': 'Tucson, AZ',
			'Mesa Community College': 'Mesa, AZ',
			'Glendale Community College': 'Glendale, AZ',
			'Paradise Valley Community College': 'Phoenix, AZ',
			'Rio Salado College': 'Tempe, AZ',
			'South Mountain Community College': 'Phoenix, AZ' },
          	'stateUniversity': {
                        'Northern Arizona University': 'Flagstaff, AZ',
                        'Arizona State University': 'Tempe, AZ',
                        'University of Arizona': 'Tucson, AZ',
                        'University of Texas at Austin': 'Austin, TX',
                        'Texas Tech University': 'Lubbock, TX',
                        'Texas A&M University': 'College Station, TX',
                        'Univeristy of Houston': 'Houston, TX',
                        'New York University': 'New York, NY',
                        'University of California, Berkeley': 'Berkeley, CA',
                        'Purdue University': 'West Lafayette, IN' },
          	'privateUniversity': {
                        'Grand Canyon University': 'Phoenix, AZ',
                        'Embry Riddle Aeronautical University': 'Prescott, AZ',
                        'Baylor University': 'Waco, TX',
                        'Southern Methodist University': 'Dallas, TX',
                        'Texas Christian University': 'Fort Worth, TX',
                        'Massachusetts Institute of Technology': 'Cambridge, MA',
                        'University of Notre Dame': 'Notre Dame, IN',
                        'California Institute of Technology': 'Pasadena, CA' },
          	'ivyLeague': {
                        'Dartmouth College': 'Hanover, NH',
                        'Cornell University': 'Ithaca, NY',
                        'Columbia University': 'New York City, NY',
                        'Princeton University': 'Princeton, NJ',
                        'University of Pennsylvania': 'Philadelphia, PA',
                        'Harvard University': 'Cambridge, MA',
                        'Brown University': 'Providence, RI',
                        'Yale University': 'New Haven, CT' } }
	foodDict = {
               'grocery': ['Bashas\'', 'Safeway', 'Albertson\'s', 'Von\'s', 'Sprouts', 'Fry\'s', 'Costco', 'Sam\'s Club', 'Whole Foods', 'Rainbow', 'Cub Foods',
			   'Kowalski\'s Markets', 'Lunds & Byerlys', 'H-E-B Grocery', 'Kroger', 'Target', 'Walmart', ],
               'fastfood': ['Wendy\'s', 'McDonald\'s', 'Burger King', 'Panda Express', 'Five Guys', 'Domino\'s', 'Pizza Hut', 'Taco Bell', 'Raising Cane\'s Chicken Fingers',
          	     'Subway', 'Quiznos', 'Arby\'s', 'Little Caesars', 'Chick-fil-A', 'Jack In The Box', 'Carl\'s Jr.', 'Del Taco', 'Sonic Drive-In',
                     'Freddy\'s Frozen Custard & Steakburgers', 'Culver\'s', 'Whataburger', 'Dairy Queen', 'In-N-Out Burger', 'The Habit Burger Grill', 'KFC', 'Wienerschnitzel',
					 'Smashburger', 'Popeyes Louisiana Kitchen', 'Jimmy John\'s', 'Jersey Mike\'s', 'White Castle', 'Checkers', 'Church\'s Chicken', 'Cinnabon',
					 'Dunkin\' Donuts', 'Hardee\'s', 'Krispy Kreme', 'Long John Silver\'s', 'Wingstop', 'Tim Hortons', 'Chipotle', 'Starbucks', 'Steakhouse N\' Shake', 'Cafe Rio'
					 'Bojangles', 'Fatburger', 'Papa John\'s', 'Portillo\'s', 'El Pollo Loco', 'Johnny Rockets', 'Schlotzsky\'s', 'Umami Burger', 'Shake Shack'],
               'sitdown': ['Chili\'s', 'Outback Steakhouse', 'Olive Garden', 'Panera Bread', 'Buffalo Wild Wings', 'A&W', 'IHOP', 'Denny\'s', 'Texas Roadhouse', 'Coco\'s',
			   		 'Cracker Barrel Old Country Store', 'Pita Jungle', 'Sizzler', 'Red Lobster', 'Bubba Gump Shrimp Co.', 'NORMS Restaurants', 'The Cheesecake Factory',
					 'Claim Jumper Restaurants', 'Elephant Bar Restaurants', 'TGI Fridays', 'BJ\'s Restaurant & Brewhouse', 'Eureka!', 'Hooters', 'Marie Callender\'s',
					 'Applebee\'s', 'Islands', 'Carrows', 'El Torito'] }

	for schoolCat in schoolDict.keys():
		for school in schoolDict[schoolCat].keys():
			for foodCat in foodDict:

				origins = [school]
				destinations = []

				tempDests = foodDict[foodCat]
				for index in range( len( tempDests ) ):
					destinations.append(tempDests[index] + " near " + school)

				# Prepare the request details for the assembly into a request URL
				payload = {
					'origins' : '|'.join(origins),
					'destinations' : '|'.join(destinations),
					'mode' : 'driving',
					'api_key' : api_key,
					'units' : 'imperial'
				}

				# Assemble the URL and query the web service
				r = requests.get(base_url, params = payload)

				# Check the HTTP status code returned by the server. Only process the response,
				# if the status code is 200 (OK in HTTP terms).
				if r.status_code != 200:
					print('HTTP status code {} received, program terminated.'.format(r.status_code))
				else:
					try:
						# Try/catch block should capture the problems when loading JSON data,
						# such as when JSON is broken. It won't, however, help much if JSON format
						# for this service has changed -- in that case, the dictionaries json.loads() produces
						# may not have some of the fields queried later. In a production system, some sort
						# of verification of JSON file structure is required before processing it. In XML
						# this role is performed by XML Schema.
						x = json.loads(r.text)

						# Now you can do as you please with the data structure stored in x.
						# Here, we print it as a Cartesian product.
						for isrc, src in enumerate(x['origin_addresses']):
							index = 0
							for idst, dst in enumerate(x['destination_addresses']):
								print( destinations[index] + ": ", end="" )
								index += 1
								row = x['rows'][isrc]
								cell = row['elements'][idst]
								if cell['status'] == 'OK':
									print('{} to {}: {}, {}.'.format(src, dst, cell['distance']['text'], cell['duration']['text']))
								else:
									print('{} to {}: status = {}'.format(src, dst, cell['status']))

						# Of course, we could have also saved the results in a file,
						with open('data' + school + foodCat + '.json', 'w') as f:
							f.write(r.text)

						# TODO Or in a database,

						# Or whatever.
						# ???
						# Profit!

					except ValueError:
						print('Error while parsing JSON response, program terminated.')
			time.sleep(90)

	# Prepare for debugging, but only if interactive. Now you can pprint(x), for example.
	if sys.flags.interactive:
		from pprint import pprint
