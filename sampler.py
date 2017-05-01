# coding: utf-8
import random
import json


def full_sample(tar_f=None, res_f=None, res_size=50, start_pos=0, end_pos=100):
    buff = []
    if tar_f:
        with open(tar_f, 'r') as reader:
            cnt = 0
            for line in reader:
                buff.append(json.dumps({'text': line, 'id': cnt}))
                if cnt > end_pos:
                    break
                cnt += 1
        target_field = buff[start_pos: end_pos]
        result_set = random.sample(target_field, res_size)

        if not res_f:
            res_f = '%d_sampled_%s_from_%d_to_%d' % (res_size, res_f, start_pos, end_pos)
        with open(res_f, 'w') as writer:
            writer.write('\n'.join(result_set))
    else:
        print 'ERROR: no target file'


if __name__ == '__main__':
    test_f = './template/title_template'
    full_sample(test_f, res_size=50, start_pos=0, end_pos=2000)
