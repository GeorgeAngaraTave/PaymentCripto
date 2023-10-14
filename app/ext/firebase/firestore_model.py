# -*- coding: utf-8 -*-

"""Python module for Google Cloud Firestore."""

import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from app.ext.utils import DateUtils, Commons
from .geo_hash import encode, decode
from app.ext.utils import haversine

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

try:
    db = firestore.Client()
except Exception as e:
    print("Firestore Client Exception:", e)
    raise e


def get_by():
    return [1, 2]


class Query:
    """ A class representing a query on a collection """

    def __init__(self, query_params, to_json=True):
        print("Query init", self)
        self.cls = self
        self.result = None
        self.q = None

    @staticmethod
    def and_(self, query_params, to_json=True):
        print("Query and_")
        print("Query and_ cls", self)
        print("Query and_ query_params", query_params)
        print("Query and_ to_json", to_json)
        self.result = None
        print("self.cls.__tablename__:", self.__tablename__)
        self.q = db.collection(self.__tablename__)

        # parse the params
        for param in query_params:
            if len(param) == 2:
                print("and_ entro param 2")
                self.q = self.q.where(param[0], '==', param[1])
            if len(param) == 3:
                print("and_ entro param 3")
                self.q = self.q.where(*param)

        result = self.q.get()

        print('Query and_ result:', result)
        if to_json is True:
            resp = self.to_json(result, True)
            return resp
        else:
            return result

    @staticmethod
    def or_(self, query_params=None, to_json=True):
        print("Query or_")
        print("Query or_ cls", self)
        print("Query or_ query_params", query_params)
        print("Query or_ to_json", to_json)
        self.result = None
        print("self.cls.__tablename__:", self.__tablename__)
        self.q = db.collection(self.__tablename__)

        try:
            collection = self.__tablename__
            doc_ref = db.collection(collection)

            for param in query_params:
                if len(param) == 2:
                    print("or_ entro param 2")
                    doc_ref.where(param[0], '==', param[1])
                if len(param) == 3:
                    print("or_ entro param 3")
                    doc_ref.where(*param)

            result = doc_ref.get()

            print('or_ result:', result)
            if to_json is True:
                resp = self.to_json(result, True)
                return resp
            else:
                return result

        except Exception as e:
            print('FirestoreModel or_ Exception', e)
            return e

    def get(self):
        print("Query get")
        """ Executes the query
            @return Generator object that yields hydrated instances of the class supplied __init__
        """
        self.result = self.q.get()
        try:
            for r in self.result:
                yield r
        except Exception as e:
            print('Query result get Exception', e)
            raise e


