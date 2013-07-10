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

from .types import _BaseType
from . import json


class Model(object):
    '''
    Base model
    '''

    def __init__(self, data=None):

        #Set default values
        for i in self.__properties__:
            default = getattr(self.__class__, i).default
            if hasattr(default, '__call__'):
                default = default()
            setattr(self, i, default)

        if data:
            self.__load__(data)

    def __load__(self, data):
        '''
        Load a dict into model instance
        '''

        self.id = data.get("_id", data.get("id"))
        data = data.get("_source") if "_source" in data else data
        for i in self.__properties__:
            val = data.get(i)
            if val is not None:
                setattr(self, i, val)

    def __mapping__(self):
        '''
        Generate mapping dict for model instance
        '''

        #Get mappings from properties
        properties = {} 
        for i in self.__properties__:
            current = getattr(self.__class__, i).map()
            if current is not None:
                properties[i] = current

        mapping = self._mapping if hasattr(self, "_mapping") else {}
        if not isinstance(mapping, dict):
            raise ValueError("_mapping is not dict")

        mapping["properties"] = properties
        return {self.__class__.__name__: mapping}

    def __validate__(self):
        '''
        Validate model
        '''

        if not hasattr(self, "_index"):
            raise ValueError("Missing _index mapping")

        if not hasattr(self, "_pool"):
            raise ValueError("Missing _pool mapping")

        for i in self.__properties__:
            getattr(self.__class__, i).validate(getattr(self, i))

    @property
    def __properties__(self):
        '''
        List type properties
        '''

        return [i for i in dir(self.__class__)
                if isinstance(getattr(self.__class__, i), _BaseType)]

    @property
    def __json__(self):
        '''
        JSON representation for model
        '''

        d = self.__dict__
        d["_id"] = self.id
        return json.dumps(d)
