# -*- coding: utf-8 -*-
#
#   Copyright 2013 Adam Höse <adis AT blad DOT is>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import copy
import urllib
from . import json
from .model import Model


class Query(object):

    def __init__(self, *models):
        self.models = models
        self.modelmap = {}
        for i in self.models:
            self.modelmap["/".join((i._index, i.__name__))] = i

    @property
    def __basestring__(self):
        '''
        Base string (e.g twitter/tweet)
        '''
        indices = []
        types = []
        for i in self.models:
            try:
                indices.append(i._index)
            except AttributeError:
                raise AttributeError("Missing _index mapping for model '{0}'"
                                     .format(i.__name__))
            types.append(i.__name__)

        return "/".join((
            ",".join(indices),
            ",".join(types)))

    def map(self, results):
        '''
        Map a set of documents to models
        '''

        ret = []
        for i in results:
            doc = i.get("_source")
            doc["id"] = i["_id"]
            ret.append(self.modelmap["/".join((i["_index"], i["_type"]))](doc))
        return ret

    def search(self, query={}, **kwargs):
        '''
        Search elastic and map results to models
        '''
        path = "/".join((
            self.__basestring__,
            "_search?{0}".format(
                urllib.urlencode(kwargs.items())
            )))

        return self.map(
            self.models[0]._pool.es.get(path, data=query, json_decoder=json.loads).get("hits", {}).get("hits"))

    @staticmethod
    def save(models):
        '''
        Save one or more model instances
        Returns models with populated ids

        Uses elasticsearch bulk api
        '''

        #Normalize data into list
        normalized = False
        if not isinstance(models, list):
            normalized = True
            models = [models]

        #Build request
        es = None
        request = []
        for i in models:
            if not es:
                es = i._pool.es
            i.__validate__()

            req = dict(i._options.items()+[("_index", i._index), ("_type", i.__class__.__name__)])
            req = {"index": req}
            if i.id is not None:
               req["index"]["_id"] = i.id
            request.append(req)
            for attr in ("id", "_options"):
                delattr(i, attr)
            request.append(i.__dict__)
        request = "\n".join([json.dumps(i) for i in request])
        request += "\n" #Trailing newline required

        for idx, item in enumerate(es.post("_bulk", data=request).get("items")):
            if "create" in item:
                models[idx].id = item.get("create").get("_id")

        if not normalized:
            return models
        else:
            return models[0]

    @staticmethod
    def delete(models, _index=None, _type=None, pool=None):
        '''
        Delete one or more models or ids
        '''

        #Normalize to bulk
        if not isinstance(models, list):
            models = [models]
        
        #Build query
        request = []

        for i in models:
            if isinstance(i, Model):
                if i.id == None: #Can't delete an unsaved model
                    continue
                if not pool:
                    pool = i._pool
                request.append({ "delete" : { "_index" : i._index, "_type" : i.__class__.__name__, "_id" : i.id}})
            else:
                if not _index or not _type:
                    raise ValueError("Value not model instance and missing _index or _type")
                if not pool:
                    raise ValueError("Value not model instance and missing pool")
                request.append({ "delete" : { "_index" : _index, "_type" : _type, "_id" : i}})
        request = "\n".join([json.dumps(i) for i in request])
        request += "\n" #Trailing newline required

        pool.es.post("_bulk", data=request)
