import pymongo
from pymongo import ReturnDocument
from bson.dbref import DBRef

from datetime import datetime
from feqor.utils import constants
from feqor.app import mongo


class DB(object):
    """
    Performs all CRUD MongoDB operations
    """
    def __init__(self, logger):
        self.logger = logger

    def fetch(self, collection, query, **kwargs):
        sort_data = []
        if 'sort' in kwargs and kwargs['sort']:
            for key in kwargs['sort'].keys():
                if kwargs['sort'][key] == 1:
                    order = pymongo.ASCENDING
                else:
                    order = pymongo.DESCENDING
                sort_data.append((key, order))

        if not len(sort_data):
            sort_data.append(("_id",pymongo.ASCENDING))

        if 'skip' in kwargs and kwargs['skip']:
            skip = int(kwargs['skip'])
        else:
            skip = 0

        if 'limit' in kwargs and kwargs['limit']:
            _limit = int(kwargs['limit'])
        else:
            _limit = constants.MAX_PAGE_SIZE

        if 'projection' in kwargs and kwargs['projection']:
            projection = kwargs['projection']
        else:
            projection = None

        db_ref_fields = []
        if projection:
            for key in list(projection):
                if collection in constants.DB_REFS and key in constants.DB_REFS[collection]:
                    db_ref_fields.append(key)
        else:
            db_ref_fields.extend(constants.DB_REFS.get(collection, []))

        self.logger.info("interacting with mongodb to fetch data.....",
                         query=str(query), sort=sort_data, projection=projection, skip=skip,limit=_limit,
                         collection=collection)

        cursor = mongo.db[collection].find(query, projection)\
            .sort(sort_data)\
            .skip(skip)\
            .limit(_limit)

        if not len(db_ref_fields):
            return list(cursor)
        else:
            return self.fetch_db_ref_fields_data(cursor, db_ref_fields)

    def create(self, collection, payload, **kwargs):
        """
        replaces or created new document into mongoDB based on _id field.
        :param payload: document data
        :param kwargs:
        :return: complete document
        """
        payload[constants.CREATED_DATE] = datetime.strftime(datetime.now(), constants.MONGO_DOC_CREATE_FORMAT)
        id = mongo.db[collection].save(payload)
        payload['_id']=str(id)
        self.logger.info("document saved into mongodb.", _id=str(id), collection=collection)
        return payload


    def bulk_update(self, collection, data):
        self.logger.info("bulk updating started.")
        bulk = mongo.db[collection].initialize_unordered_bulk_op()
        for doc in data:
            data = self.remove_ref_fields(doc['data'])
            query = doc['query']
            bulk.find(query).update({'$set': data})
        bulk.execute()
        self.logger.info("bulk update completed.")
        return

    def update(self,collection, query, data, **kwargs):
        """
        updates document in mongoDB based on query field.
        :param payload: document data
        :param kwargs:
        :return: complete document
        """
        data = self.remove_ref_fields(data)
        result = mongo.db[collection].find_one_and_update(
            query,
            {"$set":data},
            return_document=ReturnDocument.AFTER
        )
        self.logger.info("updated mongodb document", query=query, collection=collection, **kwargs)
        return result


    def aggregate_query(self, collection,  query):
        """
        returns aggregated query output results
        :param query:
        :return:
        """
        self.logger.info("running aggregation query", query=query, collection=collection)
        self.logger = self.logger.bind(agg_query=query, collection=collection)
        return mongo.db[collection].aggregate(query, allowDiskUse=True)

    def get_distinct_values(self, collection, field_name):
        """
        fetches distinct values for given col name
        :param collection:
        :param field_name: name of field(coloumn)
        :return: array of values
        """
        self.logger.info("fetching distinct values", collection=collection, field_name=field_name)
        return mongo.db[collection].distinct(field_name)

    def get_distinct_values_by_query(self, collection, **kwargs):
        """
        fetches distinct values for given col name
        :param collection:
        :param field_name: name of field(coloumn)
        :return: array of values
        """

        self.logger.info("fetching distinct values by query", collection=collection, **kwargs)
        return mongo.db[collection].find(kwargs['query'], kwargs['projection']).distinct(kwargs['field_name'])

