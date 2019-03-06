import re
import unicodedata

text = '	ＣＬＥＡＮＳ ing  によりﾃｷｽﾄﾃﾞｰﾀを変換すると　トラブルが少なくなります。'
print("Before:", text)

text = unicodedata.normalize('NFKC', text)
text = re.sub(r'\s+', '', text)
print("After:", text)