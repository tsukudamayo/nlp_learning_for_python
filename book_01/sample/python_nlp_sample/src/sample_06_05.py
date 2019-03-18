import json

import bottle


@bottle.route('/')
def index_html():
    return bottle.static_file('sample_06_06.html', root='./src/static')


@bottle.route('/file/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./src/static')


@bottle.get('/get')
def get():
    data = {
        'collection': {
            'entity_types': [
                {
                    'type': 'Person',
                    'bgColor': '#7fa2ff',
                    'borderColor': 'darken'
                }
            ],
        },
        'annotation': {
            'text': "Ed O'Kelley was the man who shot the man who shot Jesse James.",
            'entities': [
                [
                    'T1',
                    'Person',
                    [[0, 11]]
                ],
                [
                    'T2',
                    'Person',
                    [[20, 23]]
                ],
                [
                    'T3',
                    'Person',
                    [[37, 40]]
                ],
                [
                    'T4',
                    'Person',
                    [[50, 61]]
                ]
            ],
            'relations': [
                [
                    'R1',
                    'Anaphora',
                    [['Anaphor', 'T2'], ['Entity', 'T1']]
                ]
            ],
        },
    }
    return json.dumps(data, ensure_ascii=False)


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port='8702')
