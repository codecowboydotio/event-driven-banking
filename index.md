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

```
curl https://api.up.com.au/api/v1/webhooks \
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



### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/codecowboydotio/event-driven-banking/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

