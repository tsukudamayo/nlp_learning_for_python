import json

import solrindexer as indexer

if __name__ == '__main__':
    results = indexer.search(keywords=[['アメリカ'], ['大学']], rows=5)

    print('responseHeader')
    print(json.dumps(results['responseHeader'],
                     indent=4, ensure_ascii=False), '\n\n')

    print('highlighting')
    print(json.dumps(results['highlighting'],
                     indent=4, ensure_ascii=False), '\n\n')

    print('response')
    print(results['response']['numFound'])
    for row in results['response']['docs']:
        for fl, value in row.items():
            if fl == 'content_txt_ja':
                value = value[:300].replace('\n', ' ')
            print('{0}\t{1}'.format(fl, value))
        print()
