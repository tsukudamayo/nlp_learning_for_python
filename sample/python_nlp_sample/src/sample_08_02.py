import json

import dbpediaknowledge

if __name__ == '__main__':
    synonyms = dbpediaknowledge.get_synonyms('アメリカ合衆国')
    print(json.dumps(synonyms, indent=4, ensure_ascii=False))
