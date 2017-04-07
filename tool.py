import string

def num_there(s):
    return any(i.isdigit() for i in s)


def convert_to_word_lst(sentence):
    sentence = filter(lambda x: x in string.printable, sentence)
    exclude = '''!"#$%&\'()*+,:;<=>?@[\\]^_`{|}~-/\t''' + '\n'
    for e in exclude:
        sentence = sentence.replace(e, ' ')
    # sentence = sentence.lower()
    word_sq = sentence.split(' ')
    ret = []
    for ind, w in enumerate(word_sq):
        if '.' in w:
            if num_there(w):
                try:  # detect whether there is a float number
                    float_word = float(w)
                    if w[len(w) - 1] == '.':
                        w.replace('.', '')
                    ret.append(w)
                except ValueError:
                    if w[len(w) - 1] == '.':
                        w.replace('.', '')
                    ret.append(w)
            else:
                ret.extend(w.split('.'))
        else:
            ret.append(w)
    return filter(lambda x: x.strip(), ret)