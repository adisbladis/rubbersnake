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


class _BaseException(Exception):

    #Make it possible to set default values for an exception class
    def __init__(self, value=None):
        if value:
            self.value = value

    def __str__(self, *args, **kwargs):
        if self.value:
            return repr(self.value)
        else:
            return super(BaseException, self).__str__(self, *args, **kwargs)


class NotImplementedError(_BaseException):
    pass


class ValueNullException(_BaseException):
    value = "Null/empty value not allowed"


class ValueTooLargeException(_BaseException):
    value = "Value larger than specified max"


class ValueTooSmallException(_BaseException):
    value = "Value smaller than specified min"


class ValueException(_BaseException):
    value = "Value of wrong type"


class ModelException(_BaseException):
    value = "Value not model instance"
