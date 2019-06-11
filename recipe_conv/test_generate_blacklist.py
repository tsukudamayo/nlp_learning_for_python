from generate_blacklist import split_food_tag
from generate_blacklist import extract_ner_foodlist
from generate_blacklist import compare_foodlist_with_parmeters
from generate_blacklist import is_param_in_parameterstrings


def test_split_food_tag_1():
    sample_strings = '玉ねぎ/F'
    expected = '玉ねぎ'
    result = split_food_tag(sample_strings)

    assert result == expected


def test_split_food_tag_2():
    sample_strings = 'すりおろ/Ac'
    expected = ''
    result = split_food_tag(sample_strings)

    assert result == expected


def test_extract_ner_foodlist():
    sample_file = 'weekcook/ner_result/weekcook_00000001_ner_result.txt'
    expected = ['玉ねぎ', '玉ねぎ', 'おろし', 'still', '赤味噌', '豆板', 'タレ', '牛ロース肉', 'タレ', '牛ロース肉', 'グリル', 'サンチュ', '焼肉', 'キムチ']
    foodlist = extract_ner_foodlist(sample_file)

    assert foodlist == expected


def test_is_param_in_parameterstrings_true():
    sample_strings = 'タレ'
    sample_paramstrings = '<param2>はすりおろす。\nすりおろした<param2>に、<param4>と<param5>、<param6>と<param7>、<param8>を加えて、よく混ぜ合わせてタレを作り、牛ロース肉を漬ける。\nタレに漬けた牛ロース肉を<param10>（<param9>でも可）で焼く。\n<param3>を敷いた器に焼肉を盛り付け、お好みでキムチを添えたら完成。\n'
    expected = 'タレ'
    result = is_param_in_parameterstrings(sample_strings, sample_paramstrings)

    assert result == expected


def test_is_param_in_parameterstrings_false():
    sample_strings = 'still'
    sample_paramstrings = '<param2>はすりおろす。\nすりおろした<param2>に、<param4>と<param5>、<param6>と<param7>、<param8>を加えて、よく混ぜ合わせてタレを作り、牛ロース肉を漬ける。\nタレに漬けた牛ロース肉を<param10>（<param9>でも可）で焼く。\n<param3>を敷いた器に焼肉を盛り付け、お好みでキムチを添えたら完成。\n'
    expected = ''
    result = is_param_in_parameterstrings(sample_strings, sample_paramstrings)

    assert result == expected


def test_compare_foodlist_with_parameters():
    food_list = ['玉ねぎ', '玉ねぎ', 'おろし', 'still', '赤味噌', '豆板', 'タレ', '牛ロース肉', 'タレ', '牛ロース肉', 'グリル', 'サンチュ', '焼肉', 'キムチ']
    param_strings_file = 'weekcook/paramstrings/weekcook_1_convrecipe.txt'
    expected_set = set(['おろし', 'タレ', '牛ロース肉', '焼肉', 'キムチ'])
    expected = list(expected_set)
    result = compare_foodlist_with_parmeters(food_list, param_strings_file)
    print('result', result)

    assert result == expected
