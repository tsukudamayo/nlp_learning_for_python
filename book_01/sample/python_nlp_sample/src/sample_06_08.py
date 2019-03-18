import json
import re

import bottle
import sqlitedatastore as datastore


@bottle.route('/')
def index_html():
    return bottle.static_file('sample_06_09.html', root='./src/static')


@bottle.route('/file/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./src/static')


@bottle.get('/get')
def get():
    doc_id = bottle.request.params.id
    names = bottle.request.params.names.split()

    row = datastore.get(doc_id, fl=['content'])
    text = row['content']
    # text = re.sub(r'[。！]', '\n', text)

    data = {
        'collection': {
            'entity_types':     [],
        },
        'annotation': {
            'text':             text,
            'entities':         [],
            'relations':        [],
        },
    }

    mapping = {}
    for name in names:
        annos = datastore.get_annotation(doc_id, name)
        for i, anno in enumerate(annos):
            data['collection']['entity_types'].append({
                'type':        name,
                'bgColor':     '#7fa2ff',
                'borderColor': 'darken'
            })

            Ti = 'T{0:d}'.format(len(data['annotation']['entities']) + 1)
            data['annotation']['entities'].append([
                Ti,
                name,
                [[anno['begin'], anno['end']]]
            ])
            mapping[(name, i)] = Ti

    for name in names:
        annos = datastore.get_annotation(doc_id, name)
        for i, anno in enumerate(annos):
            if 'link' not in anno:
                continue
            name_linked, i_linked = anno['link']
            if (name, i) not in mapping or (name_linked, i_linked) not in mapping:
                continue

            data['annotation']['relations'].append([
                'R{0:d}'.format(len(data['annotation']['relations']) + 1),
                'arg',
                [['src', mapping[(name, i)]], ['tgt', mapping[(name_linked, i_linked)]]]
            ])

    return json.dumps(data, ensure_ascii=False)


if __name__ == '__main__':
    datastore.connect()
    bottle.run(host='0.0.0.0', port='8702')
    datastore.close()
