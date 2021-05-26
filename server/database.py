import pymongo
from datetime import datetime, timedelta

class Database(object):
	def __init__(self):
		self.client = pymongo.MongoClient("mongodb+srv://sebastian:test1234@cluster0.0kjei.mongodb.net/blackboard?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs="CERT_NONE")
		self.db = self.client["blackboard"]
		self.collection = self.db["blackboard1"]

	def validate_blackboard(self, name, content, validityTime, timestamp):
	# Überprüft den Datensatz auf Gültigkeit der Zeit
	# Dabei wird die aktuelle Zeit mit der gespeicherten Zeit + die Gültigkeitsdauer verglichen.
		now = datetime.now()
		time = timestamp + timedelta(seconds = validityTime)
		if validityTime == 0:
			self.collection.update_one({"name": name}, {"$set":{"validity": "true"}})
		if content == "":
			self.collection.update_one({"name": name}, {"$set":{"validity": False}})
		elif now < time:
			self.collection.update_one({"name": name}, {"$set":{"validity": True}})
		elif content == "":
			self.collection.update_one({"name": name}, {"$set":{"validity": "true"}})
		else:
			self.collection.update_one({"name": name}, {"$set":{"validity": False}})

	def create_blackboard(self, name, validityTime):
	# Erstellt auf dem Server eine neues leeres Blackboard
	# Zu Beginn werden die Attribute name, validityTime, und timestamp angelegt
		try:
			if self.collection.count_documents({"name": name}) > 0:
				return (None, 409)
			else:
				now = datetime.now()
				self.collection.insert_one({"name": name, "validityTime": validityTime, "timestamp": now})
				return (None, 200)
		except:
			return (None, 500)

	def display_blackboard(self, name, content):
	# Aktualisiert den Inhalt eines Blackboards. Im gleichen Zuge wird die Aktualitätsinformation (Zeitstempel) aktualisiert
		try:
			if self.collection.count_documents({"name": name}) > 0:
				time = datetime.now()
				self.collection.update_one({"name": name}, {"$set":{"content": content, "timestamp": time}})
				return (None, 200)
			else:
				return (None, 404)
		except:
			return (None, 500)

	def clear_blackboard(self, name):
	# Löscht den Inhalt eines Blackboards. Blackboard ist nicht mehr gültig
		try:
			if self.collection.count_documents({"name": name}) > 0:
				self.collection.update_one({"name": name}, {"$set": {"content": ""}})
				return (None, 200)
			else:
				return (None, 404)        
		except:
			return (None, 500)

	def read_blackboard(self, name):
	# Ließt den Inhalt eines Blackboards aus. Zusätlich wird die Gültigkeit der Daten signalisiert. Wenn die Nachricht veraltet ist wird diese Information zurück gegeben.
	# Die Gültigkeit der Daten wird als eigenes Attribut in der Funktion validate_blackboard übergeben.
		try:
			temp = self.collection.find_one({"name": name},{'_id': False})
			if temp is not None:
				name = temp["name"]
				validityTime = temp["validityTime"]
				timestamp =	temp["timestamp"]
				content = temp["content"]
				self.validate_blackboard(name, content, validityTime, timestamp)
				results = self.collection.find_one({"name": name},{'_id': False})
				return (results, 200)
			else:
				return (None, 404)
		except Exception as e:
			raise( e )
			return (None, 500)


	def get_blackboard_status(self, name):
	# Gibt den aktuellen Status eines Blackboards zurück.
		try:
			temp = self.collection.find_one({"name": name},{'_id': False})
			if temp is not None:	
				name = temp["name"]
				validityTime = temp["validityTime"]
				timestamp =	temp["timestamp"]
				content = temp["content"]
				self.validate_blackboard(name, content, validityTime, timestamp)
				results = self.collection.find({"name": name},{'_id': False})
				return (results[0], 200)
			else:
				return (None, 404)
		except:
			return (None, 500)

	def list_blackboards(self):
	# Listet alle vorhandenen Blackboards auf
		try:
			results = list(self.collection.find({},{'_id': False}))
			return (results, 200)
		except:
			return (None, 500)

	def delete_blackboard(self, name):
	# Löscht ein Blackboard
		try:
			if self.collection.count_documents({"name": name}) > 0:
				self.collection.delete_one({"name": name})
				return (None, 200)
			else:
				return (None, 404)
		except:
			return (None, 500)


	def delete_all_blackboards(self):
	# Löscht alle Blackboards
		try:
			self.collection.delete_many({})
			return (None, 200)
		except:
			return (None,500)
		
	# def validate_blackboard(self, validityTime, timestamp):
	# 	now = datetime.now() # current date and time
	# 	time = timestamp + timedelta(seconds = validityTime)
	# 	if validityTime == 0:
	# 		return True
	# 	elif now < time:
	# 		return True
	# 	else:
	# 		return False

	
