import json

import solrindexer as indexer

if __name__ == '__main__':
    results = indexer.search_annotation(
        fl_keyword_pairs=[
            ('cause_txt_ja', [['気候変動']]),
            ('name_s',       [['cause']])
        ])
    print(json.dumps(results, indent=4, ensure_ascii=False))
