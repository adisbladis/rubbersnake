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

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.org")).read()

install_requires = [
    'requests>=0.5.2'
]

classifiers = [
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules"
]

setup(name='rubbersnake',
      version='0.0.1',
      description='Python model mapper for elasticsearch',
      long_description=README,
      author='Adam Höse',
      author_email='@adisbladis',
      license='Apache-2.0',
      download_url='https://github.com/adisbladis/rubbersnake/tarball/master',
      url='https://github.com/adisbladis/rubbersnake',
      include_package_data=True,
      zip_safe=False,
      classifiers=classifiers,
      install_requires=install_requires,
      packages=find_packages()
      )
