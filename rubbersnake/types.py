# -*- coding:utf-8 -*-
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

import sys
import datetime
from .exceptions import *

class _BaseType(object):
    '''
    Common type properties and validations
    '''

    def __init__(self, default=None, max=None, min=None, null=False, mapping={}):
        #Parent class is specified in each type class, not here
        self.default = default() if hasattr(default, '__call__') else default
        self.max = max
        self.min = min
        self.null = null

        self.mapping = mapping

    def map(self):
        mapping = self.mapping.copy()
        if self.eltype is not None and "type" not in mapping:
            mapping["type"] = self.eltype
        return mapping if mapping else None

    def validate(self, value):

        #Validations that should be done for all types
        if self.null and value is None:
            return #No need to go any further

        #Validate against parent types
        if True not in [isinstance(value, i) for i in self.parent]:
            raise ValueError("Value '{0}' not allowed".format(value))

class String(_BaseType):
    '''
    String type
    '''

    def __init__(self, **kwargs):

        self.parent = [str]
        self.eltype = "string"

        #Unicode is deprecated in Py3K
        if sys.version_info[0] < 3:
            self.parent.append(unicode)
            
        super(String, self).__init__(**kwargs)

    def validate(self, value):
        super(String, self).validate(value)

        if value:
            if self.max and len(value) > self.max:
                raise ValueTooLargeException()
            if self.min and len(value) < self.min:
                raise ValueTooSmallException()

class Bool(_BaseType):
    '''
    Boolean type
    '''

    parent = [bool]
    eltype = "boolean"

class Num(_BaseType):
    '''
    Numeric type
    '''

    parent = [int, float]
    eltype = "integer"

    def validate(self, value):
        super(Num, self).validate(value)

        if value:
            if self.max and value > self.max:
                raise ValueTooLargeException()
            if self.min and value < self.min:
                raise ValueTooSmallException()

class DateTime(_BaseType):
    '''
    DateTime type
    '''

    parent = [datetime.datetime]
    eltype = "date"

    def validate(self, value):
        super(DateTime, self).validate(value)

        if value:
            if self.max and value > self.max:
                raise ValueTooLargeException()
            if self.min and value < self.min:
                raise ValueTooSmallException()

class Enum(_BaseType):
    '''
    Enum type
    '''

    def __init__(self, *values, **kwargs):
        self._values = values
        self.eltype = None
        super(Enum, self).__init__(**kwargs)

    def validate(self, value):
        if value not in self._values:
            raise ValueException("Value {0} not valid for this enum".format(value))

class List(_BaseType):
    '''
    List type
    '''

    def __init__(self, *args, **kwargs):
        self.parent = args
        if "default" not in kwargs:
            kwargs["default"] = []
        super(List, self).__init__(**kwargs)

    def map(self):
        return None #Lists not supported yet

    def validate(self, value):
        #No need to run validation if null is allowed and value is null
        if self.null and value == None:
            return

        if not isinstance(value, tuple) and not isinstance(value, list):
            raise ValueException("List neither tuple nor list")

        for i in value:
            valid = False
            for p in self.parent:
                try:
                    p.validate(i)
                    valid = True
                except Exception as e:
                    pass
            if not valid:
                raise ValueError("Value '{0}' not allowed".format(i))

class Dict(_BaseType):
    '''
    Dict type
    '''

    parent = [dict]

    def __init__(self, comp={}, **kwargs):
        self._comp = comp

        if kwargs.get("null"):
            default = None
        else:
            default = {}
            for key in comp:
                if isinstance(comp[key], _BaseType):
                    value = comp[key].default
                    if hasattr(value, "__call__"):
                        value = value()
                    default[key] = value

        kwargs["default"] = default
        super(Dict, self).__init__(**kwargs)

    def map(self):

        mapping = {}
        for key in self._comp:
            current = {}
            if current is not None:
                mapping[key] = self._comp[key].map()

        return {
            "type": "object",
            "properties": mapping
        }

    def validate(self, value):
        #No need to run validation if null is allowed and value is null
        if self.null and value == None:
            return

        if value == None:
            raise ValueNullException()

        for key in self._comp.keys():
            self._comp[key].validate(value.get(key))
