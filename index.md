# Event Driven Banking with UP Bank

## What is this?
Recetly, a neo bank that I am a member of released a new API. 
This API has the usual banking related functions, get your account details, view your transactions and so on.

The developer docs are available here: https://developer.up.com.au

What caught my eye though was this: https://developer.up.com.au/#get_webhooks

## A lightbulb moment

When I read about arbitrary webhooks for my bank account, a lightbulb went off in my head.
I can do **anything** with an arbitrary webhook.

It occurred to me that by sending data in a real time fashion to an **arbitrary** **webhook** that what the UP team had done was create a situation where I could start to use **real time event driven banking**. The possibilities immediately struck me as being endless. 

## Enter Kafka

If we are going to talk about event driven architecture, then the software for me is definitely Kafka (yes there are others, but I'm comfortable with Kafka). 
I began to wonder if my bank would send an event to my webhook, and my webhook could act as a Kafka producer and post an event for me. I could then have one (or more) consumers come along and pick up these events and do something else with them. 

I could: 

- Post a picture to twitter
- Pull data from my event bus and push into accounting software
- Calulate my real time financial position and reconcile as events come in (no overnight processing).

...the possibilities are really only limited by my imagination.


## The end to end architecture
The architecture is very simple. It is completely event driven, and everything occurs in real time. 
Consider the following:
- I transfer money from my account to someone else
- This creates a new transactions
- This transaction triggers my webhook that I have configured against my bank account
- Webhook sends transaction data to my listener
- My listener authenticates the message
- My listener pushes portions of the incoming message to Kafka
- I have a consumer configured to listen to the same topic I'm pushing events to
- My consumer processes the event and does **something** with it

![End to End Architecture](/Architecture.PNG)


## How do I get started?
There are a few things you need to do before you can get started. 
- Get a bank account with UP
- Get an API key for your account

Once you've done both of these things, then you can start to configure your account.

### Create a webhook
There are a few calls that you need to perform in order to configure a webhook within your bank account.

The main things to configure as part of the create call are:
- Authorization header (this is your API key)
- url (this is address and uri of your code)
- description (this is the description of your webhook)

```
#curl https://api.up.com.au/api/v1/webhooks \
  -XPOST \
  -H 'Authorization: your-token' \
  -H 'Content-Type: application/json' \
  --data-binary '{
    "data": {
      "attributes": {
        "url": "http://mywebhook.com/webhook",
        "description": "Example webhook"
      }
    }
  }'
```

### Data that is returned
The curl call above will return a blob of data that contains a **secret key**. 
The **secret key** is important to save away (and not share) - it will be used later to authenticate incoming requests.

```
{
    "data": {
        "type": "webhooks",
        "id": "XXX-a697-290df70f8298",
        "attributes": {
            "url": "http://x.x.x.x/",
            "description": "Test webhook",
            "secretKey": "TIGC3OcKKJOBQ7jClQQ5oLCiDlYPFYsKgKTr",
            "createdAt": "2020-08-19T20:30:17+10:00"
        },
        "relationships": {
            "logs": {
                "links": {
                    "related": "https://api.up.com.au/api/v1/webhooks/XXX-a697-290df70f8298/logs"
                }
            }
        },
        "links": {
            "self": "https://api.up.com.au/api/v1/webhooks/XXX-a697-290df70f8298"
        }
    }
}
```

...it's that simple - **you have created a webhook for your bank account.**
New transactions in your bank account will trigger events to be sent to your webhook.

## The Listener and Kafka Producer
Now that I have my bank account with a webhook, it will be sending transaction data to my endpoint. 
I need to have something to listen for incoming requests, and handle these incoming requests. 
In my case, I have decided to do two things, handle incoming requests, parse them for the transaction URL, and pass that URL to a Kafka topic.
It looks like the diagram below.


![Listener and Producer](/ListenerProducer.png)

## The Code

```
from flask import Flask, request, Response  #import main Flask class and request object
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import hmac
import hashlib
import base64
import codecs

app = Flask(__name__) #create the Flask app
app.config.from_object('config.ProductionConfig')

@app.route('/', methods=['POST'])
def processrequest():
  try:
    auth_header = request.headers[app.config['HEADER']]
    app_debug = app.config['APP_DEBUG']
    debug_header = app.config['DEBUG_HEADER']
    debug_footer = app.config['DEBUG_FOOTER']
    expected_user_agent = app.config['USER_AGENT']
    key = app.config['KEY'].encode("ascii") #ascii encoding returns a byte object
    rawdata = request.get_data()
    data = request.get_json()

    h = hmac.new(key, rawdata, hashlib.sha256 ) # byte object in should compute the same hash as the header
    computed_hmac = h.hexdigest()

    if auth_header == computed_hmac:
      if app_debug.lower() == 'true':
        print(debug_header)
        print('Auth Header: ', auth_header)
        print('Computed HMAC: ', computed_hmac)
        print(debug_footer)
      eventType = (data['data']['attributes']['eventType'])
      eventCreated = (data['data']['attributes']['createdAt'])
      transactionUrl = (data['data']['relationships']['transaction']['links']['related'])

      khost = app.config['KHOST']
      ktopic = app.config['KTOPIC']
      if app_debug.lower() == 'true':
        print (debug_header)
        print ('Kafka Host: ', khost, '\nKafka Topic: ', ktopic)
        print ('Event Type: ', eventType, '\nEvent Created: ', eventCreated, '\nTransaction Url: ', transactionUrl)
        print ('Raw Data: ', rawdata)
        print (debug_footer)
      try:
        producer = KafkaProducer(
          value_serializer=lambda v: json.dumps(v).encode('utf-8'),
          bootstrap_servers=khost)
        kafka_payload=transactionUrl
        kafka_topic = ktopic
        producer.send(kafka_topic, kafka_payload)
        producer.flush()
      except Exception as e:
        if app_debug.lower() == 'true':
          print (debug_header)
          print ('Kafka problem: ', e)
          print (debug_footer)
        return Response("{Data: 'Kafka Error'}", status=400, mimetype='application/json')
      return Response("{'Data':'all good'}", status=200, mimetype='application/json')
    else:
      print ('HEader doesn\'t match')
      print(debug_header)
      print('Auth Header: ', auth_header)
      print('Computed HMAC: ', computed_hmac)
      print(debug_footer)
      return Response("{'Data':'authentication does not match'}", status=403, mimetype='application/json')
  except Exception as exc:
    print(exc)
    return Response("{'Data':'authentication was not present'}", status=403, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80) #run app in debug mode on port 80

```
