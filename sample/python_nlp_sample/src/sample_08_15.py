import json

import word2vec

if __name__ == '__main__':
    results = word2vec.analogy(('フランス', 'パリ'), '日本')
    print(json.dumps(results, indent=4, ensure_ascii=False))
