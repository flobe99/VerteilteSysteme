#!/usr/bin/env python3
import unittest
import server
import database
import mongomock
import json

from urllib.parse import urlencode
from datetime import *

app = server.app.test_client()
def call(method, path, data):
	return app.open( path, method=method, query_string=urlencode( data ))

# Wrapper for generating datetime.
# Microseconds are not stored in MongoDB. Cut off microseconds for testing
def now():
	d = datetime.now()
	d = d.replace( microsecond=0 )

	return d

class MockDatabase( database.Database ):

	def __init__(self):
		self.client = mongomock.MongoClient()
		self.db = self.client["blackboard"]
		self.collection = self.db["blackboard1"]

class TestBlackboardCreate(unittest.TestCase):
	def setUp(self):
		server.db = MockDatabase()
		server.db.collection.insert_many([
			{ "name": "exists"}
		])

	def test_create_blackboard_success(self):
		r = call( "POST", "/blackboard/create", {
			"name": "test",
			"validityTime": 5
		})
		self.assertEqual( r.status[:3], "200" )

	def test_create_blackboard_exists(self):
		r = call( "POST", "/blackboard/create", {
			"name": "exists",
			"validityTime": 5
		})
		self.assertEqual( r.status[:3], "409" )

	def test_create_blackboard_invalid_param(self):
		r = call( "POST", "/blackboard/create", {
			"name": "test",
			"validityTime": "abc"
		})
		self.assertEqual( r.status[:3], "400" )

		r = call( "POST", "/blackboard/create", {
			"name": "test",
		})
		self.assertEqual( r.status[:3], "400" )

		r = call( "POST", "/blackboard/create", {
			"validityTime": "abc"
		})
		self.assertEqual( r.status[:3], "400" )

		r = call( "POST", "/blackboard/create", {
		})
		self.assertEqual( r.status[:3], "400" )

