import json


class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'


_INGREDIENT_SAMPLE = ['アボカド', '塩鮭', '生クリーム', 'チーズ（ピザ用）', '塩', 'ブラックペッパー']
_INGREDIENT_00000038 = ['さんま', '塩']
_INGREDIENT_00000254 = ['筍', '人参', '椎茸', '卵', '水', '鶏がらスープの素',
                        '片栗粉', 'ラー油', '胡麻油', '酢', 'こしょう']
_INGREDIENT_00000257 = ['糸昆布', 'さつま揚げ', '人参', '絹さや', '★', '水', 'stillたれ']
_INGREDIENT_00001895 = ['ナス', 'かつお節', '生姜', 'しょう油']
_INGREDIENT_00001977 = ['太刀魚', '塩', 'セロリ', '実山椒', '酢', 'stillたれ']
_INGREDIENT_00002344 = ['ブロッコリー', 'トマト', 'セロリ', 'ツナ缶', 'マヨネーズ', '塩']
_INGREDIENT_00002816 = ['ブロッコリー', 'ミニトマト', 'マヨネーズ', '味噌']
_INGREDIENT_00003159 = ['新じゃがいも', '新玉ねぎ', 'ミニトマト', 'マヨネーズ', '胡椒', 'ドライパセリ']
_INGREDIENT_00003363 = ['椎茸', 'アンチョビ', 'にんにく', 'オリーブオイル', '鷹の爪', 'パセリ', '塩']


