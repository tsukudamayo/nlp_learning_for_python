import json
import math
import operator
from typing import List


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


def compute_70per(number_str: str) -> int:
    compute_70per = int(math.floor(float(number_str) * 0.7))

    return compute_70per


def define_num_param_70percent(num_param_dict: dict) -> dict:
    num_param_70per_dict = {k: str(compute_70per(v))
                            for k, v in num_param_dict.items()}

    return num_param_70per_dict


def mapping_70per_to_100per(dict_100per: dict, dict_70per: dict) -> dict:
    relation_map = [{per100: per70} for per100, per70
                     in zip(dict_100per.values(), dict_70per.values())]

    return relation_map


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


def convert_cooking_time_strings(strings_array: str) -> List[str]:
    hhmmss_list = ['時間', '分', '秒']
    convert_strings = []
    for hhmmss in hhmmss_list:
        word_index = [hhmmss_index
                         for hhmmss_index, x in enumerate(strings_array) if x == hhmmss]
        for word in word_index:
            current_strings = ''
            for idx in reversed(range(word)):
                if strings_array[idx].isdecimal() or strings_array[idx] == '～':
                    current_strings += strings_array[idx]
                else:
                    if current_strings != '':
                        reverse_strings = current_strings[::-1]
                        result_strings = reverse_strings + hhmmss
                        convert_strings.append(result_strings)
                        break
                    else:
                        break

    return convert_strings


def convert_cooking_time_wakachi(wakachi_strings: str) -> List[str]:
    hhmmss_list = ['時間', '分', '秒']
    convert_strings = []

    split_lines = wakachi_strings.split(' ')
    print(split_lines)
    tmp_word = ''
    for word in split_lines:
        if word.isdecimal():
            tmp_word += word
        elif word.isdecimal() is False and word in hhmmss_list:
            tmp_word += word
            convert_strings.append(tmp_word)
            tmp_word = ''
        elif word.isdecimal() is False and word not in hhmmss_list:
            tmp_word = ''
        else:
            print('something wrong!')
            raise ValueError

    return convert_strings


def preordering_for_cooking_time_strings(strings_array: str,
                                convert_strings: List[str]) -> str:
    print(strings_array)
    insert_candidate = ['、', '。']
    for keyword in convert_strings:
        is_replace = False
        print(keyword)
        word_index = strings_array.index(keyword)
        print(word_index)
        keyword_delete = strings_array.replace(keyword, '')
        print(keyword_delete)
        preordering_strings = ''
        for word_idx in range(len(keyword_delete)):
            print(word_idx)
            if keyword_delete[word_idx] in insert_candidate\
              and word_idx >= word_index\
              and is_replace is False:
                # print('if')
                # print(word_idx)
                preordering_strings += keyword_delete[word_idx] + '(目安: 約' + str(keyword) + ')'
                is_replace = True
            else:
                # print('else')
                # print(word_idx)
                preordering_strings += keyword_delete[word_idx]
        strings_array = preordering_strings
    print(preordering_strings)

    return preordering_strings


