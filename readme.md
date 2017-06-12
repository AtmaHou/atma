# Light NLP Tool: atma-0.4.1
Author: Atma (Yutai Hou) | Modified: 5/7/2017 8:29 PM

## Introduction
Commonly used NLP tools, which are verified and fast.  
Function included:  
bleu score, proxy crawler, tokenizer, massive keyword matcher and so on.


## Install
pip install atma

## Quick Start
- Calculate BLEU for a single sentence
    The result of this code is same as the most popular perl script  
    eg:  
        from atma.bleu import *  
        weight = [0.25, 0.25, 0.25, 0.25]  
        can = 'It is a guide to action which ensures that the military always obeys the commands of the party'.lower().split()  
        ref1 = 'It is a guide to action that ensures that the military will forever heed Party commands'.lower().split()  
        ref2 = 'It is the guiding principle which guarantees the military forces always being under the command of the Party'.lower().split()  
        ref = [ref1, ref2]  
        print bleu(can, ref, weight)  



## Content & Description
- ./bleu.py  
Sentence level bleu score tool, used as a labeling tool.  
The nltk's bleu tool can not get right results, so i wrote this.  
Code is verified by comparing results to commonly used perl-BLEU tool.   

- ./tool.py  
Contain many frequently used & verified small & dirty function,  
such as convert sentence to word list, judge number, remove punctuation...

- ./crawling/*  
A proxy class & proxy check tool written by me & jinpeng.  
I rewrite Jinpeng's code to enable the proxy to crawl ssl-website.  
This proxy is proved to be stable.


- ./AcoraMatcher.py  
A multi-keyword match tool base on the package acora.  
It use index method to speed up the process.  
When you need to match a lot of pre-defined keyword in a long text, it  
will be a great help.
