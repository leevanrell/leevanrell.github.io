---
layout: post
title:  "Reverse Engineering Convolutional Codes"
date:   2020-07-18 17:03:36 -0500
categories: InformationTheory
---

I've recently been reading through Daniel Estevez's blog because I wanted to learn more about reverse engineering signals. If your unfamiliar, Daniel Estevez is the code owner/maintainer/big boi of [gr-satellites](https://github.com/daniestevez/gr-satellites), a very popular OOT module for gnuradio that supports decoding 80+ satellites.

This eventually led me to find [cccrack](https://github.com/BatchDrake/cccrack) mentioned in a post where Daniel was trying to reverse engineer the convolutional encoder for the DSCS-III beacon. 

The tool itself is fairly limited in its capability however, I hope as it ages it develops to be more practical to use. Currently, it reads in symbols from a file and guesses its codes using the [ Marazin-Gautier-Burel](https://www.researchgate.net/publication/224093438_Dual_Code_Method_for_Blind_Identification_of_Convolutional_Encoder_for_Cognitive_Radio_Receiver_Design). I wish I could go into more depth on this algorithm but I'm very lacking in the linear algebra department but it definitely looks dope __af__ from my ignorant standpoint. Let's try it out and see how it works.


First let's make a encoder:

![Encoder diagram](/assets/img/re_convolutional_codes/encoder.png)

This is a diagram of a simple 1/2 convolutional encoder I stole from the internet. It has a code rate of 1/2 meaning that it takes in one bit and outputs two bits. The center boxes are a single bit registers that store a single bit and the circle with pluses represent xor operations. Here's the python code that implement's the encoder.

```python
import random 

nums = 10000
_in = [random.randint(0,1) for _ in range(nums)]
out = []

r1 = 0
r2 = 0
r3 = 0

for i in _in:
	o1 = i ^ r2 ^ r3
	o2 = i ^ r1 ^ r3
	out.append(o1)
	out.append(o2)
	r3 = r2
	r2 = r1
	r1 = i

with open('bits.txt', 'w') as f:
	f.write(''.join([str(o) for o in out]))

```

For the sake of simplicity and my cpu, we're going to keep the 'symbols' in a binary constellation however, cccrack does support complex modulation schemes up to 6 bits per symbol.

Now we build cccrack and see if it can figure out our encoder:

```bash
autoreconf -i
./configure
make
src/cccrack bits.txt
```

and this is cccrack's output:


![cccrack output](/assets/img/re_convolutional_codes/cccrack_output.png)

Here not only can see we that it accurately estimated the code rate, but it accurately describes the structure of the encoder.
I'm unsure of what the H[1] means but the G[1] represents the physical connections of the encoder for each output. Essentially it says the first output bit is xor'd with the input, the 2nd, and 3rd register, while the second output bit is xor'd with the input, 1st register, and 3rd register. A picture's worth a thousand words so here:

![cccrack diagram](/assets/img/re_convolutional_codes/cccrack_diagram.png)


I think this tool has a lot of potential and can be more useful than alternatives like gr-baz's autofec block if its given more dev time. The developer [mentions](https://batchdrake.github.io/sc2019/) that he would like to add this algorithm to SigDigger using the soft decision version algorithm, which I think would greatly enhance its usefulness in practical applications

If you're completely unaware of what convolutional encoding is or why its needed, tough.

Fin.