class FirestoreModel:

    @classmethod
    def dict_to_obj(cls, _dict=None, _name='from_dict'):
        if _dict is None:
            return None
        try:
            new_obj = type(_name, (object,), _dict)
            return new_obj
        except Exception as e:
            print('FirestoreModel dict_to_obj Exception', e)
            return None

    @staticmethod
    def to_json(docs, key=False):
        try:
            obj = {}
            array_result = []

            for item in docs:
                obj = item.to_dict()
                if key is True:
                    obj['key'] = item.id
                array_result.append(obj)
            return array_result
        except Exception as e:
            print('FirestoreModel to_json Exception', e)
            return None

    @classmethod
    def save(self, data=None):
        if data is None:
            return None

        try:
            collection = self.__tablename__

            data.created_at = DateUtils.get_timestamp()
            doc_ref = db.collection(collection)
            doc_ref.add(data.__dict__)
            return None
        except Exception as e:
            print('Firestore save Exception', e)
            return e

    @classmethod
    def get_all(self):
        try:
            the_coll = self.__tablename__
            users_ref = db.collection(the_coll)
            docs = users_ref.get()
            result = self.to_json(docs, True)
            return result
        except Exception as e:
            print("FirestoreModel get_all Exception:", e)
            return e

    @classmethod
    def get_by(self, key, value):
        if key is None:
            return None

        if value is None:
            return None
        try:
            collection = self.__tablename__
            doc_ref = db.collection(collection)
            docs = doc_ref.where(key, '==', str(value)).get()
            result = self.to_json(docs, True)

            if Commons.is_iterable(result):
                if len(result) == 0:
                    return None
                else:
                    return result
            else:
                print("FirestoreModel get_by Exception: Result is not Iterarable")
                return None
        except Exception as e:
            print("FirestoreModel get_by Exception:", e)
            return e

    @classmethod
    def get_by_id(self, key, as_object=False):
        if key is None:
            return None

        try:
            collection = self.__tablename__
            users_ref = db.collection(collection).document(str(key))
            docs = users_ref.get()
            result = docs.to_dict()

            if result is None:
                return None
            else:
                if as_object is True:
                    return self.dict_to_obj(result)
                return result
        except Exception as e:
            print('Firestore get_by_id Exception', e)
            return e

    @classmethod
    def get_ref(self):

        try:
            collection = self.__tablename__
            doc_ref = db.collection(collection)
            return doc_ref
        except Exception as e:
            print('FirestoreModel query Exception', e)
            return e

    @classmethod
    def get_radius(self, coord=None, radio=10):
        pass

    @classmethod
    def geo_point(self, lat=None, lon=None):
        if lat is None:
            return None
        if lon is None:
            return None

        return firestore.GeoPoint(float(lat), float(lon))

    @classmethod
    def from_geo_point(self, coords=None):
        if coords is None:
            return None

        return {
            'latitude': coords.latitude,
            'longitude': coords.longitude
        }

    @classmethod
    def raw_query(self, params=None, to_json=True):

        try:
            collection = self.__tablename__
            doc_ref = db.collection(collection)

            for param in params:
                doc_ref.where(*param)

            result = doc_ref.get()

            print('raw_query result:', result)
            if to_json is True:
                resp = self.to_json(result, True)
                return resp
            else:
                return result

        except Exception as e:
            print('FirestoreModel raw_query Exception', e)
            return e

    @classmethod
    def or_(cls, q=(), to_json=True):
        """ Get a handle to a query object (see Query or_ helper class above)
        @param cls The class of the instance calling make
        @param q A list of query key/value or key/operator/value pairs (
        """
        print("FirestoreModel or_", q)
        return Query.or_(cls, q, to_json)

    @classmethod
    def and_(cls, q=(), to_json=True):
        print("FirestoreModel and_:", q)
        """ Get a handle to a query object (see Query and_ helper class above)
        @param cls The class of the instance calling make
        @param q A list of query key/value or key/operator/value pairs (
        """
        return Query.and_(cls, q, to_json)

    @classmethod
    def get(cls, doc_id, raise_exception=False):
        """ Get a single model instance
        @param cls The class of the instance calling make
        @param doc_id The id of the document to get
        @return A model instance of type class hydrated w/ data from the database
        """
        print("FirestoreModel get", doc_id, raise_exception)
        try:
            doc_ref = db.collection(cls.__tablename__).document(doc_id).get()
            return cls(**doc_ref.to_dict())
        except Exception as e:
            print('FirestoreModel get Exception', e)
            if raise_exception:
                raise e
        return None

    @classmethod
    def update(self, key=None, data=None):
        if key is None:
            return None

        if data is None:
            return None

        try:
            collection = self.__tablename__
            city_ref = db.collection(collection).document(key)
            data['updated_at'] = DateUtils.get_timestamp()
            city_ref.update(data)
            # info = data.__dict__
            # info.update({'updated_at': DateUtils.get_timestamp()})
            # city_ref.update(data)
            return None
        except Exception as e:
            print('Firestore update Exception', e)
            return e

    @classmethod
    def delete(self, key=None):
        try:
            collection = self.__tablename__
            db.collection(collection).document(key).delete()
            return None
        except Exception as e:
            print('Firestore delete Exception', e)
            return e
