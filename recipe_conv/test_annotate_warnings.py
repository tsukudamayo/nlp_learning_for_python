from annotate_warnings import annotate_warnings
from annotate_warnings import insert_warnings
from annotate_warnings import black_list_to_array


def test_insert_warnings():
    sample_word = '牛ロース肉'

    expected = '<param2>はすりおろす。\nすりおろした<param2>に、<param4>と<param5>、<param6>と<param7>、<param8>を加えて、よく混ぜ合わせてタレを作り、&#x26a0牛ロース肉を漬ける。\nタレに漬けた&#x26a0牛ロース肉を<param10>（<param9>でも可）で焼く。\n<param3>を敷いた器に焼肉を盛り付け、お好みでキムチを添えたら完成。\n'
    test_strings = '<param2>はすりおろす。\nすりおろした<param2>に、<param4>と<param5>、<param6>と<param7>、<param8>を加えて、よく混ぜ合わせてタレを作り、牛ロース肉を漬ける。\nタレに漬けた牛ロース肉を<param10>（<param9>でも可）で焼く。\n<param3>を敷いた器に焼肉を盛り付け、お好みでキムチを添えたら完成。\n'
    result = insert_warnings(sample_word, test_strings)

    assert result == expected


def test_black_list_to_array():
    test_file = 'weekcook/blacklist/blacklist_00000001.json'
    expected = ["牛ロース肉", "タレ", "キムチ", "おろし", "焼肉"]
    result = black_list_to_array(test_file)

    assert result == expected


def test_annotate_warnings():
    expected = '<param2>はすりおろす。\nすり&#x26a0おろした<param2>に、<param4>と<param5>、<param6>と<param7>、<param8>を加えて、よく混ぜ合わせて&#x26a0タレを作り、&#x26a0牛ロース肉を漬ける。\n&#x26a0タレに漬けた&#x26a0牛ロース肉を<param10>（<param9>でも可）で焼く。\n<param3>を敷いた器に&#x26a0焼肉を盛り付け、お好みで&#x26a0キムチを添えたら完成。\n'
    test_file = 'weekcook/paramstrings/weekcook_1_convrecipe.txt'
    black_list = ["牛ロース肉", "タレ", "キムチ", "おろし", "焼肉"]
    result = annotate_warnings(test_file, black_list)
    print('result', result)

    assert result == expected
