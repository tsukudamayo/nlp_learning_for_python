import sqlitedatastore as datastore

if __name__ == '__main__':
    datastore.connect()
    for doc_id in datastore.get_all_ids(limit=-1):
        row = datastore.get(doc_id, ['id', 'content', 'meta_info'])
        print(row['id'], row['meta_info'], row['content'][:100])
    datastore.close()
