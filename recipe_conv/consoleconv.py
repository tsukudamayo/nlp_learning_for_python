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

_COOK_WARE = ['オーブントースター', 'オーブン', 'トースター', 'フライパン', 'グリル', '電子レンジ']
_UNIT = ['cm', '分', '%', '等', 'w']


def text_to_strings(filename: str) -> str:
    read_file = open(filename, 'r', encoding='utf-8')
    strings = read_file.read()
    read_file.close()

    return strings


def convert_num_to_param(strings_array: str) -> dict:
    numparam_dict = {}
    number_flag = False
    count = 1
    for word in strings_array:
        # print(word, word.isdecimal())
        if word.isdecimal() is True and number_flag is False:
            # print('True:False')
            number_flag = True
            tmp_word = word
        elif word.isdecimal() is True and number_flag is True:
            # print('True:True')
            tmp_word = tmp_word + word
        elif word.isdecimal() is False and number_flag is True:
            # print('False:True')
            numparam_dict.update({'quantity' + str(count): tmp_word})
            tmp_word = word
            count += 1
            number_flag = False
        elif word.isdecimal() is False and number_flag is False:
            # print('False:False')
            tmp_word = word

    return numparam_dict


def convert_tool_to_param(strings_array: str) -> dict:
    tool_list = _COOK_WARE
    tool_param_dict = {}
    count = 1
    for tool in tool_list:
        if strings_array.find(tool) >= 0:
            current_param = 'tool' + str(count)
            converted_strings = strings_array.replace(tool, current_param)
            tool_param_dict.update({current_param: tool})
            strings_array = converted_strings
            count += 1
        else:
            pass

    return tool_param_dict


def convert_unit_to_param(strings_array: str, numparam_dict: dict) -> dict:
    unit_list = _UNIT
    unit_param_dict = {}
    split_array = strings_array.split(' ')
    unit_flag = False
    concat_flag = False
    tmp_word = ''
    count = 1
    for word in split_array:
        if unit_flag is True and word in unit_list:
            if word == '分' and concat_flag is True:
                concat_word = tmp_word + word
                unit_param_dict.update({'unit' + str(count): concat_word})
                concat_flag = False
                unit_flag = False
                count += 1

            elif word == '等':
                tmp_word = word
                concat_flag = True

            else:
                unit_param_dict.update({'unit' + str(count): word})
                unit_flag = False
                count += 1
        elif unit_flag is True and word not in unit_list:
            unit_flag = False
        else:
            pass

        if word in numparam_dict.values():
            unit_flag = True
        else:
            pass

    return unit_param_dict


