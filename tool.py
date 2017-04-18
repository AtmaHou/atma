import string

def num_there(s):
    return any(i.isdigit() for i in s)

	
def keep_bound(value, bound):
    return min(max(value, bound[0]), bound[1])


def convert_to_word_lst(sentence, lower=True):
    sentence = filter(lambda x: x in string.printable, sentence)
    exclude = '''!"#$%&\'()*+,:;<=>?@[\\]^_`{|}~-/\t''' + '\n'
    for e in exclude:
        sentence = sentence.replace(e, ' ')
    if lower:
        sentence = sentence.lower()
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


def wrap_star_digger(item, type_str, data_name='Value'):
    """
    code used to extract data from Bing's wrap star
    :param item: wrap star obj
    :param type_str: target type string
    :param data_name: target data label, might be "Entities", "Properties", 'Value'
    :return: list of all matched target, arranged in occurance
    """
    ret = []
    if type(item) == dict:
        if 'Type' in item and item['Type'] == type_str and data_name in item:  # 'Business.Consumer_Product.Description'
            if len(item[data_name]) > 1:
                # print 'length error!!!!!!!!!!!'
                pass
            return item[data_name]
        else:
            for k in item:
                sub_ret = wrap_star_digger(item[k], type_str, data_name)
                if sub_ret:
                    ret.extend(sub_ret)
    elif type(item) == list:
        for i in item:
            sub_ret = wrap_star_digger(i, type_str, data_name)
            if sub_ret:
                ret.extend(sub_ret)
    return ret
