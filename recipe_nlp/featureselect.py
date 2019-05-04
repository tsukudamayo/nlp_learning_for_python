import os

import numpy as np

import create_matrix as cm


_LOG_DIR = 'C:/Users/USER/local/nlp_learning_for_python/recipe_nlp/procedure_3'

def separate_sentence(word_list):
    sentence_array = []
    current_array = []
    for word in word_list:
        if word != '。':
            print('not EOS')
            current_array.append(word)
        else:
            print('EOS')
            current_array.append(word)
            sentence_array.append(np.array(current_array))
            current_array = []
            continue
        print('sentence_array')
        print(sentence_array)

    return np.array(sentence_array)


def separate_procedure(word_list):
    procedure_array = []
    current_array = []
    for word in word_list:
        print('word')
        print(word)
        if word != '。\n':
            print('not EOS')
            current_array.append(word)
        else:
            print('EOS')
            word = word.split('\n')[0]
            print('word')
            print(word)
            current_array.append(word)
            procedure_array.append(np.array(current_array))
            current_array = []
            continue
        # print('procedure_array')
        # print(procedure_array)

    return np.array(procedure_array)


def is_exist_word(corpus, vocab_size, id_to_word, array_id):
    feature = np.zeros((vocab_size, vocab_size), dtype=np.int32)
    for i in array_id:
        for j in i:
            for k in i:
                feature[j][k] = 1

    return feature


def main():
    word_list = cm.generate_wordlist(_LOG_DIR)
    # print(word_list)
    word_to_id, id_to_word = cm.generate_word_id_map(word_list)
    print('word_to_id')
    print(word_to_id)
    print('id_to_word')
    print(id_to_word)
    corpus = np.array([word_to_id[w] for w in word_list])
    print('corpus')
    print(corpus)

    # ---------------------------
    # feature separate sentence
    # ---------------------------
    # separate by sentence
    print('word_list')
    print(word_list)
    sentence_array = separate_sentence(word_list)
    print('sentence_array')
    print(sentence_array)
    print(type(sentence_array))
    print(type(sentence_array[0]))

    sentence_array_id = np.array(
        [np.array([word_to_id[w] for w in l]) for l in sentence_array]
    )
    print('sentence_array_id')
    print(sentence_array_id)
    print(type(sentence_array_id))

    vocab_size = len(id_to_word)
    sentence_feature = is_exist_word(
        corpus,
        vocab_size,
        id_to_word,
        sentence_array_id,
    )
    print('sentence_feature')
    print(sentence_feature)

    # ----------------------------
    # feature separate precedure
    # ----------------------------
    word_list = cm.generate_wordlist_no_split(_LOG_DIR)
    print('word_list')
    print(word_list)
    procedure_array = separate_procedure(word_list)
    print('procedure_array')
    print(procedure_array)
    procedure_array_id = np.array(
        [np.array([word_to_id[w] for w in l]) for l in procedure_array]
    )
    print('precedure_array_id')
    print(procedure_array_id)

    procedure_feature = is_exist_word(
        corpus,
        vocab_size,
        id_to_word,
        procedure_array_id,
    )
    print('precedure_feature')
    print(procedure_feature)


if __name__ == '__main__':
    main()
