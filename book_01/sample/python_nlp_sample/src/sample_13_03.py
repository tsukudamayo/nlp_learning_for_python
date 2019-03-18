import sys

import sqlitedatastore as datastore

if __name__ == '__main__':
    datastore.connect()
    anno_dict = {}
    begin = None
    last = {'label': 'E'}
    for line in sys.stdin:
        pair = line.rstrip().split('\t')
        if len(pair) != 6:
            cur = {
                'label': 'E'  # 文末
            }
        else:
            cur = {
                'id':       int(pair[2]),
                'begin':    int(pair[3]),
                'end':      int(pair[4]),
                'label':    pair[5][0],  # 1文字目のみ取得
            }

        if last['label'] in ['B', 'I'] and cur['label'] in ['B', 'O', 'E']:
            anno_dict.setdefault(last['id'], []).append({
                'begin':    begin,
                'end':      last['end']
            })
        elif last['label'] in ['O', 'E'] and cur['label'] == 'I':
            cur['label'] = 'O'

        if cur['label'] == 'B':
            begin = cur['begin']

        last = cur

    for doc_id, annos in anno_dict.items():
        datastore.set_annotation(doc_id, 'affiliation_crf', annos)

    datastore.close()