def preordering_for_cooking_time_wakachi(wakachi_file: str,
                                         convert_strings: List[str]) -> List[str]:

    # TODO for wakachi file
    units = ['分', '秒', '時間', 'w']
    insert_candidate = ['、', '。']

    with open(wakachi_file, 'r', encoding='utf-8') as r:
        lines = r.readlines()

    split_lines_2d = [x.split(' ') for x in lines]
    split_lines = [y for x in split_lines_2d for y in x]
    print(split_lines)

    replace_template = '(目安: {} 約{})'
    preordering_strings = []
    convert_candidate = []
    tmp_word = ''
    replace_buffer = ''
    is_decimal = False
    is_replace = False
    for word in split_lines:
        if word.isdecimal() or word == '～':
            is_decimal = True
            tmp_word += word
        # --------------------- #
        # processing '、', '。' #
        # --------------------- #
        ##########################
        # TODO function -> class #
        ##########################
        elif word == '。\n' and is_replace is True:
            ############################
            # TODO -> funcition as one #
            ############################
            temperature_candidate = ''
            time_candidate = ''
            for candidate in convert_candidate:
                if candidate.find('w') >= 0:
                    temperature_candidate = candidate
                elif candidate.find('分') >= 0\
                  or candidate.find('秒') >= 0\
                  or candidate.find('時間') >= 0:
                    time_candidate = candidate
                else:
                    print('something wrong!')
                    raise ValueError
                
            replace_buffer = replace_template.format(
                temperature_candidate, time_candidate
            )
            format_replace_buffer = replace_buffer.replace('  ', ' ')
            print(format_replace_buffer)
            replace_word = '。' + format_replace_buffer + '\n'
            print(replace_word)
            preordering_strings.append(replace_word)
            replace_buffer = ''
            temperature_candidate = ''
            time_candidate = ''
            is_replace = False
        elif word == '。\n' and is_replace is False:
            preordering_strings.append(word)
        elif word == '。' and is_replace is True:
            ############################
            # TODO -> funcition as one #
            ############################
            temperature_candidate = ''
            time_candidate = ''
            for candidate in convert_candidate:
                if candidate.find('w') >= 0:
                    temperature_candidate = candidate
                elif candidate.find('分') >= 0\
                  or candidate.find('秒') >= 0\
                  or candidate.find('時間') >= 0:
                    time_candidate = candidate
                else:
                    print('something wrong!')
                    raise ValueError
                
            replace_buffer = replace_template.format(
                temperature_candidate, time_candidate
            )
            format_replace_buffer = replace_buffer.replace('  ', ' ')
            print(format_replace_buffer)
            replace_word = '。' + format_replace_buffer
            print(replace_word)
            preordering_strings.append(replace_word)
            replace_buffer = ''
            temperature_candidate = ''
            time_candidate = ''
            is_replace = False
        elif word == '。' and is_replace is False:
            preordering_strings.append(word)
        elif word == '、' and is_replace is True:
            ############################
            # TODO -> funcition as one #
            ############################
            temperature_candidate = ''
            time_candidate = ''
            for candidate in convert_candidate:
                if candidate.find('w') >= 0:
                    temperature_candidate = candidate
                elif candidate.find('分') >= 0\
                  or candidate.find('秒') >= 0\
                  or candidate.find('時間') >= 0:
                    time_candidate = candidate
                else:
                    print('something wrong!')
                    raise ValueError
                
            replace_buffer = replace_template.format(
                temperature_candidate, time_candidate
            )
            format_replace_buffer = replace_buffer.replace('  ', ' ')
            print(format_replace_buffer)
            replace_word = '、' + format_replace_buffer
            print(replace_word)
            preordering_strings.append(replace_word)
            replace_buffer = ''
            temperature_candidate = ''
            time_candidate = ''
            is_replace = False
            
        elif word == '、' and is_replace is False:
            replace_word = '、' + replace_buffer
            preordering_strings.append(replace_word)
            replace_buffer = ''
        # ---------------------------------- #
        # processing word about cooking time #
        # ---------------------------------- #
        elif word.isdecimal() is False and word in units and is_decimal:
            is_decimal = False
            tmp_word += word
            convert_candidate.append(tmp_word)
            is_replace = True
            tmp_word = ''
            print(is_replace)
        elif word.isdecimal() is False and word not in units and is_decimal:
            is_decimal = False
            preordering_strings.append(tmp_word)
            preordering_strings.append(word)
            tmp_word = ''
        elif word.isdecimal() is False and is_decimal is False:
            preordering_strings.append(word)
        # elif word.isdecimal() is False and word not in units and is_decimal is False:
        #     preordering_strings.append(word)
        else:
            print('something wrong!')
            print(word)
            raise ValueError

    print(preordering_strings)

    return preordering_strings


def sort_dict_by_values_length(org_dict: dict) -> dict:
    dict_len = {key: len(value) for key, value in org_dict.items()}
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_key_list)
    sorted_dict_by_values = [{item[0]: org_dict[item[0]]} for item in sorted_key_list]
    print(sorted_dict_by_values)
    
    return sorted_dict_by_values


