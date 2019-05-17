import os
import json

from consoleconv import text_to_strings
from consoleconv import convert_num_to_param
from consoleconv import convert_tool_to_param
from consoleconv import convert_unit_to_param
from consoleconv import convert_recipe_parameter


def test_text_to_strings():
    sample_file = 'weekcook/org/weekcook_sample.txt'
    strings = text_to_strings(sample_file)
    print(strings)
    expected = '塩鮭は骨と皮を取り除き1cm厚さに斜め切りにし、ペーパータオルで包んで水気を取る。\nアボカドは半分に切りタネを除いて1cm幅に切る。\nスキレットを温めてサラダ油を塗り、塩鮭を軽く両面焼く。\n鮭が焼けたらアボカドを一緒に並べて生クリームを加え、塩とブラックペッパーを少々ふる。\n中火にかけて沸々してきたらチーズ（ピザ用）を乗せ、オーブントースターで8分焼いて焦げ目が付いたら完成。\n'

    assert strings == expected


def test_convert_num_to_param():
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


def test_convert_recipe_parameter():
    org_file = 'weekcook/org/weekcook_sample.txt'
    org_lines = text_to_strings(org_file)
    
    wakachi_file = 'weekcook/procedure_3/weekcook_sample_proc3.txt'
    wakachi_string = text_to_strings(wakachi_file)

    json_filepath = 'weekcook/ingredient_json/weekcook_sample.json'
    with open(json_filepath, 'r', encoding='utf-8') as j:
        ingredient_dict = json.load(j)
    
    num_param_dict = convert_num_to_param(org_lines)
    tool_param_dict = convert_tool_to_param(org_lines)
    wakachi_file = 'weekcook/procedure_3/weekcook_sample_proc3.txt'
    wakachi_string = text_to_strings(wakachi_file)
    unit_param_dict = convert_unit_to_param(wakachi_string, num_param_dict)
    ingredient_param_dict = {'ingredient' + str(idx): v
                             for idx, v in enumerate(ingredient_dict.keys())
                             if v != '材料'}
    
    converted_strings = convert_recipe_parameter(
        wakachi_file,
        ingredient_param_dict,
        num_param_dict,
        unit_param_dict,
        tool_param_dict,
        )
    expected = '<param8>は骨と皮を取り除き<param1><param2>厚さに斜め切りにし、ペーパータオルで包んで水気を取る。\n<param7>は半分に切りタネを除いて<param3><param4>幅に切る。\nスキレットを温めてサラダ油を塗り、<param8>を軽く両面焼く。\n鮭が焼けたら<param7>を一緒に並べて<param9>を加え、<param11>と<param12>を少々ふる。\n中火にかけて沸々してきたら<param10>を乗せ、<param13>で<param5><param6>焼いて焦げ目が付いたら完成。\n'

    assert converted_strings == expected
