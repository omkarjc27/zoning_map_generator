#http://ecn.t0.tiles.virtualearth.net/tiles/a1233030302121212121.jpeg?g=10583
import urllib.request
import itertools
import json
# store the URL in url as 
# parameter for urlopen
#url = "http://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial?output=json&include=ImageryProviders&key=AhPe4ojD-5t0igIhrWqKo00EP35zbC3TqlosYmJpgLJGxJ1pXgav2C8NH8zbGwLq"
  
# store the response of URL
#response = urllib.request.urlopen(url)
  
# storing the JSON response 
# from url in data
#data_json = json.loads(response.read())
  
# print the json response
#scrape_url = data_json['resourceSets'][0]['resources'][0]['imageUrl']
#print(scrape_url)
#http://ecn.t0.tiles.virtualearth.net/tiles/a1233003111.jpeg?g=10602
#print(itertools.product(['0','1','2','3'], repeat=6))

for quadkey in ["".join(p) for p in itertools.product(['0','1','2','3'], repeat=6)]:
	print(quadkey)
	urllib.request.urlretrieve("http://ecn.t0.tiles.virtualearth.net/tiles/a1233003111120{}.jpeg?g=10583".format(quadkey), "images/1233003111120{}.jpg".format(quadkey))
#https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial/72.98577232054774,19.199475300596134?zl=19&o=xml&key=AhPe4ojD-5t0igIhrWqKo00EP35zbC3TqlosYmJpgLJGxJ1pXgav2C8NH8zbGwLq