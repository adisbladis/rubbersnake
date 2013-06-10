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

try:
    import simplejson as json
except ImportError:
    import json
import dateutil.parser
import datetime
import sys
import re


def default_json_dumps(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("{0} is not JSON serializable".format(repr(obj)))


def default_json_loads(data):
    for k, v in data.items():
        if isinstance(v, str) or (isinstance(v, unicode) if sys.version_info[0] == 2 else False):
            if re.match("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", v):
                try:
                    data[k] = dateutil.parser.parse(v)
                except ValueError:
                    pass
    return data


def dumps(data):
    '''
    Encode dict to json string with proper datetime-formatting
    '''
    return json.dumps(data, default=default_json_dumps)


def loads(data):
    '''
    Load json string with proper datetime loading
    '''
    return json.loads(data, object_hook=default_json_loads)
