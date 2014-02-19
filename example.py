#!/usr/bin/env python
'''
Simple usage example of rubbersnake
'''

import rubbersnake as rs
import datetime
from pprint import pprint

class User(rs.Model):

    #User properties
    username = rs.types.String(mapping={"index": "not_analyzed"})
    active = rs.types.Bool(default=True)
    userlevel = rs.types.Enum("MEMBER", "ADMIN", default="MEMBER")

    #Callables are fine as default values too
    registrationdate = rs.types.DateTime(default=lambda : datetime.datetime.utcnow())

    meta = rs.types.Dict({
        "test": rs.types.String(null=True)
    }, mapping={
        "type": "nested"
    })

    #Optionally extra mappings can be added (properties will be overriden with your model data)
    #_mapping = {}

#Get a mapping dict for the model
pprint(User().__mapping__)

#Instantiate a new user and save it
user = User({
    "username": "foobar",
}, _parent="AOEU")
pprint(user.__dict__)

#You can also trigger validations manually
user.__validate__()
