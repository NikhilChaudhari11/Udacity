# Insert Data
from pymongo import MongoClient
client  = MongoClient('mongodb://localhost:27017')
db = client.udacity
for item in data:
	db.project2.insert(item)


# Data Aggregation
import pprint
from pymongo import MongoClient
client  = MongoClient('mongodb://localhost:27017')
db = client.udacity

# number of unique users
pprint.pprint(len(db.project2.distinct("created.user")))
# number of nodes and ways
pprint.pprint(db.project2.find({"type":"way"}).count())
pprint.pprint(db.project2.find({"type":"node"}).count())
# number of book stores
pipeline1 = [
			{"$match": {"amenity": "books"}},
			{"$project":{"_id": "$name", "opening_hours": "$opening_hours"}}]
pprint.pprint(len(db.project2.aggregate(pipeline1)['result']))
# number of soccer fields
pipeline2 = [
			{"$match": {"amenity": "soccer"}},
			{"$project":{"_id": "$name", "surface": "$surface"}}]
pprint.pprint(len(db.project2.aggregate(pipeline2)['result']))
# number of hotels
pipeline3 = [
			{"$match": {"amenity": "hotel"}},
			{"$project":{"_id": "$name", "stars": "$stars", "rooms": "$rooms"}}]
pprint.pprint(len(db.project2.aggregate(pipeline3)['result']))
# top 10 contributed users
pipeline4 = [
            {"$match": {"created.user":{"$exists":1}}},
            {"$group": {"_id":"$created.user","count":{"$sum":1}}},
            {"$sort": {"count":-1}},
            {"$limit" : 10}]
pprint.pprint(db.project2.aggregate(pipeline4)['result'])


# Data Aggregation - Advanced
pprint.pprint(len(db.project2.distinct("amenity")))
# Top 10 appearing amenities
pipeline5 = [
            {"$match": {"amenity":{"$exists":1}}},
            {"$group": {"_id":"$amenity","count":{"$sum":1}}},
            {"$sort": {"count":-1}},
            {"$limit" : 10}]
pprint.pprint(db.project2.aggregate(pipeline5)['result'])
# Top 5 fast food brand
pipeline6 = [
			{"$match":{"amenity":{"$exists":1}, "amenity":"fast_food"}},
			{"$group": {"_id":"$name","count":{"$sum":1}}},
			{"$sort": {"count":-1}},
            {"$limit" : 5}]
pprint.pprint(db.project2.aggregate(pipeline6)['result'])
# Top 5 restaurant cuisine
pipeline7 = [
			{"$match":{"amenity":{"$exists":1}, "amenity":"restaurant"}},
			{"$group": {"_id":"$cuisine","count":{"$sum":1}}},
			{"$sort": {"count":-1}},
            {"$limit" : 10}]
pprint.pprint(db.project2.aggregate(pipeline7)['result'][1:6])
# Biggest religion
pipeline8 = [
			{"$match":{"amenity":{"$exists":1}, "amenity":"place_of_worship"}},
			{"$group": {"_id":"$religion","count":{"$sum":1}}},
			{"$sort": {"count":-1}},
            {"$limit" : 10}]
pprint.pprint(db.project2.aggregate(pipeline8)['result'])
# Top 10 Elevation of grave_yard
pipeline9 = [
			{"$match":{"amenity":{"$exists":1}, "amenity":"grave_yard"}},
			{"$project": {"_id":"$name","ele":"$ele"}},
			{"$sort": {"ele":-1}},
            {"$limit" : 10}]
pprint.pprint(db.project2.aggregate(pipeline9)['result'])

