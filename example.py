#!/usr/bin/env python

import rubbersnake as rs
import datetime

ServerPool = rs.ElasticPool()

class User(rs.Model):

    #Index is a mandatory mapping
    _index = "users"
    _pool = ServerPool

    username = rs.types.String()
    active = rs.types.Bool(default=True)
    age = rs.types.Num()
    registrationdate = rs.types.DateTime(default=lambda : datetime.datetime.utcnow())
    userlevel = rs.types.Enum("MEMBER", "ADMIN", default="MEMBER")

users = [
    User({
        "username": "AOEU",
        "age": i,
        "example": ["A", 3],
        "profile": {
            "test": "AOEU"
        }
    })
    for i in range(1,5)]
users = rs.Query(User).search({})
users = rs.Query.save(users)


#print(users)
#rs.Query(User).delete(users)
#rs.Query.delete("oVgYn55sSWmml-QTVwC7zg", _index="users", _type="User", pool=ServerPool)
