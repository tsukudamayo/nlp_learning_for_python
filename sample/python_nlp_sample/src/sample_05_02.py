import sqlitedatastore as datastore

if __name__ == '__main__':
    datastore.connect()
    anno_name = 'affiliation'
    for doc_id in datastore.get_all_ids(limit=-1):
        row = datastore.get(doc_id, fl=['content'])
        text = row['content']
        annos = datastore.get_annotation(doc_id, anno_name)
        for anno in annos:
            print('{0}: {1}'.format(anno_name.upper(),
                                    text[anno['begin']:anno['end']]))
    datastore.close()
