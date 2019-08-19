from count_ingredients import count_elements
from count_ingredients import output_jsondata
from count_ingredients import count_lf


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
    
