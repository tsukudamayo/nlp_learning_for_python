from countAC import sum_dict


def test_reduce_dict():
    sample_dict_1 = {'a': 1, 'b': 1}
    sample_dict_2 = {'a': 1, 'c': 1}

    expected = {'a': 2, 'b': 1, 'c': 1}
    result = sum_dict(sample_dict_1, sample_dict_2)

    assert result == expected
