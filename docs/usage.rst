.. _ref-usage:

============
Usage
============

1. Rename settings.example.py as settings.py

Example of console script:

	os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")

	goz = Gozokia()
	goz.initialize()
	goz.console()Rename settings.example.py as settings.py
