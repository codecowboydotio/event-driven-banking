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
![End to End Architecture](/Architecture.png)




### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/codecowboydotio/event-driven-banking/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
