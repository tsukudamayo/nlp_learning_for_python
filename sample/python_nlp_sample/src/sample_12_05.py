import json

import bottle
import dbpediaknowledge
import solrindexer as indexer


@bottle.route('/')
def index_html():
    return bottle.static_file('sample_12_06.html', root='./src/static')


@bottle.route('/file/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./src/static')


@bottle.get('/get')
def get():
    name = bottle.request.params.name
    keywords = bottle.request.params.keywords.split()
    keywords_expanded = [[keyword] + [synonym['term'] for synonym
                            in dbpediaknowledge.get_synonyms(keyword)]
                         for keyword in keywords]

    if keywords_expanded != []:
        fl_keyword_pairs = [(name + '_txt_ja', keywords_expanded)]
    else:
        fl_keyword_pairs = [('name_s', [[name]])]

    results = indexer.search_annotation(fl_keyword_pairs)
    return json.dumps(results, ensure_ascii=False)


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port='8702')
