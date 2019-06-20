import os
import datetime
import sys

from simplecrypt import encrypt, decrypt
from pymongo import MongoClient
from mongoengine import connect

from northstar_cloud.common import logs as logging
from northstar_cloud.common import utils as c_utils

encKey = b'c\xf8\xccH\xbe\x7ffp\xda\xe4\xa4TY\x03\x85CR<\x97f'

LOG = logging.getLogger(__name__)

DEFAULT_FILE_PATH = "etc/northstar-service-config.json"

ROOT_DIR = os.path.abspath(os.curdir)
NORTHSTAR_SERVICE_PATH = ROOT_DIR + "/" + DEFAULT_FILE_PATH


class Client(object):
    pass


class MongoPymongoDB(Client):
    def __init__(self, mongo_host, mongo_port):
        self.mongo_client = None
        self.mongo_host = host
        self.mongo_port = port
        self.mongo_url_path = "mongodb://"

    def make_connection(self):
        try:
            # client = MongoClient('mongodb://localhost:27017')
            self.mongo_client = MongoClient(self.mongo_url_path + self.mongo_host + ":" + self.mongo_port)
        except:
            LOG.exception("Error: Unable to connect to the databases")

    @property
    def mongoclient(self):
        return self.mongo_client

    def get_connection(self):
        return self.mongo_client


class MongoEnginDB(object):
    def __init__(self, db_name, host, port):
        self.db_name = db_name
        self.host = host
        self.port = port

    def connect_to_engine(self):
        try:
            return connect(self.db_name, host=self.host + ":" + self.port, alias='default')
        except Exception as e:
            raise e

def get_db_connection(config_path=None):
    if not config_path:
        config_path = NORTHSTAR_SERVICE_PATH

    config = c_utils.read_json_file(config_path)
    if config['db'] == 'mongo':
        db_client = MongoEnginDB(config['db_name'], config['db_host'], config['db_port'])
        return db_client.connect_to_engine()

    return None
