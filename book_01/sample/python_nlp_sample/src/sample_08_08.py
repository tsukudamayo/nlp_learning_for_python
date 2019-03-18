import json

import wordnetknowledge

if __name__ == '__main__':
    synonyms = wordnetknowledge.get_synonyms('アメリカ合衆国')
    print(json.dumps(synonyms, indent=4, ensure_ascii=False))