def convert_recipe_parameter(wakachi_file: str,
                             ingredient_param_dict: dict,
                             num_param_dict: dict,
                             unit_param_dict: dict,
                             tool_param_dict: dict) -> str:
    inv_ingredient_param = {v: k for k, v in ingredient_param_dict.items()}
    inv_num_param = {v: k for k, v in num_param_dict.items()}
    inv_unit_param = {v: k for k, v in unit_param_dict.items()}
    inv_tool_param = {v: k for k, v in tool_param_dict.items()}
    print('inv_ingredient_param')
    print(inv_ingredient_param)
    print('inv_num_param')
    print(inv_num_param)
    print('inv_unit_param')
    print(inv_unit_param)
    print('inv_tool_param')
    print(inv_tool_param)
    
    with open(wakachi_file, 'r', encoding='utf-8') as r:
        lines = r.readlines()

    # --------------------------
    # convert quantity and unit
    # --------------------------
    param_key_value = {}
    word_key_value = {}
    converted_num_unit = []
    count = 1
    for line in lines:
        line = line.split(' ')
        print(line)
        for word in line:
            # XXXXXXXXXXXXXXXXXXXXXXXXXXX #
            # TODO gather as one function #
            # XXXXXXXXXXXXXXXXXXXXXXXXXXX #
            if word in inv_num_param:
                param_num = 'param' + str(count)
                param_deco = '<param' + str(count) + '>'
                param_key_value.update({param_num: 'quantity'})
                word_key_value.update({param_num: word})
                word = param_deco
                count += 1
            elif word in inv_unit_param:
                param_num = 'param' + str(count)
                param_deco = '<param' + str(count) + '>'
                param_key_value.update({param_num: 'unit'})
                word_key_value.update({param_num: word})
                word = param_deco
                count += 1
            else:
                pass
            converted_num_unit.append(word)

    # print('converted_num_unit')
    # print(converted_num_unit)

    # -------------------
    # convert ingredient
    # -------------------
    strings_for_join = ''
    join_converted_num_unit = strings_for_join.join(converted_num_unit)
    # print(join_converted_num_unit)
    # XXXXXXXXXXXXXXXXXXXXXXXXXXX #
    # TODO gather as one function #
    # XXXXXXXXXXXXXXXXXXXXXXXXXXX #    
    for k in inv_ingredient_param.keys():
        print('k')
        print(k)
        print(count)
        param_num = 'param' + str(count)
        param_deco = '<param' + str(count) + '>'
        converted_ingredient = join_converted_num_unit.replace(k, param_deco)
        join_converted_num_unit = converted_ingredient
        param_key_value.update({param_num: 'ingredient'})
        word_key_value.update({param_num: k})
        count += 1

    # print('converted_ingredient')
    # print(converted_ingredient)

    # --------------------
    # convert ingredient
    # --------------------
    for k in inv_tool_param:
        print('k')
        print(k)
        print(count)
        param_num = 'param' + str(count)
        param_deco = '<param' + str(count) + '>'
        converted_tool = converted_ingredient.replace(k, param_deco)
        converted_ingredient = converted_tool
        param_key_value.update({param_num: 'tool'})
        word_key_value.update({param_num: k})
        count += 1

    print(converted_tool)

    # ----------------
    # print by color
    # ----------------
    aux_print_converted = converted_tool.replace('<', ' <')
    print_converted = aux_print_converted.replace('>', '> ')
    # print(print_converted)
    split_print_recipe = print_converted.split(' ')
    delete_space = [x for x in split_print_recipe if x]
    # print(delete_space)

    # print(param_key_value)
    # print()

    for param in delete_space:
        delete_lf = param.replace('\n', '')
        conv_param_aux = delete_lf.replace('<', '')
        param_value = conv_param_aux.replace('>', '')
        if param_value not in param_key_value.keys():
            print(delete_lf, end='')
            continue
        if param_key_value[param_value] == 'ingredient':
            print(Color.RED + delete_lf + Color.END, end='')
        elif param_key_value[param_value] == 'tool':
            print(Color.CYAN + delete_lf + Color.END, end='')
        elif param_key_value[param_value] == 'unit'\
          or param_key_value[param_value] == 'quantity':
            print(Color.GREEN + delete_lf + Color.END, end='')
        else:
            print(param, end='')

    print()
    for k, v in param_key_value.items():
        print(k, v)
    print()
    for k, v in word_key_value.items():
        print(k, v)
    print()

    return converted_tool


def main():
    # print(Color.GREEN + 'Green' + Color.END)
    # print(Color.RED + 'RED' + Color.RED)
    print()
    org_file = 'weekcook/org/weekcook_sample.txt'
    org_lines = text_to_strings(org_file)
    print('original text')
    print(org_lines)
    print()

    print()
    json_filepath = 'weekcook/ingredient_json/weekcook_sample.json'
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
        convert_food = org_lines.replace(k, 'param' + str(idx))
    print(convert_food)

    print('################ convert num to param ################')
    num_param_dict = convert_num_to_param(org_lines)
    print(num_param_dict)

    print('################ convert tool to param ################')
    tool_param_dict = convert_tool_to_param(org_lines)
    print(tool_param_dict)

    print('################ convert unit to param ################')
    wakachi_file = 'weekcook/procedure_3/weekcook_sample_proc3.txt'
    wakachi_string = text_to_strings(wakachi_file)
    unit_param_dict = convert_unit_to_param(wakachi_string, num_param_dict)
    print(unit_param_dict)

    print('################ convert ingredient to param ################')
    ingredient_param_dict = {'ingredient' + str(idx): v
                             for idx, v in enumerate(ingredient_dict.keys())
                             if v != '材料'}
    print(ingredient_param_dict)

    print('################ convert reciepe ################')
    converted_recipe = convert_recipe_parameter(
        wakachi_file,
        ingredient_param_dict,
        num_param_dict,
        unit_param_dict,
        tool_param_dict,
    )

    # converted_recipe = convert_recipe_parameter()

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
