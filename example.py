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
    registrationdate = rs.types.DateTime(default=lambda : datetime.datetime.utcnow())
    userlevel = rs.types.Enum("MEMBER", "ADMIN", default="MEMBER")

    testlist = rs.types.List(rs.types.Num())

    searchprofile = rs.types.Dict({
        "lookingForMinAge": rs.types.Num(min=18, max=99, default=18),
        "lookingForMaxAge": rs.types.Num(min=18, max=99, default=99),
        "testhest": rs.types.Dict({
            "a": rs.types.Num(default=10),
            "b": rs.types.Num(default=20)
        })
    })

users = [
    User({
        "username": "AOEU",
        "example": ["A", 3],
        "profile": {
            "test": "AOEU"
        }
    })
    for i in range(1,2)]
#users = rs.Query.save(users)
#users = rs.Query(User).search({})
for user in users:
    user.testlist = ["A"]
    #user. searchprofile["testhest"]["a"] = "AOEU"
    user.__validate__()

#print(users)
#rs.Query(User).delete(users)
#rs.Query.delete("oVgYn55sSWmml-QTVwC7zg", _index="users", _type="User", pool=ServerPool)
