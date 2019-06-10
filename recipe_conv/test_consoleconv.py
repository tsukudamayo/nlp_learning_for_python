import os
import json

from consoleconv import text_to_strings
from consoleconv import convert_num_to_param
from consoleconv import convert_tool_to_param
from consoleconv import convert_unit_to_param
from consoleconv import convert_recipe_parameter
from consoleconv import define_num_param_70percent
from consoleconv import compute_70per
from consoleconv import mapping_70per_to_100per
from consoleconv import convert_cooking_time_strings
from consoleconv import convert_cooking_time_wakachi
from consoleconv import preordering_for_cooking_time_strings
from consoleconv import preordering_for_cooking_time_wakachi
from consoleconv import sort_dict_by_values_length


# def test_text_to_strings():
#     sample_file = 'weekcook/org/weekcook_sample.txt'
#     strings = text_to_strings(sample_file)
#     print(strings)
#     expected = '塩鮭は骨と皮を取り除き1cm厚さに斜め切りにし、ペーパータオルで包んで水気を取る。\nアボカドは半分に切りタネを除いて1cm幅に切る。\nスキレットを温めてサラダ油を塗り、塩鮭を軽く両面焼く。\n鮭が焼けたらアボカドを一緒に並べて生クリームを加え、塩とブラックペッパーを少々ふる。\n中火にかけて沸々してきたらチーズ（ピザ用）を乗せ、オーブントースターで8分焼いて焦げ目が付いたら完成。\n'

#     assert strings == expected


def test_convert_num_to_param_sample():
    sample_file = 'weekcook/org/weekcook_sample.txt'
    strings = text_to_strings(sample_file)
    numparam_dict = convert_num_to_param(strings)
    print(numparam_dict)
    expected = {
        'quantity1': '1',
        'quantity2': '1',
        'quantity3': '8',
    }

    assert numparam_dict == expected


def test_compute_70per_1():
    test_strings = '1'
    value_70per = compute_70per(test_strings)
    expected = int(0)

    assert value_70per == expected


def test_compute_70per_2():
    test_strings = '8'
    value_70per = compute_70per(test_strings)
    expected = int(5)

    assert value_70per == expected


def test_define_num_param_70percent():
    sample_file = 'weekcook/org/weekcook_sample.txt'
    strings = text_to_strings(sample_file)
    numparam_dict = convert_num_to_param(strings)
    num_param_70per_dict = define_num_param_70percent(numparam_dict)
    expected = {
        'quantity1': '0',
        'quantity2': '0',
        'quantity3': '5',
    }

    assert num_param_70per_dict == expected


def test_mapping_70per_to_100per():
    sample_file = 'weekcook/org/weekcook_sample.txt'
    strings = text_to_strings(sample_file)
    numparam_dict = convert_num_to_param(strings)
    num_param_70per_dict = define_num_param_70percent(numparam_dict)
    relatetion_70per_100per = mapping_70per_to_100per(
        numparam_dict, num_param_70per_dict
    )
    expected = [
        {'1': '0'},
        {'1': '0'},
        {'8': '5'},
    ]

    assert relatetion_70per_100per == expected


def test_convert_tool_to_param_sample():
    sample_file = 'weekcook/org/weekcook_sample.txt'
    strings = text_to_strings(sample_file)
    tool_param_dict = convert_tool_to_param(strings)
    print(tool_param_dict)
    expected = {
        'tool1': 'オーブントースター',
    }

    assert tool_param_dict == expected


def test_convert_tool_to_param_00000083():
    sample_file = 'weekcook/org/weekcook_00000083.txt'
    strings = text_to_strings(sample_file)
    tool_param_dict = convert_tool_to_param(strings)
    print(tool_param_dict)
    expected = {
        'tool1': 'フライパン',
        'tool2': 'グリル',
    }

    assert tool_param_dict == expected


