import json

import wordnetknowledge

if __name__ == '__main__':
    text = '幸福'
    results = wordnetknowledge.get_hypernym(text)
    print(json.dumps(results, indent=4, ensure_ascii=False))
