
Gozokia
=======

[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)
[![Build Status](https://travis-ci.org/avara1986/gozokia.svg)](https://travis-ci.org/avara1986/gozokia)
[![Coverage Status](https://coveralls.io/repos/avara1986/gozokia/badge.svg?branch=master&service=github)](https://coveralls.io/github/avara1986/gozokia?branch=master)
[![Requirements Status](https://requires.io/github/avara1986/gozokia/requirements.svg?branch=master)](https://requires.io/github/avara1986/gozokia/requirements/?branch=master)
Installation from repo
----------------------
* Clone the project
```
#!bash
git clone https://github.com/avara1986/gozokia.git
```
* Install Python dependencies
```
#!bash
pip install -r requirements.txt
```
* Install Linux dependencies
```
#!bash
sudo apt-get install python3-dev
sudo apt-get install portaudio19-dev
```

Rename settings.example.py as settings.py

Example of console script:
```
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")

goz = Gozokia()
goz.initialize()
goz.console()
```

Run console gozokia
-------------------
```
python -m gozokia
```


Run examples
------------
If you clone the git repo, you can run the examples:

```
#!bash
./example/main.py
```


Testing
-------
* Install Python dependencies
```
#!bash
pip install tox
```
* Running the tests
```
#!bash
./test
```

Docs
-------

sphinx-build -b html docs docs/_build

License
=======

This software is licensed under the `The MIT License (MIT)`. See the ``LICENSE``
file in the top distribution directory for the full license text.