def convert_recipe_parameter(preordering_wakachi_array: List[str],
                             ingredient_param_dict: dict,
                             num_param_dict: dict,
                             unit_param_dict: dict,
                             tool_param_dict: dict) -> str:

    def replace_word_to_param(strings_array: str, category: str) -> str:
        param_num = 'param' + str(count)
        param_deco = '<param' + str(count) + '>'
        param_key_value.update({param_num: category})
        word_key_value.update({param_num: strings_array})
        strings_array = param_deco

        return strings_array

    def replace_word_to_param_once(strings_array: str, category: str,
                                   target_string: str, count: int) -> str:
        param_num = 'param' + str(count)
        param_deco = '<param' + str(count) + '>'
        param_key_value.update({param_num: category})
        word_key_value.update({param_num: target_string})
        param_strings = strings_array.replace(target_string, param_deco, 1)

        return param_strings

    def replace_word_to_numrange_param(strings_array: str, category: str, count: int,
                                       relatetion_70per_100per: dict, number_of_replace: int) -> str:
        
        param_num = 'param' + str(count)
        param_deco = '<param' + str(count) + '>'
        param_key_value.update({param_num: category})
        word_key_value.update({param_num: list(relatetion_70per_100per[number_of_replace].values())[0]})
        strings_array = param_deco
        count += 1
        param_num = 'param' + str(count)
        param_deco = '<param' + str(count) + '>'
        param_key_value.update({param_num: category})
        word_key_value.update({param_num: list(relatetion_70per_100per[number_of_replace].keys())[0]})
        
        strings_array = strings_array + param_deco

        return strings_array

    print(ingredient_param_dict)
    print(num_param_dict)
    print(unit_param_dict)
    print(tool_param_dict)
    per70_param_dict = define_num_param_70percent(num_param_dict)
    relatetion_70per_100per = mapping_70per_to_100per(
        num_param_dict, per70_param_dict
    )
    print('per70')
    print(per70_param_dict)
    print('70-100')
    print(relatetion_70per_100per)
    # inv_ingredient_param = {v: k for k, v in ingredient_param_dict.items()}
    inv_num_param = {v: k for k, v in num_param_dict.items()}
    # inv_unit_param = {v: k for k, v in unit_param_dict.items()}
    inv_tool_param = {v: k for k, v in tool_param_dict.items()}
    # print('inv_ingredient_param')
    # print(inv_ingredient_param)
    # print('inv_num_param')
    # print(inv_num_param)
    # print('inv_unit_param')
    # print(inv_unit_param)
    # print('inv_tool_param')
    # print(inv_tool_param)

    # with open(wakachi_file, 'r', encoding='utf-8') as r:
    #     lines = r.readlines()
    lines = preordering_wakachi_array
    org_recipe = ''.join(lines)
    print('################ original recipe ################')
    print(org_recipe)

    # --------------------------
    # convert quantity and unit
    # --------------------------
    param_key_value = {}
    word_key_value = {}
    converted_num = []
    units = ['秒', '分', '時間']
    number_of_replace = 0
    count = 1
    for idx, line in enumerate(lines):
        # line = line.split(' ')
        # print(idx)
        # print(line)
        # print(len(lines))
        if idx <= (len(lines) - 1):
            if line in inv_num_param:
                # print('numparam')
                if lines[idx+1] in units:
                    print('if')
                    print('lines[idx+1]')
                    print(lines[idx+1])
                    line = replace_word_to_numrange_param(
                        line, 'quantity', count, relatetion_70per_100per, number_of_replace
                    )
                    count += 2
                elif idx == len(lines):
                    print('elif')
                    pass
                else:
                    print('else')
                    line = replace_word_to_param(line, 'quantity')
                    count += 1
                number_of_replace += 1
            # elif line in inv_unit_param:
            #     # print('unitparam')
            #     line = replace_word_to_param(line, 'unit')
            #     count += 1
            elif line.find('目安') >= 0 and line.find('～') >= 0:
                is_decimal = False
                # print(line)
                convert_line = ''
                tmp_word = ''
                for word in line:
                    # print(word)
                    if word.isdecimal():
                        # print('decimal')
                        tmp_word += word
                        continue
                    else:
                        if tmp_word != '':
                            if tmp_word in inv_num_param:
                                tmp_word = replace_word_to_param(tmp_word, 'quality')
                                convert_line += tmp_word
                                tmp_word = ''
                                count += 1
                                number_of_replace += 1
                            else:
                                print('something wrong!')
                                raise ValueError
                        else:
                            pass
                    # if word in inv_num_param:
                    #     # print('numparam')
                    #     word = replace_word_to_param(word, 'quantity')
                    #     convert_line += word
                    #     count += 1
                    # elif word in inv_unit_param:
                    #     # print('unitparam')
                    #     word = replace_word_to_param(word, 'unit')
                    #     convert_line += word
                    #     count += 1
                    # else:
                    convert_line += word
                line = convert_line
            elif line.find('目安') >= 0 and line.find('～') < 0:
                print('line')
                print(line)
                print('～ < 0:')
                is_decimal = False
                convert_line = ''
                tmp_word = ''
                for word in line:
                    # print('word')
                    # print(word)
                    # print('tmp_word')
                    # print(tmp_word)
                    if word.isdecimal():
                        # print('decimal')
                        # print(word)
                        tmp_word += word
                        continue
                    else:
                        if tmp_word != '':
                            # print("tmp_word != ''")
                            if tmp_word in inv_num_param:
                                tmp_word = replace_word_to_numrange_param(
                                    tmp_word, 'quantity', count, relatetion_70per_100per, number_of_replace
                                )
                                # print('replace_word_to_param')
                                # print(tmp_word)
                                convert_line += tmp_word
                                tmp_word = ''
                                count += 2
                                number_of_replace += 1
                            else:
                                print('something wrong!')
                                raise ValueError
                        else:
                            pass
                    convert_line += word
                line = convert_line
            else:
                pass
        else:
            pass
        converted_num.append(line)
    # # print('converted_num_unit')
    # # print(converted_num_unit)

    # -------------
    # convert unit
    # -------------
    join_converted_num = ''.join(converted_num)
    join_converted_num_unit = ''
    for k, v in unit_param_dict.items():
        join_converted_num_unit = replace_word_to_param_once(
            join_converted_num, 'unit', v, count,
        )
        join_converted_num = join_converted_num_unit
        count += 1
    print(join_converted_num_unit)

    # -------------------
    # convert ingredient
    # -------------------
    # XXXXXXXXXXXXXXXXXXXXXXXXXXX #
    # TODO gather as one function #
    # XXXXXXXXXXXXXXXXXXXXXXXXXXX #
    # for k in inv_ingredient_param.keys():
    for k in ingredient_param_dict.values():
        # print('k')
        # print(k)
        # print(count)
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

    if len(inv_tool_param) == 0:
        converted_tool = converted_ingredient
    else:
        pass

    # ----------------
    # print by color
    # ----------------
    aux_print_converted = converted_tool.replace('<', ' <')
    print_converted = aux_print_converted.replace('>', '> ')
    print(print_converted)
    split_print_recipe = print_converted.split(' ')
    delete_space = [x for x in split_print_recipe if x]
    print(delete_space)

    print('param_key_value')
    print(param_key_value)
    print()

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
    org_file = 'weekcook/org/weekcook_00000257.txt'
    org_lines = text_to_strings(org_file)
    print('original text')
    print(org_lines)
    print()

    print()
    json_filepath = 'weekcook/ingredient_json/weekcook_00000257.json'
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

    print('################ convert num to 70% ################')
    per70_param_dict = define_num_param_70percent(num_param_dict)
    print(per70_param_dict)

    print('################ convert tool to param ################')
    tool_param_dict = convert_tool_to_param(org_lines)
    print(tool_param_dict)

    print('################ convert unit to param ################')
    wakachi_file = 'weekcook/procedure_3/weekcook_00000257_proc3.txt'
    wakachi_string = text_to_strings(wakachi_file)
    unit_param_dict = convert_unit_to_param(wakachi_string, num_param_dict)
    print(unit_param_dict)

    print('################ convert ingredient to param ################')
    ingredient_param_dict = {'ingredient' + str(idx): v
                             for idx, v in enumerate(ingredient_dict.keys())
                             if v != '材料'}
    print(ingredient_param_dict)

    print('################ replace time words ################')
    convert_strings = convert_cooking_time_wakachi(wakachi_string)
    preordering_wakachi_array = preordering_for_cooking_time_wakachi(
        wakachi_file,
        convert_strings,
    )

    print('################ convert reciepe ################')
    converted_recipe = convert_recipe_parameter(
        preordering_wakachi_array,
        ingredient_param_dict,
        num_param_dict,
        unit_param_dict,
        tool_param_dict,
    )


if __name__ == '__main__':
    main()
