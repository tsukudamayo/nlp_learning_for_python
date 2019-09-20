from search_ingredients import extarct_from_weekcook_db


def test_extract_from_weekcook_db_recipe_2():
    test_data = './test_file/test_recipe_2.json'
    expected = {
        "id": 2,
        "title": "あげとわかめのお味噌汁",
        "ingredients": ["だし", "乾燥わかめ", "油揚げ", "白味噌"],
        "numof": 4
    }
    result = extarct_from_weekcook_db(test_data)

    assert result == expected


def test_extract_from_weekcook_db_recipe_3112():
    test_data = './test_file/test_recipe_3112.json'
    expected = {
        "id": 3112,
        "title": "おひな様のちらし寿司",
        "ingredients": ['しょう油', 'だし汁', 'みりん', 'エビ', 'サラダ油', 'ハマグリ', 'レンコン', '人参', '卵', '塩', '干し椎茸', '日本酒', '昆布', '桜でんぶ', '砂糖', '米', '絹さや', '酢'],
        "numof": 18
    }
    result = extarct_from_weekcook_db(test_data)
    print('result')
    print(result)

    assert result == expected
