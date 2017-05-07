# Author: Atma (Yutai Hou)
# Modified: 5/7/2017 8:29 PM

Introduction
Commonly used NLP tools, that verified & written by Atma Hou.


Content & Description
./bleu.py
Sentence level bleu score tool, used as a labeling tool.
The nltk's bleu tool can not get right results, so i wrote this.
Code is verified by comparing results to commonly used perl-BLEU tool. 

./tool.py
Contain many frequently used & verified small & dirty function, 
such as convert sentence to word list, judge number, remove punctuation...

./crawling/*
A proxy class & proxy check tool written by me & jinpeng.
I rewrite Jinpeng's code to enable the proxy to crawl ssl-website.
This proxy is proved to be stable.


./AcoraMatcher.py
A multi-keyword match tool base on the package acora.
It use index method to speed up the process. 
When you need to match a lot of pre-defined keyword in a long text, it 
will be a great help.