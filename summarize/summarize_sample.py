# _*_ coding: utf-8 _*_
import numpy as np
import MeCab
import re
from gensim.models import Word2Vec


class SemanticVolume:
    def __init__(self):
        self.available_pos = ['名詞', '動詞-自立', '形容詞']
        self.not_available_pos = ['名詞-数']
        self.tokenizer = MeCab.Tagger("-Ochasen")

        self.model_name = "word2vec.gensim.model"
        self.model = Word2Vec.load(self.model_name)
        self.features = self.model.vector_size

        self.original_sentence = []
        self.summarized_sentence = []

    def make_wakati(self, sentence):
        result = []
        chasen_result = self.tokenizer.parse(sentence)
        for line in chasen_result.split('\n'):
            elems = line.split('\t')
            if len(elems) < 4:
                continue
            word = elems[0]
            pos = elems[3]
            if True in [pos.startswith(w) for w in self.not_available_pos]:
                continue
            if True in [pos.startswith(w) for w in self.available_pos]:
                result.append(word)

        return result

    def wordvec2docmentvec(self, sentence):
        docvecs = np.zeros(self.features, dtype='float32')
        denominator = len(sentence)
        for word in sentence:
            try:
                temp = self.model[word]
            except:
                denominator -= 1
                continue
            docvecs += temp

        if denominator > 0:
            docvecs = docvecs /denominator

        return docvecs

    def compute_centroid(self, vector_space):
        centroid = np.zeros(self.features, dtype='float32')
        for vec in vector_space:
            centroid += vec

        centroid /= len(vector_space)

        return centroid

    def projection(self, u, b):
        return np.dot(u, b) * b

    def basis_vector(self, v):
        return v / np.linalg.norm(v)

    def span_distance(self, v, span_space):
        proj = np.zeros(self.features, dtype="float32")
        for span_vec in span_space:
            proj += self.projection(v, span_vec)

        return np.linalg.norm(v - proj)

    def compute_farthest_spanspace(self, sentences_vector, span_subspace, skip_keys):
        all_distance = [self.span_distance(vec, span_subspace) for vec in sentences_vector]
        for i in skip_keys:
            all_distance[i] = 0
        farthest_key = all_distance.index(max(all_distance))

        return farthest_key

    def execute(self, input_document, summary_length):
        corpus_vec = []
        sentences = []
        self.summarized_sentence = []
        sentences = input_document.split('。')

        for sent in sentences:
            self.original_sentence.append(sent)
            wakati = self.make_wakati(sent)
            docvec = self.wordvec2docmentvec(wakati)
            corpus_vec.append(docvec)

        summarize_indexes = []
        centroid = self.compute_centroid(corpus_vec)

        abc = [np.linalg.norm(centroid - vec) for vec in corpus_vec]
        first_summarize_index = abc.index(max(abc))
        summarize_indexes.append(first_summarize_index)

        adfss = [np.linalg.norm(corpus_vec[first_summarize_index] - vec) for vec in corpus_vec]
        second_summarize_index = adfss.index(max(adfss))
        summarize_indexes.append(second_summarize_index)

        total_length = len(self.original_sentence[first_summarize_index]) + len(self.original_sentence[second_summarize_index])
        first_basis_vector = self.basis_vector(corpus_vec[second_summarize_index])
        span_subspace = [first_basis_vector]

        while True:
            farthest_index = self.compute_farthest_spanspace(corpus_vec, span_subspace, summarize_indexes)
            if total_length + len(self.original_sentence[farthest_index]) < summary_length:
                span_subspace.append(corpus_vec[farthest_index])
                total_length += len(self.original_sentence[farthest_index])
                summarize_indexes.append(farthest_index)
            else:
                break

        summarize_indexes.sort()
        for idx in summarize_indexes:
            self.summarized_sentence.append(sentences[idx])

        return


