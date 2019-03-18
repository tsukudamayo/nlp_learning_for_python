import json
import urllib.parse
import urllib.request

# 使用するSolrのURL
solr_url = 'http://localhost:8983/solr'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def load(collection, data):
    # Solrへデータを登録するリクエストを作成（＊２）
    req = urllib.request.Request(
        url='{0}/{1}/update'.format(solr_url, collection),
        data=json.dumps(data).encode('utf-8'),
        headers={'content-type': 'application/json'})

    # データの登録を実行（＊３）
    with opener.open(req) as res:
        # データ確認（＊４）
        print(res.read().decode('utf-8'))

    # コミット（＊５）
    url = '{0}/{1}/update?softCommit=true'.format(solr_url, collection)
    req = urllib.request.Request(url)
    with opener.open(req) as res:
        print(res.read().decode('utf-8'))


def search(keywords, rows=100):
    query = ' AND '.join([
        '(' + ' OR '.join(['content_txt_ja:"{}"'.format(keyword)
                           for keyword in group]) + ')'
        for group in keywords])
    data = {
        'q':     query,
        'wt':    'json',
        'rows':  rows,
        'hl':    'on',
        'hl.fl': 'content_txt_ja',
    }
    # 検索リクエストの作成（＊１）
    req = urllib.request.Request(
        url='{}/doc/select'.format(solr_url),
        data=urllib.parse.urlencode(data).encode('utf-8'),
    )
    # 検索リクエストの実行（＊２）
    with opener.open(req) as res:
        return json.loads(res.read().decode('utf-8'))


def search_annotation(fl_keyword_pairs, rows=100):
    query = ' AND '.join([
        '(' + ' OR '.join(['{0}:"{1}"'.format(fl, keyword)
                           for keyword in group]) + ')'
        for fl, keywords in fl_keyword_pairs
            for group in keywords])
    data = {
        'q':    query,
        'wt':   'json',
        'rows': rows,
    }
    # 検索リクエストの作成（＊１）
    req = urllib.request.Request(
        url='{}/anno/select'.format(solr_url),
        data=urllib.parse.urlencode(data).encode('utf-8'),
    )
    # 検索リクエストの実行（＊２）
    with opener.open(req) as res:
        return json.loads(res.read().decode('utf-8'))
