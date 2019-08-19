from extractAC import count_actag


def test_count_ac_tag():
    sample_strings = '油揚げ/F に 熱湯/F を かけ/Ac て 油抜き/Ac を し/Ac て から 、 食べ 易/Sf い 大き/Sf さ に 切/Ac り 、 乾燥/F わかめ は 水/F で さっ と 洗/Ac う 。 鍋/T に だし/F を 入れ/Ac て 火/T に かけ/Ac 、 沸騰/Af し て き た ら 油揚げ/F を 加え=一/Ac 煮立ち/Af し た ら 一旦 火/T を 止め/Ac る 。 乾燥 わかめ を 加え/Ac て 再び 、 鍋/T を 火/T に かけ/Ac 沸騰/Af し て き た ら 、 白=味噌/F を 溶か/Ac し たら 火/T を 止め/Ac る 。 油揚げ/F と わかめ の お 味噌=汁/F を お 椀/T に よそい分け/Ac て 、 お 好み で 三つ葉/F を 散ら/Ac し たら 完成/Af 。'
    result = count_actag(sample_strings)

    expected = {
        'かけ': 3,
        '止め': 2,
        '油抜き': 1,
        'し': 1,
        '切': 1,
        '洗': 1,
        '入れ': 1,
        '加え一': 1,
        '加え': 1,
        '溶か': 1,
        'よそい分け': 1,
        '散ら': 1,
    }

    assert result == expected