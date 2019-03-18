import json

import bottle


@bottle.route('/')
def index_html():
    return bottle.static_file('sample_06_03.html', root='./src/static')


@bottle.route('/file/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./src/static')


@bottle.get('/get')
def get():
    namae = bottle.request.params.namae
    return json.dumps({
        'greet': 'Hello World, {0}!'.format(namae)
    }, ensure_ascii=False)


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port='8702')