class TestBlackboardDisplay(unittest.TestCase):
	def setUp(self):
		server.db = MockDatabase()
		server.db.collection.insert_many([
			{"name": "test1", "content": "", "validityTime": 5, "timestamp": now() },
			{"name": "test2", "content": "old", "validityTime": 5, "timestamp": now() }
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

	def test_display_blackboard_invalid_param(self):
		r = call( "GET", "/blackboard/display", {
			"name": "test1",
		})
		self.assertEqual( r.status[:3], "400" )

		r = call( "GET", "/blackboard/display", {
			"data": "test"
		})
		self.assertEqual( r.status[:3], "400" )

		r = call( "GET", "/blackboard/display", {
		})
		self.assertEqual( r.status[:3], "400" )

	def test_display_blackboard_not_found(self):
		r = call( "GET", "/blackboard/display", {
			"name": "not_exists",
			"data": "test"
		})
		self.assertEqual( r.status[:3], "404" )

class TestBlackboardClear(unittest.TestCase):
	def setUp(self):
		server.db = MockDatabase()
		server.db.collection.insert_many([
			{"name": "test1", "content": "", "validityTime": 5, "timestamp": now() },
			{"name": "test2", "content": "old", "validityTime": 5, "timestamp": now() }
		])

	def test_clear_blackboard_success(self):
		r = call( "GET", "/blackboard/clear", {
			"name": "test1",
		})
		self.assertEqual( r.status[:3], "200" )

		r = call( "GET", "/blackboard/clear", {
			"name": "test2",
		})
		self.assertEqual( r.status[:3], "200" )

	def test_clear_blackboard_success(self):
		r = call( "GET", "/blackboard/clear", {
		})
		self.assertEqual( r.status[:3], "400" )

	def test_clear_blackboard_success(self):
		r = call( "GET", "/blackboard/clear", {
			"name": "test3"
		})
		self.assertEqual( r.status[:3], "404" )

class TestBlackboardRead(unittest.TestCase):
	def setUp(self):
		self.data = [
			{"name": "test1", "content": "new", "validityTime": 5, "timestamp": now() },
			{"name": "test2", "content": "old", "validityTime": 5, "timestamp": (now() - timedelta(10)) },
			{"name": "test3", "content": "", "validityTime": 5, "timestamp": now() }
		];

		server.db = MockDatabase()
		server.db.collection.insert_many(self.data)

	def test_read_blackboard_success(self):
		# Valid
		r = call( "GET", "/blackboard/read", {
			"name": "test1"
		})
		self.assertEqual( r.status[:3], "200" )
		result = json.loads( next(r.response).decode("ascii") )
		self.assertEqual( result, {"content": "new", "validity": True} )

		# Invalid
		r = call( "GET", "/blackboard/read", {
			"name": "test2"
		})
		self.assertEqual( r.status[:3], "200" )
		result = json.loads( next(r.response).decode("ascii") )
		self.assertEqual( result, {"content": "old", "validity": False} )

	def test_read_blackboard_invalid_param(self):
		r = call( "GET", "/blackboard/read", {
		})
		self.assertEqual( r.status[:3], "400" )

	def test_read_blackboard_not_found(self):
		r = call( "GET", "/blackboard/read", {
			"name": "test4"
		})
		self.assertEqual( r.status[:3], "404" )

	def test_read_blackboard_empty(self):
		r = call( "GET", "/blackboard/read", {
			"name": "test3"
		})
		self.assertEqual( r.status[:3], "444" )


class TestBlackboardStatus(unittest.TestCase):
	def setUp(self):
		server.db = MockDatabase()
		self.data = [
			{"name": "test1", "content": "old", "validityTime": 5, "timestamp": (now() - timedelta(10)) },
			{"name": "test2", "content": "new", "validityTime": 5, "timestamp": now() },
			{"name": "test3", "content": "", "validityTime": 5, "timestamp": now() }
		]
		server.db.collection.insert_many(self.data)

	def test_status_blackboard_success(self):
		# Valid
		r = call( "GET", "/blackboard/getStatus", {
			"name": "test2"
		})
		self.assertEqual( r.status[:3], "200" )
		result = json.loads( next(r.response).decode("ascii") )
		print( self.data[1]["timestamp"] )
		self.assertEqual( result, {"timestamp": self.data[1]["timestamp"].isoformat(), "validity": True, "empty": False })

		# Invalid
		r = call( "GET", "/blackboard/getStatus", {
			"name": "test1"
		})
		self.assertEqual( r.status[:3], "200" )
		result = json.loads( next(r.response).decode("ascii") )
		self.assertEqual( result, {"timestamp": self.data[0]["timestamp"].isoformat(), "validity": False, "empty": False })

		# Empty
		r = call( "GET", "/blackboard/getStatus", {
			"name": "test3"
		})
		self.assertEqual( r.status[:3], "200" )
		result = json.loads( next(r.response).decode("ascii") )
		self.assertEqual( result, {"timestamp": self.data[2]["timestamp"].isoformat(), "validity": False, "empty": True })

	def test_status_blackboard_invalid_param(self):
		r = call( "GET", "/blackboard/getStatus", {
		})
		self.assertEqual( r.status[:3], "400" )

	def test_status_blackboard_not_found(self):
		r = call( "GET", "/blackboard/getStatus", {
			"name": "test4"
		})
		self.assertEqual( r.status[:3], "404" )

class TestBlackboardList(unittest.TestCase):
	def setUp(self):
		server.db = MockDatabase()
		server.db.collection.insert_many([
			{"name": "test1", "content": "", "validityTime": 5, "timestamp": now()},
			{"name": "test2", "content": "old", "validityTime": 5, "timestamp": now()}
		])

	def test_list_blackboard_success(self):
		r = call( "GET", "/blackboard/list", {
		})
		self.assertEqual( r.status[:3], "200" )

		result = json.loads( next(r.response).decode('ascii') )
		self.assertEqual( sorted( result, key=lambda e: e["name"] ), [{"name": "test1"}, {"name": "test2"}] )

class TestBlackboardDelete(unittest.TestCase):
	def setUp(self):
		server.db = MockDatabase()
		server.db.collection.insert_many([
			{"name": "test1", "content": "", "validityTime": 5, "timestamp": now()},
			{"name": "test2", "content": "old", "validityTime": 5, "timestamp": now()}
		])

	def test_delete_blackboard_success(self):
		r = call( "DELETE", "/blackboard/delete", {
			"name": "test1"
		})
		self.assertEqual( r.status[:3], "200" )

	def test_delete_blackboard_invalid_param(self):
		r = call( "DELETE", "/blackboard/delete", {
		})
		self.assertEqual( r.status[:3], "400" )

	def test_delete_blackboard_not_found(self):
		r = call( "DELETE", "/blackboard/delete", {
			"name": "test3"
		})
		self.assertEqual( r.status[:3], "404" )

class TestBlackboardDeleteAll(unittest.TestCase):
	def setUp(self):
		server.db = MockDatabase()
		server.db.collection.insert_many([
			{"name": "test1", "content": "", "validityTime": 5, "timestamp": now()},
			{"name": "test2", "content": "old", "validityTime": 5, "timestamp": now()}
		])

	def test_deleteall_blackboard_success(self):
		r = call( "DELETE", "/blackboard/deleteAll", {
		})
		self.assertEqual( r.status[:3], "200" )



if __name__ == "__main__":
	unittest.main()