def main():
    test_title = "真に「使える」手書きメモアプリだと思わせてくれた『DioNote』"
    test_text = "ジャニーズ事務所の創業者、ジャニー喜多川さんが7月9日、くも膜下出血で死去した。87歳だった。筆者は朝日新聞で演劇記者をしていた時代に、一度だけ直接インタビューする機会に恵まれた。取材したのは、2011年9月。「最も多くのナンバーワン・シングルをプロデュースした」「最も多くのコンサートをプロデュースした」として、ギネス・ワールド・レコーズに認定された時のことだ。一代にして「ジャニーズ帝国」を築き上げた芸能界の立志伝中の人物だけに緊張したが、帝国劇場の貴賓室に姿を現したジャニーさんは、好々爺然として物腰柔らかだった。【BuzzFeed Japan / 神庭亮介】ジャニー喜多川さんが生前に語った言葉「SMAPの中居くんは…」ミュージカルの本場、ニューヨークのブロードウェイ「ブロードウェイに負けたくない」2時間に及んだ取材のうち、多くが割かれたのが演劇を中心とするショービジネスについてだった。「アメリカのブロードウェイなんかに負けたくない」と繰り返し、舞台へかける思いを饒舌に語った。ジャニーズの舞台は本物の水を使ったり、俳優が自在に宙を舞ったりとラスベガス風のダイナミックな演出で知られる。「客席がいかに楽しんでいるかをまず見る。客席半分とステージ半分。ステージより客席の方が大切なわけですよ」「たとえば『滝沢歌舞伎』だったら、ご年配のお客さんが身を乗り出して見ていたりする。共鳴がなかったら、お客さんはついてきません」滅多にインタビューを受けず、表舞台に出ることを嫌ったジャニーさん。テレビ担当や音楽担当ではなく、演劇記者の取材を受けたのは、「舞台人」「演劇人」として正当に評価されることを望んでいたからかもしれない。美空ひばりの通訳を任され…父親は真言宗米国別院の僧侶。米ロサンゼルスで育ち、幼いころからミュージカルやショーを浴びるように見てきた。10代のころ、訪米した服部良一や美空ひばりらの通訳を任された。ブロマイド写真をつくると非常によく売れ、収益はすべてタレント本人に渡した。子どもながらに、大人たちから信頼されることに喜びを感じたという。そんな体験が、芸能界を目指す原点となった。"
    print(test_title)
    print(test_text)

    sv = SemanticVolume()
    sv.execute(test_text, 200)

    print('################ original text ################')
    print(test_text)
    print('################ summarize ################')
    for s in sv.summarized_sentence:
        print(s)
    
if __name__ == '__main__':
    main()



    "Android：手書きメモアプリが使えないのは過去の話になったかも。「手書きメモアプリ」と聞くだけで、筆者は敬遠するところがありました。今までいくつかのアプリを試してきて、うまく文字が書けたり、正しく反映されたためしがなかったのです。大人しくキーボードから入力するメモが一番だ、と。ですが、今回紹介する『DioNote』は、手書き反映の機敏さといい、認識力の高さといい、かなりの実力を持っていて、久々に「いいね！」と言いたくなるアプリでした。加えて、画像の挿入や文字入力、メモのショートカットをホームに置けるなど、細かな機能も実装されており、あらゆる点からなかなか使える仕上がりとなっています。早速、トップ画面右上のプラスマークからメモを作ってみます。ノートのようなデザインです。画面下部の領域に文字を手書きで入力していきます。一文字書いてみると、反応の正確さにビックリします。すぐさま一文字書いたことが認識され、新たな文字、さらに新たな文字...と、そのテンポの良さも素晴らしい。ちなみに、一文字ずつだけでなく、横に連続で書いていくことも可能です。画面右上のメニューから「キャンパス作成」をタップすると、真っさらな自由帳のような画面になります。ここでは画像の貼り付けも自由にでき、より気ままなメモを作成できます。"
