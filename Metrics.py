# coding: utf-8
import os
from multiprocessing import Process, Queue, current_process, freeze_support, Manager
N_THREAD = 60

# config the source/result data's input/output dir
result_file_path = './prediction/'
top_bleu_path = './TopBleu/'
kendall_tau_path = './KendallTau/'
top_meteor_path = './TopMeteor/'
test_file_path = './test/test_full_5376'
nonfeature_file_path = './nonfeatureScore/testNonFeatureScore_5376'


bleu_list = []
id_list = []
word_count_list = []
attri_count_list = []
prediction_dict = {}
weighted_attri_list = []
meteor_score_list = []

contrast_dic = {}  # used to debug
eval_result_dict = {  # used to format output evaluation result
    'Bleu': [],
    'Kendall': [],
    'METEOR': []
}


def load_dataset_items(test_file, predict_file_lst, nonfeature_file):
    """
    This function is used to read 3 kinds of data into list, 3 kinds of data are stored in files given by parameter
    :param test_file: path string, the testing set used for SVm rank
    :param predict_file_lst: filename lst, all prediction file output by SVM rank
    :param nonfeature_file: path string, contain all the score data not used as feature (aligned with test_file)
    :return: None
    """
    print 'Reading baseline feature & bleu...'
    with open(test_file, 'r') as reader:
        for line in reader:
            items = line.split(' ')
            label = float(items[0])

            id_list.append(items[1])
            bleu_list.append(label)
            word_count_list.append(float(items[2].split(':')[1]))
            attri_count_list.append(float(items[10].split(':')[1]))

    print 'Reading svm rankscore...'
    global prediction_dict
    for predict_file in predict_file_lst:
        mark = predict_file.replace('predictions', '')
        prediction_dict[mark] = []
        with open(result_file_path + predict_file, 'r') as reader:
            for line in reader:
                rankscore = float(line)
                prediction_dict[mark].append(rankscore)

    print 'Reading NonFeature score...'
    with open(nonfeature_file, 'r') as reader:
        for line in reader:
            nonfeature_items = line.split()
            w_score = float(nonfeature_items[2].split(':')[1])
            m_score = float(nonfeature_items[3].split(':')[1])
            weighted_attri_list.append(w_score)
            meteor_score_list.append(m_score)


def all_same(lst):
    a = lst[0]
    for i in lst:
        if i != a:
            return False
    return True


def get_item_metric_pair(item_lst, metric_lst, id_lst):
    """
    align bleu and specific score in item_lst, reconstruct the data as (rank_score, bleu) pairs, query_dic.
    Detail:
        query dict is input parameter used by metrics: top-x-bleu, kendall-tau
        query dict is reconstructed dict type data container,
        query dict's key is qid and value is list type, whose elements are tuple eg: count of words, bleu score pairs
    :param item_lst: the score value lst that used to rank candidates
    :param metric_lst: the metric value aligned with item_lst
    :return: query_dic
    """
    query_dic = {}  # key is qid, value is list, whose elements are tuple eg: count of words, bleu score pairs
    for index in range(len(metric_lst)):
        current_id = id_lst[index]
        current_bleu = metric_lst[index]
        current_rank_score = item_lst[index]
        if current_id in query_dic:
            query_dic[current_id].append((current_rank_score, current_bleu))
        else:
            query_dic[current_id] = []
            query_dic[current_id].append((current_rank_score, current_bleu))
    return query_dic


def top_x_bleu(query_dic, mark, x=1):
    """
    Calculate the top x average bleu value predictions ranking by item, x default is set above
    :param query_dic: dict, key is qid, value is (item, bleu) tuple list, which will be ranked by 'item' as key
    :param mark:string, which indicates which method is evaluated, also used as output file name here.
    :param x:int, define top x
    :return:average bleu score
    """
    all_total = 0.0
    with open(top_bleu_path + mark, 'w') as writer:
        for k in query_dic:
            candidate_lst = query_dic[k]
            top_x = sorted(candidate_lst, key=lambda a: a[0], reverse=True)[:x]
            total = 0
            for t in top_x:
                total += t[1]
            ave_bleu = total / x
            writer.write('%s\tAverageBleu:%f\tTop%d:%s\n' % (k, ave_bleu, x, str(top_x)))

            all_total += ave_bleu
            if k in contrast_dic:
                contrast_dic[k].append(str(ave_bleu))
            else:
                contrast_dic[k] = []
                contrast_dic[k].append(str(ave_bleu))
    result_string = '%s\ttop%d_Bleu:\t%f' % (mark, x, all_total / len(query_dic))
    print result_string
    # eval_result_dict['Bleu'].append(result_string)
    return ['Bleu', result_string]


