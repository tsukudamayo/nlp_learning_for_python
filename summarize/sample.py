from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenizer import Tokenizer as JanomeTokenizer  # sumyのTokenizerと名前が被るため
from janome.tokenfilter import POSKeepFilter, ExtractAttributeFilter

text = """多くの会社（店）で営業マンに日報を書かせていることと思います。ですが、何のために日報を書かせているのか、もう一度確認してください。営業マンは社外にいる時間が多く、その行動を把握することはできません。そこで営業マンの行動を把握するために、１日の行動記録を日報にして提出させる場合が多いようですが、日報というのは行動記録を書くことなのでしょうか。そして、営業マンに行動記録をかかせることに、どれだけの意味があるのでしょう。例えば、毎日10件の顧客を訪問している営業マンと、毎日５件訪問している営業マンでは、どちらが評価できるでしょうか。きっと、多くのマネジャーが「もちろん10件の顧客を訪問している営業マンに決まっている」と答えるでしょう。しかし、訪問件数を多くすることだけを考え、準備もそこそこに、休む間もなく得意先を回っているかもしれません。
営業マンにとって問題意識をもつことは基本です。"""

# 1行1文となっているため、改行コードで分離
sentences = [t for t in text.split('\n')]
for i in range(2):
    print(sentences[i])
# 転職 Advent Calendar 2016 - Qiitaの14日目となります。 少しポエムも含みます。
# 今年11月にSIerからWebサービスの会社へ転職しました。

# 形態素解析器を作る
analyzer = Analyzer(
    [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(r'[(\)「」、。]', ' ')],  # ()「」、。は全てスペースに置き換える
    JanomeTokenizer(),
    [POSKeepFilter(['名詞', '形容詞', '副詞', '動詞']), ExtractAttributeFilter('base_form')]  # 名詞・形容詞・副詞・動詞の原型のみ
)

# 抽出された単語をスペースで連結
# 末尾の'。'は、この後使うtinysegmenterで文として分離させるため。
corpus = [' '.join(analyzer.analyze(s)) + '。' for s in sentences]
for i in range(2):
    print(corpus[i])
# 転職 Advent Calendar 2016 - Qiita 14 日 目 なる 少し ポエム 含む。
# 今年 11 月 SIer Web サービス 会社 転職 する


from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# 連結したcorpusを再度tinysegmenterでトークナイズさせる
parser = PlaintextParser.from_string(''.join(corpus), Tokenizer('japanese'))

# LexRankで要約を2文抽出
summarizer = LexRankSummarizer()
summarizer.stop_words = [' ']  # スペースも1単語として認識されるため、ストップワードにすることで除外する

summary = summarizer(document=parser.document, sentences_count=2)

# 元の文を表示
for sentence in summary:
    print(sentence)
    print(sentences[corpus.index(sentence.__str__())])


print('summary')
print(summary)
