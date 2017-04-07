#-*- coding:utf-8 -*-

from __future__ import division
import math
from fractions import Fraction
from collections import Counter
from nltk.util import ngrams


def BP(candidate, references):
    """
    calculate brevity penalty
    """
    c = len(candidate)
    ref_lens = (len(reference) for reference in references)
    r = min(ref_lens, key=lambda ref_len: (abs(ref_len - c), ref_len))

    if c > r:
        return 1
    else:
        return math.exp(1 - r / c)


def MP(candidate, references, n):
    """
    calculate modified precision
    """
    counts = Counter(ngrams(candidate, n))
    if not counts:
        return 0

    max_counts = {}
    for reference in references:
        reference_counts = Counter(ngrams(reference, n))
        for ngram in counts:
            max_counts[ngram] = max(max_counts.get(ngram, 0), reference_counts[ngram])

    clipped_counts = dict((ngram, min(count, max_counts[ngram])) for ngram, count in counts.items())

    return sum(clipped_counts.values()) / sum(counts.values())


def bleu(candidate, references, weights):
    """
    Calculate BLEU for a single sentence, comment by atma
    The result of this code is same as the most popular perl script
    eg:
        weight = [0.25, 0.25, 0.25, 0.25]
        can = 'It is a guide to action which ensures that the military always obeys the commands of the party'.lower().split()
        ref1 = 'It is a guide to action that ensures that the military will forever heed Party commands'.lower().split()
        ref2 = 'It is the guiding principle which guarantees the military forces always being under the command of the Party'.lower().split()
        ref = [ref1, ref2]
        print bleu(can, ref, weight)
    :param candidate: word list of one sentence, eg: ['I', 'like', 'eat', 'apple']
    :param references: list of ref, each is a list of word, eg [['I', 'like', 'eat', 'apple'],['I', 'like', 'apple']]
    :param weights: a list of weight
    :return: return the bleu score
    """
    p_ns = ( MP(candidate, references, i) for i, _ in enumerate(weights, start=1))
    s = []
    for w, p_n in zip(weights, p_ns):
        try:
            s.append(w * math.log(p_n))
        except ValueError:
            s.append(0)
    s = math.fsum(s)

    bp = BP(candidate, references)
    return bp * math.exp(s)


if __name__ == '__main__':
    weight = [0.25, 0.25, 0.25, 0.25]
    can = 'It is a guide to action which ensures that the military always obeys the commands of the party'.lower().split()
    ref1 = 'It is a guide to action that ensures that the military will forever heed Party commands'.lower().split()
    ref2 = 'It is the guiding principle which guarantees the military forces always being under the command of the Party'.lower().split()
    ref = [ref1, ref2]
    print bleu(can, ref, weight)
