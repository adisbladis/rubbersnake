#!/usr/bin/env python
'''
Simple usage example of rubbersnake
'''

import rubbersnake as rs
import datetime

#Instantiate a pool
ServerPool = rs.ElasticPool()

class User(rs.Model):

    #Index is a mandatory mapping
    _index = "users"
    #A model must have a _pool mapping
    _pool = ServerPool

    #User properties
    username = rs.types.String(mapping={"index": "not_analyzed"})
    active = rs.types.Bool(default=True)
    userlevel = rs.types.Enum("MEMBER", "ADMIN", default="MEMBER")

    #Callables are fine as default values too
    registrationdate = rs.types.DateTime(default=lambda : datetime.datetime.utcnow())

    profile = rs.types.Dict({
        #A list of strings with max length 100 chars
        "interests": rs.types.List(rs.types.String(max=100))
    })

#Get a mapping dict for the model
User().__mapping__()

exit(0)
#Instantiate a new user and save it
#Before save a model is always validated
user = User({
    "username": "foobar",
})
user = rs.Query.save(user)
print("Created user {0}".format(user._id))

#You can also trigger validations manually
user.__validate__()

#Finally, lets delete the user we just created
#Delete accepts an id, a model instance or a list
rs.Query.delete(user)
print("Deleted user")
#Or the more raw approach
rs.Query.delete("userid", _index="users", _type="User", pool=ServerPool)
