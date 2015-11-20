import imp
twi = imp.load_source('twi', 'libs/twitter.py')

api = twi.begin(1)