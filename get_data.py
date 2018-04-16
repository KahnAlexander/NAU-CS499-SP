import json
import numpy
import csv

def get_data( data_str ):
	if( data_str[len( data_str ) - 2:len( data_str )] == "ft" ):
		return "f" + data_str.split( " " )[0] + ".0"
	else:
		if( "." in data_str ):
			return "m" + data_str.split( " " )[0]
		else:
			return "m" + data_str.split( " " )[0].replace( ",", "" ) + ".0"

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

data_dict = {}

for schoolCat in schoolDict.keys():
	print( "----------------" + schoolCat + "----------------" )
	data_dict[schoolCat] = {}
	for school in schoolDict[schoolCat].keys():
		print( "----" + school + "----" )
		data_dict[schoolCat][school] = {}
		for foodCat in ["fastfood", "grocery", "sitdown"]:
			try:
				print( "--" + foodCat + "--" )
				with open( "data" + school + foodCat + ".json" ) as file:
					data_dict[schoolCat][school][foodCat] = {}
					cat_nums = []
					data = json.load( file )
					for route in data["rows"][0]["elements"]:
						try:
							data_str = get_data( route["distance"]["text"] )
							if( data_str[0] == "f"):
								cat_nums.append( float( data_str[1::] ) / 5280.0 )
							else:
								data_float = float( data_str[1::] )
								if( foodCat == "sitdown" and data_float <= 8.0 ):
									cat_nums.append( data_float )
								elif( ( foodCat == "grocery" or foodCat == "fastfood" ) and data_float <= 5 ):
									cat_nums.append( data_float )
						except:
							continue
					print( cat_nums )
					data_dict[schoolCat][school][foodCat]["distances"] = cat_nums
					print( len( cat_nums ) )
					data_dict[schoolCat][school][foodCat]["num_paths"] = len( cat_nums )
					print( numpy.mean( cat_nums ) )
					data_dict[schoolCat][school][foodCat]["mean"] = numpy.mean( cat_nums )
			except:
				break

print( data_dict )

with open( "data_dump.csv", "w" ) as data_dump:
	file = csv.writer( data_dump )
	for schoolCat in schoolDict.keys():
		print( schoolCat )
		file.writerow( [schoolCat] )
		for school in schoolDict[schoolCat].keys():
			try:
				for foodCat in ["fastfood", "grocery", "sitdown"]:
					for num in data_dict[schoolCat][school][foodCat]["distances"]:
						file.writerow( [foodCat[0]] + [str( num )] )
			except:
				break
