import sqlitedatastore as datastore

if __name__ == '__main__':
    datastore.connect()
    anno_name = 'affiliation'
    for doc_id in datastore.get_all_ids(limit=-1):
        text = datastore.get(doc_id, fl=['content'])['content']
        with open('result/brat/{0}.txt'.format(doc_id), 'w') as f:
            f.write(text)
        with open('result/brat/{0}.ann'.format(doc_id), 'w') as f:
            for i, anno in enumerate(datastore.get_annotation(doc_id, anno_name)):
                f.write('T{0}\t{1} {2} {3}\t{4}\n'.format(
                    i,
                    'affiliation',
                    anno['begin'],
                    anno['end'],
                    text[anno['begin']:anno['end']]
                ))
    datastore.close()
