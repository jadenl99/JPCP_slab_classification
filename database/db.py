from pymongo import MongoClient 

class SlabInventory():
    def __init__(self):
        CONNECTION_STRING = 'mongodb://localhost:27017'
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client['jpcp_deterioration']
        self.registration_collection = self.db['registration']
        self.slab_collection = self.db['slabs']


    def all_registration_metadata(self):
        """Gets all the slab registaration metadata, such as interstate, 
        direction, mileposts, and years registered.


        Returns:
            pymongo.cursor.Cursor: A cursor object that can be used to iterate
            over each registration done
        """
        return self.registration_collection.find(
            {}, {"_id": 0, "segment_id": 1, "years" : 1, "base_year": 1}
            )

        
