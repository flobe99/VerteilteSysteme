#!/usr/bin/env python3
import unittest
import server
from urllib.parse import urlencode
import database
import mongomock

app = server.app.test_client()
def call(method, path, data):
	return app.open( path, method=method, query_string=urlencode( data ))

@mongomock.patch(servers=(('server.example.com', 27017),))
class MockDatabase( database.Database ):

	def __init__(self):
		self.client = mongomock.MongoClient()
		self.db = self.client["blackboard"]
		self.collection = self.db["blackboard1"]

class TestBlackboardCreate(unittest.TestCase):
	def setUp(self):
		server.db = MockDatabase()
		server.db.collection.insert_many([
			{"name": "exists"}
		])

	def test_create_blackboard_success(self):
		r = call( "GET", "/blackboard/create", {
			"name": "test",
			"validityTime": 5
		})
		self.assertEqual( r.status[:3], "200" )
		
	def test_create_blackboard_exists(self):
		r = call( "GET", "/blackboard/create", {
			"name": "exists",
			"validityTime": 5
		})
		self.assertEqual( r.status[:3], "409" )

	def test_create_blackboard_invalid_param(self):
		r = call( "GET", "/blackboard/create", {
			"name": "exists",
			"validityTime": "abc"
		})
		self.assertEqual( r.status[:3], "400" )
	
class TestBlackboardDisplay(unittest.TestCase):
	def setUp(self):
		server.db = MockDatabase()
		server.db.collection.insert_many([
			{"name": "test1", "content": None, "validity": False, "validityTime": "", "timestamp": ""},
			{"name": "test2", "content": "old", "validity": False, "validityTime": "", "timestamp": ""}
		])

	def test_display_blackboard_sucess(self):
		r = call( "GET", "/blackboard/display", {
			"name": "test1",
			"data": "test"
		})
		self.assertEqual( r.status[:3], "200" )

		r = call( "GET", "/blackboard/display", {
			"name": "test2",
			"data": "test"
		})
		self.assertEqual( r.status[:3], "200" )

	def test_display_blackboard_not_found(self):
		r = call( "GET", "/blackboard/display", {
			"name": "not_exists",
			"data": "test"
		})
		self.assertEqual( r.status[:3], "409" )



if __name__ == "__main__":
	unittest.main()