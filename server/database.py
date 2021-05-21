import pymongo

class Database(object):
	def __init__(self):
		self.client = pymongo.MongoClient("mongodb+srv://sebastian:test1234@cluster0.0kjei.mongodb.net/blackboard?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs="CERT_NONE")
		self.db = self.client["blackboard"]
		self.collection = self.db["blackboard1"]

	def create_blackboard(self, name, validity, time):
	#Erstellt auf dem Server eine neues leeres Blackboard
		try:
			if self.collection.count_documents({"name": name}) > 0:
				return (None, 409)
			else:
				self.collection.insert_one({"name": name, "validity": validity, "time": time})
				return (None, 200)
		except:
			return (None, 500)

	def display_blackboard(self, name, text, validity, time):
	#Aktualisiert den Inhalt eines Blackboards. Im gleichen Zuge wird die Aktualitätsinformation (Zeitstempel) aktualisiert
		try:
			if self.collection.count_documents({"name": name}) > 0:
				self.collection.update_one({"name": name}, {"$set":{"text": text, "validity": validity, "time": time}})
				return (None, 200)
			else:
				return (None, 404)
		except:
			return (None, 500)

	def clear_blackboard(self, name, time):
	#Löscht den Inhalt eines Blackboards. Blackboard ist nicht mehr gültig
		try:
			if self.collection.count_documents({"name": name}) > 0:
				self.collection.update_one({"name": name}, {"$set": {"text": "", "validity": "false", "time": time}})
				return (None, 200)
			else:
				return (None, 404)        
		except:
			return (None, 500)

	def read_blackboard(self, name):
	#Ließt den Inhalt eines Blackboards aus. Zusätlich wird die Gültigkeit der Daten signalisiert. Wenn die Nachricht veraltet ist wird diese Information zurück gegeben
		try:
			results = self.collection.find({"name": name},{'_id': False})
			if results is not None:
				return (results[0], 200)
			else:
				return (None, 404)
		except:
			return (None, 500)


	def get_blackboard_status(self, name):
	#Gibt den aktuellen Status eines Blackboards zurück
		try:
			results = self.collection.find({"name": name},{'_id': False})
			if results is not None:
				return (results[0], 200)
			else:
				return (None, 404)
		except:
			return (None, 500)

	def list_blackboards(self):
	#Listet alle vorhandenen Blackboards auf
		try:
			results = list(self.collection.find({},{'_id': False}))
			return (results, 200)
		except:
			return (None, 500)

	def delete_blackboard(self, name):
	#Löscht ein Blackboard
		try:
			if self.collection.count_documents({"name": name}) > 0:
				self.collection.delete_one({"name": name})
				return (None, 200)
			else:
				return (None, 404)
		except:
			return (None, 500)


	def delete_all_blackboards(self):
	#Löscht alle Blackboards
		try:
			self.collection.delete_many({})
			return (None, 200)
		except:
			return (None,500)