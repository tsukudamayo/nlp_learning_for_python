import os
import json
from count_ingredients import count_elements
from count_ingredients import output_jsondata
from count_ingredients import count_lf
from count_ingredients import fetch_recipename
from count_ingredients import compute_mean


def test_count_elements():
    test_file = '../recipe_conv/weekcook/ingredient_json/recipe_2.json'
    expected = 4
    result = count_elements(test_file)

    assert result == expected


def test_count_words():
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
