from flask import Flask, request, Response  #import main Flask class and request object
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

app = Flask(__name__) #create the Flask app
app.config.from_object('config.ProductionConfig')

@app.route('/', methods=['POST'])
def processrequest():
  try:
    auth_header = request.headers[app.config['HEADER']]
    app_debug = app.config['APP_DEBUG']
    debug_header = app.config['DEBUG_HEADER']
    debug_footer = app.config['DEBUG_FOOTER']
    rawdata = request.get_data()
    data = request.get_json()
    if auth_header == app.config['KEY']:
      if app_debug.lower() == 'true':
        print(debug_header)
        print('Auth Header: ', auth_header)
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
      return Response("{'Data':'authentication does not match'}", status=403, mimetype='application/json')
  except:
    return Response("{'Data':'authentication was not present'}", status=403, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80) #run app in debug mode on port 80
