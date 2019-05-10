import gc
import time
import sys
import functools

import numpy as np

import create_matrix as cm


_LOG_DIR = 'C:/Users/tsukuda/local/nlp_learning_for_python/recipe_nlp/procedure_3'
_POS_DIR = 'C:/Users/tsukuda/local/nlp_learning_for_python/recipe_nlp/procedure_2'
_RNE_DIR = 'C:/Users/tsukuda/local/nlp_learning_for_python/recipe_nlp/procedure_4_2'


# ---------------
# preprocessing
# ---------------
# TODO "combine separate functions into one"
def separate_sentence(word_list):
    sentence_array = []
    current_array = []
    for word in word_list:
        # if word != '。' or word != '。\n':
        #     # print('not EOS')
        #     current_array.append(word)
        # else:
        #     # print('EOS')
        #     current_array.append('。')
        #     sentence_array.append(np.array(current_array))
        #     current_array = []
        #     continue
        # print('sentence_array')
        # print(sentence_array)
        if word == '。\n' or word == '）\n' or word == '-\n':
            # print('EOS')
            word = word.split('\n')[0]
            # print('word')
            # print(word)
            current_array.append(word)
            sentence_array.append(np.array(current_array))
            current_array = []
            continue
        else:
            # print('EOS')
            current_array.append(word)
        # print('sentence_array')
        # print(sentence_array)

    return np.array(sentence_array)


def separate_procedure(word_list):
    procedure_array = []
    current_array = []
    for word in word_list:
        # print('word')
        # print(word)
        if word == '。\n' or word == '）\n' or word == '-\n':
            # print('EOS')
            word = word.split('\n')[0]
            # print('word')
            # print(word)
            current_array.append(word)
            procedure_array.append(np.array(current_array))
            current_array = []
            continue
        else:
            # print('not EOS')
            current_array.append(word)
        # print('procedure_array')
        # print(procedure_array)

    return np.array(procedure_array)


def separate_postext(word_list):
    pos_array = []
    current_array = []
    for word in word_list:
        print('word')
        print(word)
        if word == '\n':  # line is empty
            pass
        else:
            target_word = word.split('/')[2]
            # print('word')
            # print(word)
            # print('target_word')
            # print(target_word)

            if target_word == '。\n' or target_word == '）\n' or target_word == '-\n':
                # print('EOS')
                target_word = target_word.split('\n')[0]
                current_array.append(word)
                pos_array.append(np.array(current_array))
                current_array = []
                continue
            else:
                # print('not EOS')
                current_array.append(word)
            # print('pos_array')
            # print(pos_array)

    return pos_array


def separate_rnetext(word_list):
    rne_array = []
    current_array = []
    for word in word_list:
        if word.count('/') >= 2:
            target_word = '/'
        else:
            target_word = word.split('/')[0]
            # print('word')
            # print(word)
            # print('target_word')
            # print(target_word)
            if target_word == '。' or target_word == '。\n':
                # print('EOS')
                current_array.append(word)
                rne_array.append(np.array(current_array))
                current_array = []
                continue
            else:
                # print('not EOS')
                current_array.append(word)
            # print('rne_array')
            # print(rne_array)

    return rne_array


# -------------------
# feature extraction
# -------------------
def include_particle_or_not(target_words, between_words,
                            feature, target1, target2, id1, id2):
    if type(target_words) is list:  # agent
        if target_words[0] in between_words or target_words[1] in between_words\
          or target1 == target_words[0] or target1 == target_words[1]\
          or target2 == target_words[0] or target2 == target_words[1]:
            feature[id1][id2] = 1
            feature[id2][id1] = 1
            return True
        else:
            return False
    elif type(target_words) is str:  # target, dest, comp
        if target_words in between_words\
          or target1 == target_words or target2 == target_words:
            feature[id1][id2] = 1
            feature[id2][id1] = 1
            return True
        else:
            return False
    else:
        print('something wrong!')


def is_exist_word(vocab_size, array_id):
    feature = np.zeros((vocab_size, vocab_size), dtype=np.int32)
    for i in array_id:
        for j in i:
            for k in i:
                feature[j][k] = 1

    return feature


def is_exist_particle(vocab_size, array_id, pos_array, pos_name):

    def debug_print(count, idx1, idx2, id1, id2, pos1, pos2,
                    between_words, include_or_not):
        print('count', count)
        print('idx1', idx1)
        print('idx2', idx2)
        print('id1', id1)
        print('id2', id2)
        print('pos1', pos1)
        print('pos2', pos2)
        print('pos')
        print(pos)
        print('between_words')
        print(between_words)
        print('include or not')
        print(include_or_not)
        time.sleep(1)

        return

    pos_map = {
        'agent': ['は/助詞/は', 'が/助詞/が'],
        'target': 'を/助詞/を',
        'dest': 'に/助詞/に',
        'comp': 'で/助詞/で',
    }
    pos_words = pos_map[pos_name]

    feature = np.zeros((vocab_size, vocab_size), dtype=np.int32)
    print('pos_array')
    print(pos_array)
    for ids, pos in zip(array_id, pos_array):
        count = 0
        for idx1, (id1, pos1) in enumerate(zip(ids, pos)):
            for idx2, (id2, pos2) in enumerate(zip(ids, pos)):
                if count > idx2:
                    # print('!!!!!!!!!!!!!!!! pass !!!!!!!!!!!!!!!!')
                    pass
                else:
                    between_words = pos[idx1:idx2]
                    include_or_not = include_particle_or_not(
                        pos_words, between_words, feature, pos1, pos2, id1, id2
                    )
                    # debug_print(
                    #     count, idx1, idx2, id1, id2, pos1, pos2,
                    #     pos_words, between_words, include_or_not
                    # )
            count += 1

    return feature