def test_convert_tool_to_param_00001977():
    sample_file = 'weekcook/org/weekcook_00001977.txt'
    strings = text_to_strings(sample_file)
    tool_param_dict = convert_tool_to_param(strings)
    print(tool_param_dict)
    expected = {
        'tool1': 'フライパン',
        'tool2': 'グリル',
    }

    assert tool_param_dict == expected


def test_convert_tool_to_param_00003159():
    sample_file = 'weekcook/org/weekcook_00003159.txt'
    strings = text_to_strings(sample_file)
    tool_param_dict = convert_tool_to_param(strings)
    print(tool_param_dict)
    expected = {
        'tool1': '電子レンジ',
    }

    assert tool_param_dict == expected


def test_convert_unit_to_param_sample():
    sample_file = 'weekcook/org/weekcook_sample.txt'
    strings = text_to_strings(sample_file)
    numparam_dict = convert_num_to_param(strings)
    wakachi_file = 'weekcook/procedure_3/weekcook_sample_proc3.txt'
    wakachi_string = text_to_strings(wakachi_file)
    unit_param_dict = convert_unit_to_param(wakachi_string, numparam_dict)
    print(unit_param_dict)
    expected = {
        'unit1': 'cm',
        'unit2': 'cm',
        'unit3': '分',
    }

    assert unit_param_dict == expected


def test_convert_unit_to_param_00002344():
    sample_file = 'weekcook/org/weekcook_00002344.txt'
    strings = text_to_strings(sample_file)
    numparam_dict = convert_num_to_param(strings)
    wakachi_file = 'weekcook/procedure_3/weekcook_00002344_proc3.txt'
    wakachi_string = text_to_strings(wakachi_file)
    unit_param_dict = convert_unit_to_param(wakachi_string, numparam_dict)
    print(unit_param_dict)
    expected = {
        'unit1': 'cm',
        'unit2': '%',
        'unit3': '分',
    }

    assert unit_param_dict == expected


def test_convert_unit_to_param_00003159():
    sample_file = 'weekcook/org/weekcook_00003159.txt'
    strings = text_to_strings(sample_file)
    numparam_dict = convert_num_to_param(strings)
    wakachi_file = 'weekcook/procedure_3/weekcook_00003159_proc3.txt'
    wakachi_string = text_to_strings(wakachi_file)
    unit_param_dict = convert_unit_to_param(wakachi_string, numparam_dict)
    print(unit_param_dict)
    expected = {
        'unit1': 'w',
        'unit2': '分',
        'unit3': '等分',
    }

    assert unit_param_dict == expected


def test_convert_cooking_time_strings_sample():
    sample_file = 'weekcook/org/weekcook_sample.txt'
    strings = text_to_strings(sample_file)
    convert_strings = convert_cooking_time_strings(strings)
    expected = ['8分']

    assert convert_strings == expected


def test_convert_cooking_time_strings_00000083():
    sample_file = 'weekcook/org/weekcook_00000083.txt'
    strings = text_to_strings(sample_file)
    convert_strings = convert_cooking_time_strings(strings)
    expected = ['15～20分']

    assert convert_strings == expected


def test_convert_cooking_time_strings_00000257():
    sample_file = 'weekcook/org/weekcook_00000257.txt'
    strings = text_to_strings(sample_file)
    convert_strings = convert_cooking_time_strings(strings)
    expected = ['10分', '5分', '1分']

    assert convert_strings == expected


def test_convert_cooking_time_strings_00001977():
    sample_file = 'weekcook/org/weekcook_00001977.txt'
    strings = text_to_strings(sample_file)
    convert_strings = convert_cooking_time_strings(strings)
    expected = []

    assert convert_strings == expected


def test_convert_cooking_time_strings_00002816():
    sample_file = 'weekcook/org/weekcook_00002816.txt'
    strings = text_to_strings(sample_file)
    convert_strings = convert_cooking_time_strings(strings)
    expected = ['2～3分']

    assert convert_strings == expected


