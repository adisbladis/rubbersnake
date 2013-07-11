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

import rawes
import random


class ElasticPool(object):
    '''
    Pool of hostnames
    '''
    def __init__(self, urls=["http://localhost:9200"], timeout=30, **kwargs):
        self.pool = {}
        for url in urls:
            self.add(url, timeout, **kwargs)

    @property
    def es(self):
        '''
        Get a random rawes instance from the pool
        '''
        key = random.choice(self.pool.keys())
        return rawes.Elastic(url=key, timeout=self.pool[key]["timeout"], **self.pool[key]["kwargs"])

    def add(self, url, timeout=30, **kwargs):
        '''
        Add a connection to the pool
        '''
        self.pool[url] = {
            "kwargs": kwargs,
            "timeout": timeout
        }

    def remove(self, url):
        '''
        Remove a server from the pool
        '''
        del self.pool[url]
