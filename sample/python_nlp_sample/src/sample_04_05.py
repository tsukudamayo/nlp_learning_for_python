import sqlitedatastore as datastore

if __name__ == '__main__':
    datastore.connect()
    for doc_id in datastore.get_all_ids(limit=200):
        row = datastore.get(doc_id, fl=['content'])
        text = row['content']

        print('tokens:')
        for token in datastore.get_annotation(doc_id, 'token'):
            print('  ', token['POS'], '\t', text[token['begin']:token['end']])

        print('chunks:')
        chunks = datastore.get_annotation(doc_id, 'chunk')
        for chunk in chunks:
            _, link = chunk['link']
            print('  ', text[chunk['begin']:chunk['end']])
            if link != -1:
                parent = chunks[link]
                print('\t-->', text[parent['begin']:parent['end']])
            else:
                print('\t-->', 'None')

        print('sentences:')
        for sent in datastore.get_annotation(doc_id, 'sentence'):
            print('  ', text[sent['begin']:sent['end']])

    datastore.close()
