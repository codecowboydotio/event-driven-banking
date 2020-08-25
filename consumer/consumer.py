import twitter
import requests
from kafka import KafkaConsumer
from kafka.errors import KafkaError


consumer_key=''
consumer_secret=''
access_token_key=''
access_token_secret=''
kafka_topic= 'my-kafka-topic'
kafka_host='[localhost:9092]'
up_token = ''

try:
  consumer = KafkaConsumer(kafka_topic, group_id = 'group1',
                           bootstrap_servers = kafka_host)
  for message in consumer:
    print("Topic Name=%s, Message=%s"%(message.topic, message.value))
    url = message.value.decode('utf-8').strip('\"') # lazy hack 
    print(url)
    response = requests.get(url,
                          headers={"Authorization": up_token}
                          )
    data = response.json()
    value = (data['data']['attributes']['amount']['value'])
    currency = (data['data']['attributes']['amount']['currencyCode'])
    print(value, currency)
    api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)
    tweet = "Another something just happened in my @up_banking account. This message arrived via #Kafka, and tells me the value of my bank transation was {} {} #api #python #eventdrivenbanking".format(value, currency)
    print(tweet)
    status = api.PostUpdate(tweet)
except Exception as e:
  print(e)

