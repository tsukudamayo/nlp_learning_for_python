import json

import solrindexer as indexer

if __name__ == '__main__':
    results = indexer.search_annotation(
        fl_keyword_pairs=[
            ('affiliation_txt_ja', [['インド']])
        ],
        rows=5
    )
    print(json.dumps(results, indent=4, ensure_ascii=False))