def calculate_lst_kendall(lst):
    lst_length = len(lst)
    if lst_length < 2:
        return 0.0
    concordant, discordant = 0, 0
    for i, item in enumerate(lst):
        for j in range(i + 1, lst_length):
            tmp = lst[j]
            if item == tmp:
                continue
            rank_higher = i < j
            score_higher = item > tmp
            if rank_higher == score_higher:
                concordant += 1
            else:
                discordant += 1
    return (concordant - discordant) / (lst_length * (lst_length - 1) / 2.0)


def kendall_tau(query_dic, mark):
    """
    Calculate kendall_tau metric result of a method
    :param query_dic: dict, key is qid, value is (item, bleu) tuple list, which will be ranked by 'item' as key
    :param mark: string, which indicates which method is evaluated, also used as output file name here.
    :return: average kendall score
    """
    total = 0.0
    with open(kendall_tau_path + mark, 'w') as writer:
        for k in query_dic:
            candidate_lst = query_dic[k]
            ordered_lst = sorted(candidate_lst, key=lambda a: a[0], reverse=True)
            rank_lst = [can[1] for can in ordered_lst]
            tau_value = calculate_lst_kendall(rank_lst)
            writer.write('%s %f\n' % (k, tau_value))
            total += tau_value
    result_string = '%s\tkendall_tau:\t%f' % (mark, total / len(query_dic))
    print result_string
    # eval_result_dict['Kendall'].append(result_string)
    return ['Kendall', result_string]


def top_x_meteor(query_dic, mark, x=1):
    """
    Calculate METEOR score of the top result
    :param query_dic: dict, key is qid, value is (item, meteor) tuple list, which will be ranked by 'item' as key
    :param mark: string, which indicates which method is evaluated, also used as output file name here.
    :param x: int, define top x
    :return: average meteor score
    """
    all_total = 0.0
    with open(top_meteor_path + mark, 'w') as writer:
        for k in query_dic:
            candidate_lst = query_dic[k]
            top_x = sorted(candidate_lst, key=lambda a: a[0], reverse=True)[:x]
            total = 0
            for t in top_x:
                total += t[1]
            ave_value = total / x
            writer.write('%s\tAverageBleu:%f\tTop%d:%s\n' % (k, ave_value, x, str(top_x)))

            all_total += ave_value

            # for debug below here
            if k in contrast_dic:
                contrast_dic[k].append(str(ave_value))
            else:
                contrast_dic[k] = []
                contrast_dic[k].append(str(ave_value))
    result_string = '%s\ttop%d_METEOR:\t%f' % (mark, x, all_total / len(query_dic))
    print result_string
    # eval_result_dict['METEOR'].append(result_string)
    return ['METEOR', result_string]


def output_eval_result():
    with open('./eval_result', 'w') as writer:
        for k in eval_result_dict:
            writer.write('\n=====  %s  ===\n' % k)
            for rs in eval_result_dict[k]:
                writer.write(rs + '\n')


def full_evaluation_thread(task_queue, done_queue):
    for parameter in iter(task_queue.get, 'STOP'):
        item_lst = parameter[0]
        bleu_lst = parameter[1]
        meteor_lst = parameter[2]
        dataset_mark = parameter[3]
        id_lst = parameter[4]
        ret = []
        item_bleu_pair_dic = get_item_metric_pair(item_lst=item_lst, metric_lst=bleu_lst, id_lst=id_lst)
        item_meteor_pair_dic = get_item_metric_pair(item_lst=item_lst, metric_lst=meteor_lst, id_lst=id_lst)
        ret.append(top_x_bleu(item_bleu_pair_dic, dataset_mark))
        ret.append(kendall_tau(item_bleu_pair_dic, dataset_mark))
        ret.append(top_x_meteor(item_meteor_pair_dic, dataset_mark))

        done_queue.put(ret)


