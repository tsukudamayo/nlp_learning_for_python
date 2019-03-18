import urllib.request

import cchardet

# src/scrape.py をライブラリとしてインポート
import scrape

if __name__ == '__main__':
    url = 'https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC'
    with urllib.request.urlopen(url) as res:
        byte = res.read()
        html = byte.decode(cchardet.detect(byte)['encoding'])
        text, title = scrape.scrape(html)
        print('[title]: ', title)
        print('[text]:  ', text[:300])