def test_convert_cooking_time_strings_00003159():
    sample_file = 'weekcook/org/weekcook_00003159.txt'
    strings = text_to_strings(sample_file)
    convert_strings = convert_cooking_time_strings(strings)
    expected = ['2～3分']

    assert convert_strings == expected


def test_convert_cooking_time_strings_00003363():
    sample_file = 'weekcook/org/weekcook_00003363.txt'
    strings = text_to_strings(sample_file)
    convert_strings = convert_cooking_time_strings(strings)
    expected = ['5分']

    assert convert_strings == expected


def test_convert_cooking_time_wakachi_sample():
    wakachi_file = 'weekcook/procedure_3/weekcook_sample_proc3.txt'
    wakachi_strings = text_to_strings(wakachi_file)
    convert_strings = convert_cooking_time_wakachi(wakachi_strings)
    expected = ['8分']

    assert convert_strings == expected


# def test_preordering_for_cooking_time_sample():
#     sample_file = 'weekcook/org/weekcook_sample.txt'
#     strings = text_to_strings(sample_file)
#     convert_strings = convert_cooking_time_strings(strings)
#     preordering_strings = preordering_for_cooking_time_strings(strings, convert_strings)
#     expected = '塩鮭は骨と皮を取り除き1cm厚さに斜め切りにし、ペーパータオルで包んで水気を取る。\nアボカドは半分に切りタネを除いて1cm幅に切る。\nスキレットを温めてサラダ油を塗り、塩鮭を軽く両面焼く。\n鮭が焼けたらアボカドを一緒に並べて生クリームを加え、塩とブラックペッパーを少々ふる。\n中火にかけて沸々してきたらチーズ（ピザ用）を乗せ、オーブントースターで焼いて焦げ目が付いたら完成。(目安: 約8分)\n'

#     assert preordering_strings == expected


# def test_preordering_for_cooking_time_wakachi_sample():
#     wakachi_file = 'weekcook/procedure_3/weekcook_sample_proc3.txt'
#     wakachi_string = text_to_strings(wakachi_file)
#     convert_strings = convert_cooking_time_wakachi(wakachi_string)
#     preordering_strings = preordering_for_cooking_time_wakachi(wakachi_file, convert_strings)
#     expected = ['塩鮭', 'は', '骨', 'と', '皮', 'を', '取り除', 'き', '1', 'cm', '厚', 'さ', 'に', '斜め切り', 'に', 'し', '、', 'ペーパー', 'タオル', 'で', '包', 'ん', 'で', '水気', 'を', '取', 'る','。\n', 'アボカド', 'は', '半分', 'に', '切', 'り', 'タネ', 'を', '除', 'い', 'て', '1', 'cm', '幅', 'に', '切', 'る', '。\n', 'スキレット', 'を', '温め', 'て', 'サラダ', '油', 'を', '塗', 'り', '、', '塩鮭', 'を', '軽', 'く', '両面', '焼', 'く', '。\n', '鮭', 'が', '焼け', 'たら', 'アボカド', 'を', '一緒', 'に', '並べ', 'て', '生', 'クリーム', 'を', '加え', '、', '塩', 'と', 'ブラック', 'ペッパー', 'を', '少々', 'ふ', 'る', '。\n', '中火', 'に', 'かけ', 'て', '沸々', 'し', 'て', 'き', 'たら', 'チーズ', '（', 'ピザ', '用', '）', 'を', '乗せ', '、', 'オーブン', 'トースター','で', '焼', 'い', 'て', '焦げ', '目', 'が', '付', 'い', 'たら', '完成', '。(目安: 約8分)\n']

#     assert preordering_strings == expected


