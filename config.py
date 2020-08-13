class Config(object):
  HEADER = 'X-Up-Authenticity-Signature'


class TestingConfig(Config):
  HEADER = 'svk-header'

class ProductionConfig(Config):
  HEADER = 'X-Up-Authenticity-Signature'
  KEY = 'authheader'
  KTOPIC = 'my-kafka-topic'
#  KHOST = '10.1.1.154:9092'
  KHOST = '13.54.231.149:9092'
  APP_DEBUG = 'true'
  DEBUG_HEADER = '========DEBUG=BEGIN========='
  DEBUG_FOOTER = '========DEBUG=END==========='
