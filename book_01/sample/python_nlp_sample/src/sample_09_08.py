import json

import bottle
import solrindexer as indexer


@bottle.route('/')
def index_html():
    return bottle.static_file('sample_09_06.html', root='./src/static')


@bottle.route('/file/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./src/static')


@bottle.get('/get')
def get():
    keywords = bottle.request.params.keywords.split()
    keywords_expanded = [[keyword] for keyword in keywords]

    results = indexer.search(
        # keywords=[[keyword] for keyword in keywords],
        keywords=keywords_expanded,
    )
    return json.dumps(results, ensure_ascii=False)


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port='8702')
