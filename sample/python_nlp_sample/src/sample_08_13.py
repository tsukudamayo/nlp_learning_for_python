import json

import word2vec

if __name__ == '__main__':
    synonyms = word2vec.get_synonyms('アメリカ')
    print(json.dumps(synonyms, indent=4, ensure_ascii=False))
