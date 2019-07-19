from generate_rne_wakachi_file import preprocess_rnetag


def test_preprocess_rnetag():
    data = '玉ねぎ/F は すりおろ/Ac す 。\nすりおろ/Ac し た 玉ねぎ/F に 、 おろし=にんにく/F と おろ/Ac し 生姜 、 still/F たれ と 赤味噌/F 、 豆板=醤/F を 加え/Ac て 、 よく 混ぜ合わせ/Ac て タレ/F を 作/Ac り 、 牛=ロース=肉/F を 漬け/Ac る 。\nタレ/F に 漬け/Ac た 牛=ロース=肉/F を グリル/F （ フライパン/T で も 可 ） で 焼/Ac く 。\nサンチュ/F を 敷/Ac い た 器/T に 焼肉/F を 盛り付け/Ac 、 お 好み で キムチ/F を 添え/Ac たら 完成/Af 。'
    result = preprocess_rnetag(data)
    expected = '玉ねぎ は すりおろ す 。\nすりおろ し た 玉ねぎ に 、 おろしにんにく と おろ し 生姜 、 still たれ と 赤味噌 、 豆板醤 を 加え て 、 よく 混ぜ合わせ て タレ を 作 り 、 牛ロース肉 を 漬け る 。\nタレ に 漬け た 牛ロース肉 を グリル （ フライパン で も 可 ） で 焼 く 。\nサンチュ を 敷 い た 器 に 焼肉 を 盛り付け 、 お 好み で キムチ を 添え たら 完成 。'

    assert expected == result
