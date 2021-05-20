import pymongo


class Database(object):

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://sebastian:test1234@cluster0.0kjei.mongodb.net/blackboard?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
        self.db = self.client["blackboard"]
        self.collection = self.db["blackboard1"]

    def create_blackboard(self, name, validity, time):
    #Erstellt auf dem Server eine neues leeres Blackboard
        try:
            if self.collection.count_documents({"name": name}) > 0:
                print("Blackboard existiert bereits")
                return 409
            else:
                self.collection.insert_one({"name": name, "validity": validity, "time": time})
                print("Blackboard wurde angelegt")
                return 200
        except:
            print("Es ist ein Fehler aufgetreten")
            return 500


    def display_blackboard(self, name, text, validity, time):
    #Aktualisiert den Inhalt eines Blackboards. Im gleichen Zuge wird die Aktualitätsinformation (Zeitstempel) aktualisiert
        try:
            if self.collection.count_documents({"name": name}) > 0:
                self.collection.update_one({"name": name}, {"$set":{"text": text, "validity": validity, "time": time}})
                print("Blackboard wurde erfolgreich aktualisiert")
                return 200
            else:
                print("Blackboard existiert nicht")
                return 404
        except:
            print("Blackboard konnte nicht aktualisiert werden")
            return 500


    def clear_blackboard(self, name, time):
    #Löscht den Inhalt eines Blackboards. Blackboard ist nicht mehr gültig
        try:
            if self.collection.count_documents({"name": name}) > 0:
                self.collection.update_one({"name": name}, {"$set":{"text": "", "validity": "false", "time": time}})
                print("Blackboard wurde erfolgreich aktualisiert")
                return 200
            else:
                print("Blackboard existiert nicht")
                return 404          
        except:
            print("Es ist ein Fehler aufgetreten")
            return 500


    def read_blackboard(self, name):
    #Ließt den Inhalt eines Blackboards aus. Zusätlich wird die Gültigkeit der Daten signalisiert. Wenn die Nachricht veraltet ist wird diese Information zurück gegeben
        try:
            if self.collection.count_documents({"name": name}) > 0:
                results = self.collection.find({"name": name})
                for result in results:
                    if result["text"] == "":
                        print("Das Blackboard ist leer")
                    else:
                        print(result)
                print("Blackboard erfolgreich gelesen")
                return 200
            else:
                print("Blackboard existiert nicht")
                return 404
        except:
            print("Es ist ein Fehler aufgetreten")
            return 500


    def get_blackboard_status(self, name):
    #Gibt den aktuellen Status eines Blackboards zurück
        try:
            if self.collection.count_documents({"name": name}) > 0:
                results = self.collection.find({"name": name})
                for result in results:
                    if result["text"] == "":
                        print("Das Blackboard ist leer")
                    else: 
                        print("Das Blackboard ist gefüllt")
                    if result["validity"] == "true":
                        print("Das Blackboard ist gültig")
                    else:
                        print("Das Blackboard ist ungültig")
                    print("Letzte Aktualisierung: ", result["time"])
                print("Status des Blackboards erfolgreich gelesen")
                return 200
            else:
                print("Blackboard existiert nicht")
                return 404
        except:
            print("Es ist ein Fehler aufgetreten")
            return 500


    def list_blackboards(self):
    #Listet alle vorhandenen Blackboards auf
        try:
            results = self.collection.find({})

            for result in results:
                print(result["name"])
            print("Blackboard Liste erfolgreich zurückgegeben")
            return 200
        except:
            print("Es ist ein Fehler aufgetreten")
            return 500


    def delete_blackboard(self, name):
    #Löscht ein Blackboard
        try:
            if self.collection.count_documents({"name": name}) > 0:
                self.collection.delete_one({"name": name})
                print("Blackboard erfolgreich gelöscht")
                return 200
            else:
                print("Blackboard existiert nicht")
                return 404
        except:
            print("Es ist ein Fehler aufgetreten")
            return 500


    def delete_all_blackboards(self):
    #Löscht alle Blackboards
        self.collection.delete_many({})
        print("Es wurden alle Blackboards gelöscht")
        return 200

    

    

    

    



    #def add_multiple_data(self):
    #fügt mehrere Datensätze hinzu
    #self.collection.insert_many([self.post1, self.post2])

    #updatet einen Datensatz, dabei wird "score" nicht ersetzt, sondern 5 wird addiert (keine Strings)
    #collection.update_one({"_id": 1}, {"$inc":{"score": 5}})