# def test_preordering_for_cooking_time_wakachi_00003159():
#     wakachi_file = 'weekcook/procedure_3/weekcook_00003159_proc3.txt'
#     wakachi_string = text_to_strings(wakachi_file)
#     convert_strings = convert_cooking_time_wakachi(wakachi_string)
#     preordering_strings = preordering_for_cooking_time_wakachi(wakachi_file, convert_strings)
#     expected = ['新', 'じゃがいも', 'は', '良', 'く', '洗', 'っ', 'て', '皮', '付き', 'の', 'まま', 'ラップ', 'に', '包', 'む', '。', '新', '玉ねぎ', 'は', '薄切り', 'に', 'し', 'て', '冷水', 'に', 'は', 'な', 'し', 'て', 'お', 'く', '。', 'ミニ', 'トマト', 'は', '半分', 'に', '切', 'る', '。\n', '新', 'じゃがいも', 'を', '耐熱', '皿', 'に', 'のせ', '、', '電子', 'レンジ', 'で', '加熱', 'し', '、(目安: 600w 約2～3分)', '竹串', 'が', 'スッ', 'と', '通', 'る', 'こと', 'を', '確認', 'し', '冷ま', 'し', 'て', 'お', 'く', '。\n', '新', '玉ねぎ', 'を', '絞', 'る', 'よう', 'に', 'し', 'て', '水気', 'を', 'しっかり', 'とき', 'る', '。\n', '新', 'じゃがいも', 'を', '8', '等', '分', 'ほど', 'に', '切', 'り', '、', 'ボール', 'に', '2', 'の', '新', '玉ねぎ', '、', 'ミニ', 'トマト', 'と', '一緒', 'に', '入れ', 'て', 'マヨネーズ', 'と', '胡椒', 'を', '加え', 'て', '良く', '混ぜ合わせ', 'る', '。\n', '器', 'に', '盛り付け', 'ドライ', 'パセリ', 'を', '散ら', 'し', 'て', '完成', '。\n']

#     assert preordering_strings == expected
    

def test_preordering_for_cooking_time_wakachi_00000083():
    wakachi_file = 'weekcook/procedure_3/weekcook_00000083_proc3.txt'
    wakachi_string = text_to_strings(wakachi_file)
    convert_strings = convert_cooking_time_strings(wakachi_string)
    preordering_strings = preordering_for_cooking_time_wakachi(wakachi_file, convert_strings)
    expected = ['さんま', 'は', '頭', 'と', '内臓', '（', '腸', '）', 'を', '取除', 'い', 'た', '後', '、', '水', 'で', 'よく', '洗', 'っ', 'て', 'から', 'ペーパー', 'タオル', 'で', '水気', 'を', '拭き取', 'る', '。\n', 'グリル', '（', 'フライパン', 'で', 'も', '可', '）', 'に', 'サラダ', '油', '（', '分量', '外', '）', 'を', '塗', 'る', '。\n', 'さんま', 'に', '塩', 'を', '振', 'っ', 'て', 'から', '、', '温め', 'た', 'グリル', '（', 'フライパン', 'で', 'も', '可', '）', 'に', '並べ', '、', '（', 'フライパン', 'の', '場合', 'は', '火', 'が', '通', 'る', 'まで', '）', '焼', 'く', '。(目安: 約15～20分)\n',  '焼き上が', 'っ', 'た', 'さんま', 'の', '塩焼き', 'を', '、', 'お', '好み', 'で', '笹', 'を', '敷', 'い', 'た', '器', 'に', '盛り付け', '、', 'お', '好み', 'で', 'すだち', 'や', '大根', 'おろし', 'を', '添え', 'たら', '完成', '。\n']

    assert preordering_strings == expected


def test_sort_by_values_len():
    test_dict = {'unit1': 'w', 'unit2': '分', 'unit3': '等分'}
    expected = [{'unit3': '等分'}, {'unit1': 'w'}, {'unit2': '分'}]
    sort_dict = sort_dict_by_values_length(test_dict)

    assert sort_dict == expected


# def test_convert_recipe_parameter_sample():
#     org_file = 'weekcook/org/weekcook_sample.txt'
#     org_lines = text_to_strings(org_file)