def main():
    # print(Color.GREEN + 'Green' + Color.END)
    # print(Color.RED + 'RED' + Color.RED)

    print()
    org_file = 'weekcook/org/weekcook_00000254.txt'
    org_f = open(org_file, 'r', encoding='utf-8')
    org_lines = org_f.read()
    org_f.close()
    print('original text')
    print(org_lines)
    print()

    print()
    json_filepath = 'weekcook/ingredient_json/weekcook_00000254.json'
    with open(json_filepath, 'r', encoding='utf-8') as j:
        ingredient_dict = json.load(j)

    print('ingredient_dict')
    print(ingredient_dict)
    print()

    print('################ convert by json ################')
    for idx, k in enumerate(ingredient_dict.keys()):
        if k == '材料':
            continue
        print(k)
        org_lines = org_lines.replace(k, 'param' + str(idx))
    print(org_lines)


    # sample_file = 'weekcook/ner_result/weekcook_00000083_ner_result.txt'

    # sample_f = open(sample_file, 'r', encoding='utf-8')
    # sample_lines = sample_f.read()
    # sample_f.close()
    # print('lines : ', sample_lines)
    # split_lines = sample_lines.split(' ')
    # print('split_lines : ', split_lines)

    # # ---------
    # # color
    # # ---------
    # for line in split_lines:
    #     if line.find('F') >= 0:
    #         print(Color.RED + line + Color.END, end='')
    #     elif line.find('T') >= 0:
    #         print(Color.CYAN + line + Color.END, end='')
    #     elif line.find('Sf') >= 0:
    #         print(Color.GREEN + line + Color.END, end='')
    #     elif line.find('D') >= 0:
    #         print(Color.GREEN + line + Color.END, end='')
    #     elif line.find('焼') >= 0 and line.find('Ac') >= 0:
    #         print(Color.YELLOW + line + Color.END, end='')
    #     elif line.find('。') >= 0:
    #         print(line)
    #     else:
    #         print(line, end='')

    # # ------------------
    # # convert param tag
    # # ------------------
    # param_to_word = {}
    # word_to_param = {}
    # parameters = {}
    # count = 1
    # for line in split_lines:
    #     param_num = 'param' + str(count)
    #     # print('param_num')
    #     # print(param_num)
    #     line = line.replace('=', '')
    #     if line.find('F') >= 0:
    #         target = line.split('/')[0]
    #         if target in _INGREDIENT_00001977:
    #             if target not in word_to_param:
    #                 param_to_word.update({param_num: target})
    #                 word_to_param.update({target: param_num})
    #                 parameters.setdefault(param_num, {})
    #                 parameters[param_num].setdefault('val', target)
    #                 parameters[param_num].setdefault('type', 'ingredient')
    #                 count += 1
    #             else:
    #                 param_num = word_to_param[target]
    #             line = '<' + param_num + '>'
    #         else:
    #             pass
    #         print(Color.RED + line + Color.END, end='')

    #     elif line.find('T') >= 0 and line.find('cm') < 0:

    #         target = line.split('/')[0]
    #         if target.find('火') < 0:
    #             if target not in word_to_param:
    #                 param_to_word.update({param_num: target})
    #                 word_to_param.update({target: param_num})
    #                 parameters.setdefault(param_num, {})
    #                 parameters[param_num].setdefault('val', target)
    #                 parameters[param_num].setdefault('type', 'tool')
    #                 count += 1
    #             else:
    #                 param_num = word_to_param[target]

    #             line = '<' + param_num + '>'

    #         else:
    #             pass

    #         print(Color.CYAN + line + Color.END, end='')

    #     elif line.find('cm') >= 0:

    #         target = line.split('/')[0]
    #         if target not in word_to_param:
    #             param_to_word.update({param_num: target})
    #             word_to_param.update({target: param_num})
    #             parameters.setdefault(param_num, {})
    #             parameters[param_num].setdefault('val', target)
    #             parameters[param_num].setdefault('type', 'unit')
    #             count += 1
    #         else:
    #             param_num = word_to_param[target]

    #         line = '<' + param_num + '>'
    #         print(Color.GREEN + line + Color.END, end='')

    #     elif line.find('Sf') >= 0:

    #         target = line.split('/')[0]
    #         if target.isdigit() == True:
    #             if target not in word_to_param:
    #                 param_to_word.update({param_num: target})
    #                 word_to_param.update({target: param_num})
    #                 parameters.setdefault(param_num, {})
    #                 parameters[param_num].setdefault('val', target)
    #                 parameters[param_num].setdefault('type', 'quantity')
    #                 count += 1
    #             else:
    #                 param_num = word_to_param[target]

    #             line = '<' + param_num + '>'
    #             print(Color.GREEN + line + Color.END, end='')
    #         else:
    #             print(line, end='')

    #     elif line.find('D') >= 0:
    #         if line.find('約') >= 0:
    #             try:
    #                 target_num = line.split('/')[0]
    #                 target_max = int(target_num.split('約')[1])
    #                 target_min = int(float(target_max) * 0.7)
    #                 target_list = [target_min, target_max]
    #             except ValueError:
    #                 print(line, end='')
    #                 continue
    #         else:
    #             try:
    #                 target_num = line.split('/')[0]
    #                 target_max = int(target_num)
    #                 target_min = int(float(target_max) * 0.7)
    #                 target_list = [target_min, target_max]
    #             except ValueError:
    #                 print(line, end='')
    #                 continue

    #         for target in target_list:
    #             param_num = 'param' + str(count)
    #             if target not in word_to_param:
    #                 param_to_word.update({param_num: target})
    #                 word_to_param.update({target: param_num})
    #                 parameters.setdefault(param_num, {})
    #                 parameters[param_num].setdefault('val', target)
    #                 parameters[param_num].setdefault('type', 'quantity')
    #                 count += 1
    #             else:
    #                 param_num = word_to_param[target]

    #             line = '<' + param_num + '>'
    #             print(Color.GREEN + line + Color.END, end='')

    #     elif line.find('焼') >= 0 and line.find('Ac') >= 0:

    #         target = line.split('/')[0]
    #         # if target not in word_to_param:
    #         #     param_to_word.update({param_num: target})
    #         #     word_to_param.update({target: param_num})
    #         # else:
    #         #     param_num = word_to_param[target]
    #         # line = '<' + param_num + '>'

    #         print(Color.YELLOW + line + Color.END, end='')

    #         count += 1

    #     elif line.find('。') >= 0:
    #         print(line)
    #     else:
    #         print(line, end='')

    # # print('param_to_word', param_to_word)
    # # print('word_to_param', word_to_param)
    # print('################ word to param ################')
    # for k, v in param_to_word.items():
    #     print(k, v)
    # # for k, v in word_to_param.items():
    # #     print(k, v)

    # print('################ parameters ################')
    # for k, v in parameters.items():
    #     print(k, v)


if __name__ == '__main__':
    main()
