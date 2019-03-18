import urllib.request

import cchardet

if __name__ == '__main__':
    url = 'https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC'
    with urllib.request.urlopen(url) as res:
        byte = res.read()
        # 文字コードの変換：cchardetを使って自動で文字コードを判定
        html = byte.decode(cchardet.detect(byte)['encoding'])
        print(html)
