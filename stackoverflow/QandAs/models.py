
import pymongo
from django.conf import settings
from django.core import exceptions
from bson import Code
from mongoengine import Document, EmbeddedDocument, fields
from djongo import models
import logging
logger = logging.getLogger(__name__)

def get_client(name, db_name):
    if not hasattr(settings, "MONGO"):
        raise exceptions.ImproperlyConfigured("Settings for MONGODB not found")

    auth_string = ""
    if settings.MONGO[name].get('USERNAME') and settings.MONGO[name].get('USERNAME'):
        auth_string = f"{settings.MONGO[name]['USERNAME']}:{settings.MONGO[name]['PASSWORD']}@"
    connection_string = (
        f'mongodb://{auth_string}{getattr(settings.MONGO[name], "HOST", settings.MONGO[name]["HOST"])}:'
        f'{getattr(settings.MONGO[name], "PORT", 27017)}/'
        f'{db_name}'
    )
    print(connection_string)
    client = pymongo.MongoClient(connection_string)
    return client

calling = 0

def get_mongo_database(db_name, client=None, namespace=None, db_details="default"):
    client = client or get_client(db_details, db_name)
    default_namespace = settings.MONGO[db_details].get("NAMESPACE", "nullspace")
    namespace = namespace or default_namespace
    print("created connection " )

    return client[f"{db_name}"]

class BaseMongoModel(object):
    def __init__(self, client, entity):
        self.client = client[entity]
        self.base_client = client[entity]
        self.base_data = None
        self.filters = {"custom": {}}
        self._keys = self.__keys__()

    @staticmethod
    def _find_first(entities, value, key="id"):
        for i, dic in enumerate(entities):
            if dic[key] == value:
                return i
        return -1

    @property
    def keys(self):
        return self._keys

    def get_filters(self):
        self.filters = {"custom": {}}
        for k in self.keys:
            self.filters[k] = self.client.distinct(k)
        pregen_filters = list(
            self.base_client["metadata"]["filters"][f"{self.collection_name}s"].find()
        )
        for f in pregen_filters:
            f.pop("_id")
            self.filters["custom"].update(f)
        return self.filters

    def __keys__(self):
        key_map = Code("function() { for (var key in this) { emit(key, null); } }")
        reduce = Code("function(key, stuff) { return null; }")
        try:
            result = self.client.map_reduce(
                key_map, reduce, f"{self.client.full_name}_keys"
            )
            keys = result.distinct("_id")
            if keys:
                keys.remove("_id")
        except pymongo.errors.OperationFailure as e:
            logger.error(
                f"Key list generation failed, unable to find collection: {self.client.full_name}"
            )
            return []
        return keys

    def get_all(self):
        return self.client.find()

    def get_one_by_key(self, key_name, key_value):
        self.base_data = self.client.find_one({key_name: key_value})
        return self.base_data

    def update_entity(self, id, key_name, key_value, defer_update=False):
        spec = {"id": id}
        update_key = {"$set": {key_name: key_value}}
        result = self.base_client.update_one(
            filter=spec, update=update_key
        )

        return True

    def create_entity(self):
        if type(self.base_data) is not dict:
            raise Exception(
                f"Only dicts can be added to a collection, received a {type(self.base_data)}"
            )
        #import pdb;pdb.set_trace()
        self.base_client.insert_one(self.base_data)
        #self.__rebuild_meta__()
        return True


    def delete_by_id(self, qa_id):
        spec = {"id": qa_id}
        return self.client.delete_one(filter=spec)


class Foo(BaseMongoModel):
    def __init__(self, connection):
        super().__init__(connection, "foo")

class Question(BaseMongoModel):
    def __init__(self, connection):
        super().__init__(connection, "questions")

class Answer(BaseMongoModel):
    def __init__(self, connection):
        super().__init__(connection, "answers")

class Comment(BaseMongoModel):
    def __init__(self, connection):
        super().__init__(connection, "comments")

class UpVote(BaseMongoModel):
    def __init__(self, connection):
        super().__init__(connection, "upvotes")


'''
class Question():
    question_id = models.IntegerField()
    question_text = models.CharField(max_length=200)
    question_description = models.CharField(max_length=500)


class Answer():
    answer_id = models.IntegerField()
    answer_text = models.CharField(max_length=500)
    question_ref = models.EmbeddedModelField(model_container=Question)
'''