def full_evaluation():
    task_queue, done_queue, task_n = Queue(), Queue(), 0
    # LTR
    for f_name in file_lst:
        dataset_mark = f_name.replace('predictions', '')
        task_queue.put([prediction_dict[dataset_mark], bleu_list, meteor_score_list, dataset_mark, id_list])
        task_n += 1
    # baseline: count of word
    task_queue.put([word_count_list, bleu_list, meteor_score_list, 'WordCount', id_list])
    task_n += 1
    # baseline: count of attri
    task_queue.put([attri_count_list, bleu_list, meteor_score_list, 'AttriCount', id_list])
    task_n += 1
    # baseline: weight attri
    task_queue.put([weighted_attri_list, bleu_list, meteor_score_list, 'WeightAttri', id_list])
    task_n += 1
    # gold line: top bleu
    task_queue.put([bleu_list, bleu_list, meteor_score_list, 'Cheating', id_list])
    task_n += 1
    print "Start multi-thread Processing"
    for t in range(N_THREAD):
        task_queue.put('STOP')
    for t in range(N_THREAD):
        Process(target=full_evaluation_thread, args=(task_queue, done_queue)).start()
    # collect the results below
    for t in range(task_n):
        thread_return = done_queue.get()
        for eva in thread_return:
            eval_result_dict[eva[0]].append(eva[1])
        # print thread_return


if __name__ == '__main__':
    file_lst = os.listdir(result_file_path)
    load_dataset_items(test_file=test_file_path, predict_file_lst=file_lst, nonfeature_file=nonfeature_file_path)
    full_evaluation()
    # baseline: average bleu
    ave_bleu_blue_pair_dic = get_item_metric_pair(item_lst=bleu_list, metric_lst=bleu_list, id_lst=id_list)
    top_x_bleu(ave_bleu_blue_pair_dic, 'Ave-Bleu', x=100)

    # # LTR results
    # file_lst = os.listdir(result_file_path)
    # for f_name in file_lst:
    #     dataset_mark = f_name.replace('predictions', '')
    #     rankscore_bleu_pair_dic = get_item_metric_pair(item_lst=prediction_dict[dataset_mark], metric_lst=bleu_list)
    #     rankscore_meteor_pair_dic = get_item_metric_pair(item_lst=prediction_dict[dataset_mark],
    #                                                       metric_lst=meteor_score_list)
    #     top_x_bleu(rankscore_bleu_pair_dic, 'LTR' + dataset_mark)
    #     kendall_tau(rankscore_bleu_pair_dic, 'LTR' + dataset_mark)
    #     top_x_meteor(rankscore_meteor_pair_dic, 'LTR' + dataset_mark)
    #
    # # baseline: count of word
    # word_count_bleu_pair_dic = get_item_metric_pair(item_lst=word_count_list, metric_lst=bleu_list)
    # word_count_meteor_pair_dic = get_item_metric_pair(item_lst=word_count_list, metric_lst=meteor_score_list)
    # top_x_bleu(word_count_bleu_pair_dic, 'WordCount')
    # kendall_tau(word_count_bleu_pair_dic, 'WordCount')
    # top_x_meteor(word_count_meteor_pair_dic, 'WordCount')
    #
    # # baseline: count of attri
    # attri_count_bleu_pair_dic = get_item_metric_pair(item_lst=attri_count_list, metric_lst=bleu_list)
    # attri_count_meteor_pair_dic = get_item_metric_pair(item_lst=attri_count_list, metric_lst=meteor_score_list)
    # top_x_bleu(attri_count_bleu_pair_dic, 'AttriCount')
    # kendall_tau(attri_count_bleu_pair_dic, 'AttriCount')
    # top_x_meteor(attri_count_meteor_pair_dic, 'AttriCount')
    #
    # # baseline: weight attri
    # weight_attri_bleu_pair_dic = get_item_metric_pair(item_lst=weighted_attri_list, metric_lst=bleu_list)
    # weight_attri_meteor_pair_dic = get_item_metric_pair(item_lst=weighted_attri_list, metric_lst=meteor_score_list)
    # top_x_bleu(weight_attri_bleu_pair_dic, 'WeightAttri')
    # kendall_tau(weight_attri_bleu_pair_dic, 'WeightAttri')
    # top_x_meteor(weight_attri_meteor_pair_dic, 'WeightAttri')
    #
    # # gold line: top bleu
    # top_bleu_bleu_pair_dic = get_item_metric_pair(item_lst=bleu_list, metric_lst=bleu_list)
    # top_bleu_meteor_pair_dic = get_item_metric_pair(item_lst=bleu_list, metric_lst=meteor_score_list)
    # top_x_bleu(top_bleu_bleu_pair_dic, 'Cheating', x=1)
    # kendall_tau(top_bleu_bleu_pair_dic, 'Cheating')
    # top_x_meteor(top_bleu_meteor_pair_dic, 'Cheating')

    output_eval_result()
