import re

import sqlitedatastore as datastore


def create_annotation(doc_id, ptn):
    row = datastore.get(doc_id, fl=['content'])
    text = row['content']
    annos = []
    for chunk in datastore.get_annotation(doc_id, 'chunk'):
        chunk_str = text[chunk['begin']:chunk['end']]
        m = ptn.search(chunk_str)
        if not m:
            continue
        anno = {
            'begin':    chunk['begin'] + m.start(),
            'end':      chunk['begin'] + m.end(),
        }
        print(text[anno['begin']:anno['end']])
        annos.append(anno)
    return annos


if __name__ == '__main__':
    dic = [
        r'.+?大学',
        r'.+?学会',
        r'.+?協会',
    ]
    ptn = re.compile(r'|'.join(dic))

    anno_name = 'affiliation'

    datastore.connect()
    for doc_id in datastore.get_all_ids(limit=-1):
        annos = create_annotation(doc_id, ptn)
        datastore.set_annotation(doc_id, anno_name, annos)
    datastore.close()