def is_exist_action(vocab_size, array_id, rne_array):
    # TODO 'if rne_word > 2' 2019/5/10 tsukuda

    def debug_print(count, idx1, idx2, id1, id2,
                    rne1, rne2, between_words, include_or_not):
        print('count', count)
        print('idx1', idx1)
        print('idx2', idx2)
        print('id1', id1)
        print('id2', id2)
        print('rne1', rne1)
        print('rne2', rne2)
        print('between_words')
        print(between_words)
        print('include or not')
        print(include_or_not)
        time.sleep(1)

        return

    feature = np.zeros((vocab_size, vocab_size), dtype=np.int32)
    rne_words = ['Ac-B', 'Ac-B']
    print('rne_array')
    print(rne_array)
    for ids, rne in zip(array_id, rne_array):
        count = 0
        tag = [w.split('/')[1] if w.count('/') <= 2 else 'O' for w in rne]
        for idx1, (id1, rne1) in enumerate(zip(ids, rne)):
            for idx2, (id2, rne2) in enumerate(zip(ids, rne)):
                if count > idx2:
                    # print('!!!!!!!!!!!!!!!! pass !!!!!!!!!!!!!!!!')
                    pass
                else:
                    if rne1.count('/') >= 2 and rne2.count('/') >= 2:
                        tag1 = rne1.split('/')[2]
                        tag2 = rne2.split('/')[2]
                    elif rne1.count('/') == 1 and rne2.count('/') == 1:
                        tag1 = rne1.split('/')[1]
                        tag2 = rne2.split('/')[1]
                    else:
                        print('something wrong!')
                        print('rne1', rne1)
                        print('rne2', rne2)
                        print('tag1', tag1)
                        print('tag2', tag2)
                        sys.exit(1)
                    between_words = tag[idx1:idx2]
                    include_or_not = include_particle_or_not(
                        rne_words, between_words,
                        feature, tag1, tag2, id1, id2
                    )
                    # debug_print(
                    #     count, idx1, idx2, id1, id2,
                    #     tag1, tag2, between_words, include_or_not
                    # )
            count += 1

    return feature


def trigram(vocab_size, corpus=None, window_size=1):
    corpus_size = len(corpus)
    co_matrix = np.zeros((vocab_size, vocab_size), dtype=np.int32)
    for idx, word_id in enumerate(corpus):
        for i in range(1, window_size + 1):
            left_idx = idx - i
            right_idx = idx + i

            if left_idx >= 0:
                left_word_id = corpus[left_idx]
                current_idx = corpus[idx]
                co_matrix[word_id, left_word_id] = 1
                co_matrix[word_id, current_idx] = 1
            if right_idx < corpus_size:
                right_word_id = corpus[right_idx]
                current_idx = corpus[idx]
                co_matrix[word_id, right_word_id] = 1
                co_matrix[word_id, current_idx] = 1

    return co_matrix


def feature_by_sentence(vocab_size, word_to_id, data_dir):
    '''
    # ---------------------------
    # feature separate sentence
    # ---------------------------
    # separate by sentence
    '''
    print('################ sentence ################')
    word_list = cm.generate_wordlist(data_dir)
    sentence_array = separate_sentence(word_list)
    sentence_array_id = np.array(
        [np.array([word_to_id[w] for w in l]) for l in sentence_array]
    )

    feature = is_exist_word(
        vocab_size,
        sentence_array_id,
    )
    del sentence_array, sentence_array_id, word_list
    gc.collect()

    return feature


def feature_by_procedure(vocab_size, word_to_id, data_dir):
    '''
    # ----------------------------
    # feature separate precedure
    # ----------------------------
    '''
    print('################ procedure ################')
    word_list = cm.generate_wordlist_no_split(data_dir)
    procedure_array = separate_procedure(word_list)
    procedure_array_id = np.array(
        [np.array([word_to_id[w] for w in l]) for l in procedure_array]
    )
    # print(word_list)
    # print(procedure_array)

    feature = is_exist_word(
        vocab_size,
        procedure_array_id,
    )
    del word_list, procedure_array, procedure_array_id
    gc.collect()

    return feature


def feature_by_trigram(vocab_size, corpus=None):
    '''
    # -----------------
    # feature trigram
    # -----------------
    '''
    print('################ trigram ################')
    feature = trigram(vocab_size, corpus)

    return feature