#     wakachi_file = 'weekcook/procedure_3/weekcook_sample_proc3.txt'
#     wakachi_string = text_to_strings(wakachi_file)

#     json_filepath = 'weekcook/ingredient_json/weekcook_sample.json'
#     with open(json_filepath, 'r', encoding='utf-8') as j:
#         ingredient_dict = json.load(j)

#     num_param_dict = convert_num_to_param(org_lines)
#     tool_param_dict = convert_tool_to_param(org_lines)
#     unit_param_dict = convert_unit_to_param(wakachi_string, num_param_dict)
#     ingredient_param_dict = {'ingredient' + str(idx): v
#                              for idx, v in enumerate(ingredient_dict.keys())
#                              if v != '材料'}
#     convert_strings = convert_cooking_time_wakachi(wakachi_file)
#     preordering_wakachi_array = preordering_for_cooking_time_wakachi(
#         wakachi_file,
#         convert_strings,
#     )

#     converted_strings, _ = convert_recipe_parameter(
#         preordering_wakachi_array,
#         ingredient_param_dict,
#         num_param_dict,
#         unit_param_dict,
#         tool_param_dict,
#         )
#     expected = '<param9>は骨と皮を取り除き<param1><param5>厚さに斜め切りにし、ペーパータオルで包んで水気を取る。\n<param8>は半分に切りタネを除いて<param2><param6>幅に切る。\nスキレットを温めてサラダ油を塗り、<param9>を軽く両面焼く。\n鮭が焼けたら<param8>を一緒に並べて<param10>を加え、<param12>と<param13>を少々ふる。\n中火にかけて沸々してきたら<param11>を乗せ、<param14>で焼いて焦げ目が付いたら完成。(目安: 約<param3><param4><param7>)\n'

#     assert converted_strings == expected


def test_convert_recipe_parameter_00000083():
    org_file = 'weekcook/org/weekcook_00000083.txt'
    org_lines = text_to_strings(org_file)

    wakachi_file = 'weekcook/procedure_3/weekcook_00000083_proc3.txt'
    wakachi_string = text_to_strings(wakachi_file)

    json_filepath = 'weekcook/ingredient_json/weekcook_00000083.json'
    with open(json_filepath, 'r', encoding='utf-8') as j:
        ingredient_dict = json.load(j)

    num_param_dict = convert_num_to_param(org_lines)
    tool_param_dict = convert_tool_to_param(org_lines)
    unit_param_dict = convert_unit_to_param(wakachi_string, num_param_dict)
    ingredient_param_dict = {'ingredient' + str(idx): v
                             for idx, v in enumerate(ingredient_dict.keys())
                             if v != '材料'}
    convert_strings = convert_cooking_time_wakachi(wakachi_file)
    preordering_wakachi_array = preordering_for_cooking_time_wakachi(
        wakachi_file,
        convert_strings,
    )

    converted_strings, _ = convert_recipe_parameter(
        preordering_wakachi_array,
        ingredient_param_dict,
        num_param_dict,
        unit_param_dict,
        tool_param_dict,
        )
    expected = '<param4>は頭と内臓（腸）を取除いた後、水でよく洗ってからペーパータオルで水気を拭き取る。\n<param7>（<param6>でも可）にサラダ油（分量外）を塗る。\n<param4>に<param5>を振ってから、温めた<param7>（<param6>でも可）に並べ、（<param6>の場合は火が通るまで）焼く。(目安: 約<param1>～<param2><param3>)\n焼き上がった<param4>の<param5>焼きを、お好みで笹を敷いた器に盛り付け、お好みですだちや大根おろしを添えたら完成。\n'

    assert converted_strings == expected


# def test_convert_recipe_parameter_00000257():
#     org_file = 'weekcook/org/weekcook_00000257.txt'
#     org_lines = text_to_strings(org_file)

#     wakachi_file = 'weekcook/procedure_3/weekcook_00000257_proc3.txt'
#     wakachi_string = text_to_strings(wakachi_file)

