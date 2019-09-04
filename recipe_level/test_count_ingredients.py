import os
import json
from count_ingredients import count_elements
from count_ingredients import output_jsondata
from count_ingredients import count_lf
from count_ingredients import fetch_recipename
from count_ingredients import compute_mean
from count_ingredients import count_action_category
from count_ingredients import compute_max
from count_ingredients import standardization_by_level
from count_ingredients import count_string_length


def test_count_words_of_cut():
    test_data = './rne_wakachi/recipe_2_ner_result.txt'
    test_json = './action_category/action_category.json'
    expected = 1
    result = count_action_category('切る', test_data, test_json)

    assert result == expected


def test_count_words_of_mix():
    test_data = './rne_wakachi/recipe_2_ner_result.txt'
    test_json = './action_category/action_category.json'
    expected = 6
    result = count_action_category('混ぜる', test_data, test_json)

    assert result == expected


def test_count_words_of_heat():
    test_data = './rne_wakachi/recipe_2_ner_result.txt'
    test_json = './action_category/action_category.json'
    expected = 3
    result = count_action_category('加熱', test_data, test_json)

    assert result == expected


def test_count_string_length():
    test_data = './test_file/test_count_string_length.txt'
    expected = 6
    result = count_string_length(test_data)

    assert result == expected
    


def test_count_elements():
    test_file = '../recipe_conv/weekcook/ingredient_json/recipe_2.json'
    expected = 4
    result = count_elements(test_file)

    assert result == expected


def test_count_lf():
    test_file = './rne_wakachi/recipe_2_ner_result.txt'
    expected = 3
    result = count_lf(test_file)

    assert result == expected


def test_output_json():
    test_ingredients_key = 'number_of_ingredients'
    test_ingredients_value = str(4)
    test_sentences_key = 'number_of_sentences'
    test_sentences_value = str(8)
    test_actions_key = 'number_of_actions'
    test_actions_value = str(5)
    test_ingredients_dict = {test_ingredients_key: test_ingredients_value}
    test_sentences_dict = {test_sentences_key: test_sentences_value}
    test_actions_dict = {test_actions_key: test_actions_value}
    expected = '[{"number_of_ingredients": "4"}, {"number_of_sentences": "8"}, {"number_of_actions": "5"}]'
    result = output_jsondata(
        test_ingredients_dict,
        test_sentences_dict,
        test_actions_dict,
    )

    assert result == expected


def test_fetch_recipename():
    _HOME = os.path.expanduser("~")
    _RECIPEDB_DIR = os.path.join(_HOME, 'var/data/recipe/weekcook/recipe_root')
    test_file = os.path.join(_RECIPEDB_DIR, 'recipe_2.json')
    expected = 'あげとわかめのお味噌汁'
    result = fetch_recipename(test_file)

    assert result == expected


def test_compute_mean():
    test_data = {
        'key': 'key',
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 10,
        '6': 10,
        '7': 10,
        '8': 10,
        '9': 10,
    }
    expected = 5
    result = compute_mean(test_data)

    assert result == expected


def test_compute_max():
    test_data = {
        'key': 'key',
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 10,
        '6': 10,
        '7': 10,
        '8': 10,
        '9': 10,
    }
    expected = 10
    result = compute_max(test_data)

    assert result == expected


def test_standardization_by_max_value():
    test_data = {
        'key': 'key',
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 10,
        '6': 10,
        '7': 10,
        '8': 10,
        '9': 10,
    }
    expected = {
        'key': 'key',
        '0': 0.0,
        '1': 0.0,
        '2': 0.0,
        '3': 0.0,
        '4': 0.0,
        '5': 1.0,
        '6': 1.0,
        '7': 1.0,
        '8': 1.0,
        '9': 1.0,
    }

    result = standardization_by_level(test_data, 10.0, 1)

    assert result == expected
