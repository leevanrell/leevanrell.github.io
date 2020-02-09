---
layout: post
title:  "Turning GPT-2 into Alex Jones"
date:   2020-01-24 20:02:32 -0600
categories: Python GPT-2
---

This post is me riding the coattails of the GPT-2 hype train. 
Now for those that don't know, GPT-2 is a machine learning model that is very effective at text generation. It can maintain context over a long period of text making it more 'human' than previous algorithms.

For those that are interested read [this](https://towardsdatascience.com/transformers-141e32e69591) article on transformers
and of course openai's [site](https://openai.com/blog/better-language-models/)

Now for the memes. To get GPT-2 talking like Alex Jones, we need text and a lot of it. Unfortunately, Alex Jones was largely purged from social media in 2019 so we'll have to get creative. First, [wikiquotes](https://en.wikiquote.org/wiki/Alex_Jones) was a decent starting point. I used python w/ requests and bs4 to scrape the data (your smart, do it yourself). 

I've looked for transcripts of the Alex Jones show to no avail. But what I did find was Alex Jones's archived [twitter](https://webrecorder.io/ola_norsk/twitter---alex-jones/list/twitter-profiles/b1/20180818015205/https://twitter.com/realalexjones) on webrecorder.io. Not sure what kind of wizardry those guys are running for this web app, but I couldn't get the HTML of his twitter feed for the life of me. So instead I just selected all text and wrote it to a file. Genius. There was some manual formatting I did to group them into tweets and then clean up the actual contents, but once that's done it was somewhat useable for my purposes.

Now that we've collected around 900 lines of the good stuff we can train a model. Here's the code I used (stolen from some medium post, probably):
```
#/usr/bin/python3
import gpt_2_simple as gpt2
import os

model_name = "124M"
# model is saved into current directory under /models/124M/
if not os.path.isdir(os.path.join("models", model_name)):
	gpt2.download_gpt2(model_name=model_name)   

file_name = "./src/alex_jones.txt"

sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              file_name,
              model_name=model_name,
			  run_name='run2',
              steps=1000,
			  save_every=50,
			  print_every=5,
			  sample_every=10,
			  learning_rate = 0.0001
)

gpt2.generate_to_file(sess)


```

I've let this train in my homelab for a few hours while I slept, and checked back when I thought it was ready.

Here are some of the results:

```

Organizer: Planned Parenthood Ships Guns To The US  View all other

Open book censorship represents a poison pill for the people and a soulless dollop of
propaganda for the corporate media. #FreeInfowars #1A

These people are the future. They're such zombies that you can  not only read the news,
but look at these people! They're so freaking fastidious they have time organs  in their 
knees that they can hardly walk! They have no awareness of what's going on  and go "OOH 
O_O O_O"O Oh my gosh! That's evil! The Alex Jones Show, "HILLARY CLINTON IS A GOD DAMN 
DEMON", June 2016.

I'm like a gigantic pumpkinhead, sitting in a  park, and I'm thinking "Man, this is gonna
be a really bad day.  It just so happens, is gonna be really bad. I'm thinking ABOUT 
WHATEVER  I'm thinking about today. Yeah, I'm thinking

A vocal minority of Trump hating registered voters has called off an election for fear of
repercussions from his supporters.     #Trump2020 #MAGA #1a #USA

Video: left wing extremists targeting DC political events with machetes this weekend  

The coordinated corporate attack on Infowars has exposed a deceptic by any measure, but
the silencing of the truth is even more apparent.

Now you need to find a way to stop the Chinese from harvesting our blood.

The Rise Of Alex Jones As A Fake News Crikey, Tune in M F 11am 3pm central at:   << 
#RealNews #WednesdayWisdom #1a #ThursdayMotivation   #FreeInfowars

```

These are just a few of the hundreds of little gems GPT-2 spat out for us. There were a few artifacts that I didn't like from the outputs; so in the alex_jones.txt, I went back and cleaned it up a bit more. The rest of the text files are relatively unmodified if you'd like to do the scrubbing yourself. Unlike GPT-2, all the code, output, and finetuning text I used can all be found [here](https://github.com/leevanrell/make-alex-great-again). Have fun. And don't let the globalists win.


