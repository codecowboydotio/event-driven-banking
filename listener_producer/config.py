class Config(object):
  HEADER = 'X-Up-Authenticity-Signature'


class TestingConfig(Config):
  HEADER = 'svk-header'

class ProductionConfig(Config):
  HEADER = 'X-Up-Authenticity-Signature'
  KEY = 'put-your-secret-key-here''
  KTOPIC = 'my-kafka-topic'
  KHOST = '10.1.1.154:9092'
  USER_AGENT = 'Up Webhook Dispatcher'
  APP_DEBUG = 'true'
  DEBUG_HEADER = '========DEBUG=BEGIN========='
  DEBUG_FOOTER = '========DEBUG=END==========='
