import os

class ProductionConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'is-it-a-bottle-of-wine-in-your-pocket, or are you just happy to see me ?' #TODO change the token later?
    DEBUG=False