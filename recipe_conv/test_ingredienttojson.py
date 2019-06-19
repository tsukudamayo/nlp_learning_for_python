import os
from ingredienttojson import parse_number_of_serve
from ingredienttojson import ingredient_div_to_array
from ingredienttojson import ingredients_to_dict


_LOG_DIR = './weekcook_web/ingredient'


def test_ingedient_div_to_array():
    sample_file = 'weekcook_sample.txt'
    strings = ingredient_div_to_array(_LOG_DIR, sample_file)
    print('test_ingredient_div_to_array')
    print(strings)
    expected = ['材料4人分', 'アボカド', '2個', '塩鮭', '4切れ', '生クリーム', '200ml', 'チーズ（ピザ用）', '40g', '塩', '少々', 'ブラックペッパー', '少々']

    assert strings == expected


def test_parse_number_of_serve():
    sample_text = '材料4人分'
    serve_dict = parse_number_of_serve(sample_text)
    print('test_parse_number_of_serve')
    print(serve_dict)
    expected = {'材料': '4人分'}

    assert serve_dict == expected


def test_ingredients_to_dict():
    sample_file = 'weekcook_sample.txt'
    strings = ingredient_div_to_array(_LOG_DIR, sample_file)
    ingredients_dict = ingredients_to_dict(strings)
    print('test_ingredient_to_dict')
    print(ingredients_dict)
    expected = {
        "材料": "4人分",
        "アボカド": "2個",
        "塩鮭": "4切れ",
        "生クリーム": "200ml",
        "チーズ（ピザ用）": "40g",
        "塩": "少々",
        "ブラックペッパー": "少々"
    }

    assert ingredients_dict == expected

