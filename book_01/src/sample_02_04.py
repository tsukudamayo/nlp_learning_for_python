import re
import unicodedata

text = '	CＬＥＡＮＳing  によりﾃｷｽﾄﾃﾞｰﾀを変換すると　トラブルが少なくなります.'
print('Before:', text)

text = unicodedata.normalize('NFKC', text)
text = re.sub(r'\s+', ' ', text)
print('After:', text)
