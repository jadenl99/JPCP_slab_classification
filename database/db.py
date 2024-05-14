from pymongo import MongoClient, UpdateOne

class SlabInventory():
    def __init__(self):
        CONNECTION_STRING = 'mongodb://localhost:27017'
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client['jpcp_deterioration']
        self.registration_collection = self.db['registration']
        self.slab_collection = self.db['slabs']
        self.requests = []
        self.segment_id = None
        self.seg_str = None


    def all_registration_metadata(self):
        """Gets all the slab registaration metadata, such as interstate, 
        direction, mileposts, and years registered.


        Returns:
            pymongo.cursor.Cursor: A cursor object that can be used to iterate
            over each registration done
        """
        return self.registration_collection.find(
            {}, {"_id": 1, "segment_id": 1, "years" : 1, "base_year": 1}
            )


    def set_segment(self, seg):
        """Sets the segment_id to the given segment id and updates all the 
        necessary fields

        Args:
            seg (int): segment id to set the segment_id to
        """
        self.segment_id = seg
        self.seg_str = self.registration_collection.find_one(
            {"_id": self.segment_id}
        )['segment_id']

    
    def fetch_reg_data(self):
        """Fetches the registration data for the current segment_id.

        Returns:
            dict: registration data for the current segment_id
        """
        reg_data = self.registration_collection.find_one(
            {"_id": self.segment_id},
            {"_id": 0, "registration_data": 1}
            )
        
        return reg_data['registration_data']


    def execute_requests(self):
        """Executes all the requests in the requests list and clears all the
        requests after.
        """
        self.slab_collection.bulk_write(self.requests)
        self.requests = []  
    

    def add_slab_update_request(self, year, slab_index, update_data):
        """Adds an update request to the requests list to update a certain 
        slab

        Args:
            year (int): year of the slab to update
            slab_index (int): slab index of the slab to update
            update_data (dict): data to update the slab with
        """
        seg_yr_id = f"{self.seg_str}_{year}"
        self.requests.append(
            UpdateOne(
                {"slab_index": slab_index, "seg_year_id": seg_yr_id},
                {"$set": update_data}
                )
            )