def feature_by_pos(vocab_size, word_to_id=None, data_dir=None, pos_dir=None, pos_name=None):

    def debug_print(word_list, pos_word_list, words_array, pos_array,
                    word_to_id, pos_array_id, pos_name, feature):
        print('word_list')
        print(word_list)
        print('pos_word_list')
        print(pos_word_list)

        print('words_array')
        print(words_array)
        print('pos_array')
        print(pos_array)
        print('word_to_id')
        print(word_to_id)

        print('pos_array_id')
        print(pos_array_id)

        print('!!!!!!!!!!!!!!!! pos_name !!!!!!!!!!!!!!!!')
        print(pos_name)
        time.sleep(3)

        print('feature')
        print(feature)
        print(feature.shape)

        return

    word_list = cm.generate_wordlist_no_split(data_dir)
    pos_word_list = cm.generate_wordlist_no_split(pos_dir)

    words_array = separate_sentence(word_list)
    pos_array = separate_postext(pos_word_list)

    pos_array_id = np.array(
        [np.array([word_to_id[w] for w in l]) for l in words_array]
    )

    feature = is_exist_particle(vocab_size, pos_array_id, pos_array, pos_name)
    # debug_print(
    #     word_list, pos_word_list, words_array, pos_array,
    #     word_to_id, pos_array_id, pos_name, feature,
    # )

    return feature


def feature_by_rnetag():

    return


def feature_by_action(vocab_size, word_to_id=None, data_dir=None, rne_dir=None):
    word_list = cm.generate_wordlist_no_split(data_dir)
    rne_word_list = cm.generate_wordlist_no_split(rne_dir)
    print('word_list')
    print(word_list)
    print('rne_word_list')
    print(rne_word_list)

    words_array = separate_sentence(word_list)
    rne_array = separate_rnetext(rne_word_list)
    print('words_array')
    print(words_array)
    print('rne_array')
    print(rne_array)
    rne_array_id = np.array(
        [np.array([word_to_id[w] for w in l]) for l in words_array]
    )

    feature = is_exist_action(vocab_size, rne_array_id, rne_array)

    return feature


def get_feature_fn(feature_name, **kwargs):
    feature_funcmap = {
        'trigram': feature_by_trigram,
        'sentence': feature_by_sentence,
        'procedure': feature_by_procedure,
        'agent': feature_by_pos,
        'target': feature_by_pos,
        'dest': feature_by_pos,
        'comp': feature_by_pos,
        'action': feature_by_action,
    }

    if feature_name not in feature_funcmap:
        raise ValueError('Name of feature_name unknown {}'.format(feature_name))

    func = feature_funcmap[feature_name]
    @functools.wraps(func)
    def feature_fn(*args, **kwargs):
        return func(*args, **kwargs)

    return feature_fn


def extract_feature(feature_name, data_dir=None, pos_dir=None, rne_dir=None):
    '''
    -----
    Input
    -----
    feature_name:
        'trigram': feature_by_trigram(vocab_size, corpus),
        'sentence': feature_by_sentence(vocab_size, word_to_id, data_dir),
        'procedure': feature_by_procedure(vocab_size, word_to_id, data_dir),
        'agent': feature_by_pos(vocab_size, word_to_id, data_dir, pos_dir, 'agent'),
        'target': feature_by_pos(vocab_size, word_to_id, data_dir, pos_dir, 'target'),
        'dest': feature_by_pos(vocab_size, word_to_id, data_dir, pos_dir, 'dest'),
        'comp': feature_by_pos(vocab_size, wor:d_to_id, data_dir, pos_dir, 'comp'),
        'action': feature_by_action(vocab_size, word_to_id, data_dir, rne_dir),
    data_dir:
        filepath which include result of Morphological analysis
    pos_dir:
        filepath which include text that split words
        rne_dir:
        filepath which include result of RNE analysis
    ------
    Output
    ------
    One-hot Vector: nd.array((vocab_size, vocab_size))
    '''
    word_list = cm.generate_wordlist(data_dir)
    word_to_id, id_to_word = cm.generate_word_id_map(word_list)
    corpus = np.array([word_to_id[w] for w in word_list])
    vocab_size = len(id_to_word)

    print('feature_name')
    print(feature_name)

    feature_fn = get_feature_fn(feature_name)

    if feature_name == 'trigram':
        feature = feature_fn(vocab_size, corpus)
    elif feature_name == 'sentence' or feature_name == 'procedure':
        feature = feature_fn(vocab_size, word_to_id, data_dir)
    elif feature_name == 'action':
        feature = feature_fn(vocab_size, word_to_id, data_dir, rne_dir)
    else:
        feature = feature_fn(vocab_size, word_to_id, data_dir, pos_dir, feature_name)

    return feature


def main():
    data_dir = _LOG_DIR
    pos_dir = _POS_DIR
    rne_dir = _RNE_DIR
    feature = extract_feature('action', data_dir, pos_dir, rne_dir)

    print('feature')
    print(feature)


if __name__ == '__main__':
    main()
