import cabochaparser   as parser
import sqlitedatastore as datastore

if __name__ == '__main__':
    datastore.connect()
    for doc_id in datastore.get_all_ids(limit=-1):
        row = datastore.get(doc_id, fl=['content'])
        text = row['content']
        sentences, chunks, tokens = parser.parse(text)
        print('parsed: doc_id =', doc_id)

        datastore.set_annotation(doc_id, 'sentence', sentences)
        datastore.set_annotation(doc_id, 'chunk',    chunks)
        datastore.set_annotation(doc_id, 'token',    tokens)

    datastore.close()
