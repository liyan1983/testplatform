#coding=utf-8

# C:\Program Files\MongoDB\Server\3.6\bin\mongod --dbpath=C:\Users\40556\mongodb\data

from pymongo import MongoClient


class Mongo(object):

    def __init__(self, host='127.0.0.1', port=27017):
        self.client = MongoClient(host, port)

    def get_all_collections(self, database):
        _database = self.client.get_database(database)
        return _database.collection_names()

    def insert(self, database, collection, documents):
        """
        :param database:
        :param collection:
        :param document:
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        if isinstance(documents, list):
            _collection.insert_many(documents)
        else:
            _collection.insert_one(documents)


    def delete(self, database, collection, filter):
        """
        :param database:
        :param collection:
        :param filter:
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        result = _collection.delete_many(filter)
        print(result)

    def update(self, database, collection, filter, document):
        """
        :param database:
        :param collection:
        :param filter:
        :param document:
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        _collection.update_one(filter, {'$set': document})

    def search(self, database, collection, filter):
        """
        :param database:
        :param collection:
        :param filter:
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        results = list(_collection.find(filter))
        for result in results:
            result['_id'] = str(result['_id'])
        return results

    def close(self):
        """
        :return:
        """
        self.client.close()

    def __del__(self):
        """
        :return:
        """
        self.client.close()


if __name__ == '__main__':
    mongo = Mongo()
    results = mongo.search("testfan", "test", {'age': 35})
    if results:
        results[0]['age'] = 33
        mongo.update("testfan", "test", {'age': 35}, results[0])
    # data = [
    #     {
    #         'name': '二猫',
    #         'age': 34,
    #         'sex': 'female',
    #         'hobbit': ['吃', '喝', '玩', '乐', '看电视剧']
    #     },
    #     {
    #         'name': '小猫',
    #         'age': 7,
    #         'sex': 'male',
    #         'hobbit': ['吃', '喝', '玩']
    #     }
    # ]
    # mongo.insert("testfan", "test", data)
    # mongo.delete("testfan", "test", {'age': 35})
    # results = mongo.search("testfan", "test", {})
    # print(results)
    # mongo.insert("testfan", "test", {
    #     "name": "大猫",
    #     "age": 35,
    #     "sex": "male",
    #     "hobbit": [
    #         "吃",
    #         "喝",
    #         "玩",
    #         "乐"
    #     ]
    # })