#     json_filepath = 'weekcook/ingredient_json/weekcook_00000257.json'
#     with open(json_filepath, 'r', encoding='utf-8') as j:
#         ingredient_dict = json.load(j)

#     num_param_dict = convert_num_to_param(org_lines)
#     tool_param_dict = convert_tool_to_param(org_lines)
#     unit_param_dict = convert_unit_to_param(wakachi_string, num_param_dict)
#     ingredient_param_dict = {'ingredient' + str(idx): v
#                              for idx, v in enumerate(ingredient_dict.keys())
#                              if v != '材料'}
#     convert_strings = convert_cooking_time_wakachi(wakachi_file)
#     preordering_wakachi_array = preordering_for_cooking_time_wakachi(
#         wakachi_file,
#         convert_strings,
#     )

#     converted_strings, _ = convert_recipe_parameter(
#         preordering_wakachi_array,
#         ingredient_param_dict,
#         num_param_dict,
#         unit_param_dict,
#         tool_param_dict,
#         )
#     expected = '<param11>は、約、(目安: 約<param1><param2><param7>)<param15>に浸けて戻してから、食べ易い長さに切る。\n<param13>は千切りに、<param12>は<param3><param10>幅に切る。\n鍋に<param11>と<param12>、<param13>、★の<param15>と<param16>を入れて、約、(目安: 約<param4><param5><param8>)火にかける。\n<param14>は洗ってから筋を取り、斜めに切って鍋に加え、蓋をして、約、(目安: 約<param6><param9>)蒸らしてから火を止める。\n<param11>と<param12>の煮物を器に盛り付け完成。\n'

#     assert converted_strings == expected


# # def test_convert_recipe_parameter_sample():
# #     org_file = 'weekcook/org/weekcook_00003159.txt'
# #     org_lines = text_to_strings(org_file)

# #     wakachi_file = 'weekcook/procedure_3/weekcook_00003159_proc3.txt'
# #     wakachi_string = text_to_strings(wakachi_file)

# #     json_filepath = 'weekcook/ingredient_json/weekcook_00003159.json'
# #     with open(json_filepath, 'r', encoding='utf-8') as j:
# #         ingredient_dict = json.load(j)

# #     num_param_dict = convert_num_to_param(org_lines)
# #     tool_param_dict = convert_tool_to_param(org_lines)
# #     unit_param_dict = convert_unit_to_param(wakachi_string, num_param_dict)
# #     ingredient_param_dict = {'ingredient' + str(idx): v
# #                              for idx, v in enumerate(ingredient_dict.keys())
# #                              if v != '材料'}
# #     convert_strings = convert_cooking_time_wakachi(wakachi_file)
# #     preordering_wakachi_array = preordering_for_cooking_time_wakachi(
# #         wakachi_file,
# #         convert_strings,
# #     )

# #     converted_strings, _ = convert_recipe_parameter(
# #         preordering_wakachi_array,
# #         ingredient_param_dict,
# #         num_param_dict,
# #         unit_param_dict,
# #         tool_param_dict,
# #         )
# #     expected = '<param9>は良く洗って皮付きのままラップに包む。<param10>は薄切りにして冷水にはなしておく。<param11>は半分に切る。\n<param9>を耐熱皿にのせ、<param14>で加熱し、(目安:<param1><param2>約<param3>～<param4><param5>)竹串がスッと通ることを確認し冷ましておく。\n<param10>を絞るようにして水気をしっかりときる。\n<param9>を<param6><param7>ほどに切り、ボールに<param8>の<param10>、<param11>と一緒に入れて<param12>と<param13>を加えて良く混ぜ合わせる。\n器に盛り付けドライパセリを散らして完成。\n'

# #     assert converted_strings == expected


# # def test_convert_time_70percent():
# #     wakachi_file = 'weekcook/procedure_3/weekcook_sample_proc3.txt'
# #     wakachi_string = text_to_strings(wakachi_file)
