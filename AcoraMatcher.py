# coding:utf-8
import cPickle
import json
import acora
from atma import tool
import collections
from itertools import groupby


class AcoraMatcher:
    def __init__(self, spec_set, min_count=1, min_len=1):
        key_lst = []
        if type(spec_set) == dict or type(spec_set) == collections.Counter:
            for spec, cnt in spec_set.items():
                if cnt >= min_count and len(spec) >= min_len:
                    key_lst.append(spec)
        elif type(spec_set) == list:
            key_lst = spec_set
        else:
            print 'ERROR: wrong value type:', type(spec_set)
            exit(-1)
        self.builder = acora.AcoraBuilder(key_lst)
        self.ac = self.builder.build()

    def match(self, des, whole_match=True):
        ret = []
        letters = set("!\"$%&'()*+,.:;<>?@[\]^_`{|}~ -")
        wrong_spec = ['other', 'no', 'A', 'none']
        for kw, pos in self.ac.findall(des):
            # print des[pos - 1] == ' '
            # print des[pos: pos + len(kw)]
            # print pos+len(kw) == len(des), len(des), pos, len(kw), des[pos + len(kw) - 1] in letters
            if kw in wrong_spec:
                continue
            if not whole_match:
                ret.append((kw, pos))
            # remove non whole match
            elif (pos == 0 or des[pos-1] in letters) and (pos+len(kw) == len(des) or des[pos+len(kw)] in letters):
                ret.append((kw, pos))
        return ret  # return value format: [(match_string, start_pos)], start_pos starts from 0

    @staticmethod
    def longest_match(matches):
        ret = []
        matches = sorted(matches, key=lambda (x, y): (y, len(x) * -1))
        last_end = 0
        for m in matches:
            if len(m[0]) + m[1] > last_end:
                ret.append(m)
                last_end = len(m[0]) + m[1]
        return ret

    @staticmethod
    def distribution_counter(count_dic, items):
        for i in items:
            key = i
            if key not in count_dic:
                count_dic[key] = 1
            else:
                count_dic[key] += 1
