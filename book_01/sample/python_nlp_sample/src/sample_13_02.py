import sqlitedatastore as datastore
from annoutil import find_xs_in_y

if __name__ == '__main__':
    datastore.connect()
    for doc_id in datastore.get_all_ids(limit=-1):
        row = datastore.get(doc_id, fl=['content'])
        text = row['content']
        sentences = datastore.get_annotation(doc_id, 'sentence')
        tokens = datastore.get_annotation(doc_id, 'token')
        for sentence in sentences:
            for token in find_xs_in_y(tokens, sentence):
                print('{0}\t{1}\t{2}\t{3}\t{4}'.format(
                    text[token['begin']:token['end']],
                    token['POS'], doc_id, token['begin'], token['end']))
            print()  # 文の区切り
    datastore.close()
