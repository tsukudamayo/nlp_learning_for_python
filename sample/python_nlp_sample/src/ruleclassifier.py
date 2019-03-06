def contain_yumei(tokens):
    for token in tokens:
        if token['lemma'] == '有名':
            return True
    return False


def contain_LOC(tokens):
    for token in tokens:
        if token.get('NE', '').endswith('LOCATION'):
            return True
    return False


def contain_oishii(tokens):
    for token in tokens:
        if token['lemma'] == 'おいしい':
            return True
    return False


def meibutsu_rule(feature):
    if feature['contain_yumei'] and feature['contain_LOC']:
        return 1
    if feature['contain_oishii']:
        return 1
    return 0


def get_rule():
    return {
        'partial': {
            'contain_yumei':  contain_yumei,
            'contain_LOC':    contain_LOC,
            'contain_oishii': contain_oishii,
        },
        'compound': meibutsu_rule
    }


def convert_into_features_using_rules(sentences, rule):
    features = []
    for doc_id, sent, tokens in sentences:
        feature = {}
        for name, func in rule['partial'].items():
            feature[name] = func(tokens)
        features.append(feature)
    return features


def classify(features, rule):
    return [rule['compound'](feature) for feature in features]
