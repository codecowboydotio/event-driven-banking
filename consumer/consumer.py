import twitter
from kafka import KafkaConsumer
from kafka.errors import KafkaError


consumer_key=''
consumer_secret=''
access_token_key=''
access_token_secret=''
kafka_topic= 'my-kafka-topic'
kafka_host='[x.x.x.x:9092]'

try:
  consumer = KafkaConsumer(kafka_topic, group_id = 'group1',
                           bootstrap_servers = kafka_host)
  for message in consumer:
    print("Topic Name=%s, Message=%s"%(message.topic, message.value))
    api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)
    #print(api.VerifyCredentials())
    #status = api.PostUpdate(message.value)
except Exception as e:
  print(e)

