# _*_ coding: utf-8 _*_
import numpy as np
import MeCab
import re
from gensim.models import Word2Vec


_DANMITSU_TEXT = "■絶望に繋がる前に、諦め上手になることが大事――2017年の冬から約1年、毎日の日記をまとめた本書。シリーズとしては5冊目ですね。5年間以上、1日も欠かさず書き続けるのは、ネタ探しという面でもかなり大変じゃないかと思うのですが。壇蜜　その日あったことを本当にそのまま書いているだけですし、1行で終わらせている日もあるのでそれほどは……。むしろ「書きすぎない」というのがいちばん大変かもしれない。場合によっては人に迷惑をかけるので、適度にぼやかしながら読者の皆さんに想像力を駆使していただく、というのがスタイルです。――以前、小説家の桜木紫乃さんとの対談でも「文章を削るのが好きで、原稿を添削するとどんどん短くなっていく」とおっしゃっていました。壇蜜　余計なことを言わないほうがいいのは、日記も私生活も同じだと思っています。でもむずかしい。わかっていても、すぐ余計なこと言っちゃうから。――どうやって戒めているんですか？壇蜜　「少ないようで多いのが無駄」って張り紙を毎日見てます。一人暮らしを始めた頃に薬局でもらってきた標語なんですけど。何のためのもので、薬局の方にもどんな意図があったのかは未だに不明ですが、もう7～8年、自宅のトイレに貼ってあります。それでも失敗してしまったときは「大丈夫、誰も見てなかった、誰もあなたのことを気にしてないよ」って言い聞かせる。――壇蜜さんって、いい意味で諦めるのがお上手ですよね。日記でも「なぜだろう？」と思ったことを追求しすぎないでそのままにしておくじゃないですか。そうか、それでいいんだ、って読んでいて気持ちが楽になりました。壇蜜　そう思っていただけたなら、ありがたいです。今、「諦めない」とか「夢を追いかけよう」とか、前向きな言葉が世の中に溢れすぎてるじゃないですか。でも実際、諦めないでなんとかなるのは、あの監督がいるバスケ部くらいですよ。あの監督がいて、潜在能力のある選手がたくさんいて、強くなれる素養が十二分にある、だから諦めない、というのはわかります。でも私はそうじゃないから。やみくもにただ続けるのは、自分のエナジーが削られるばかりで一つもいいことがない。絶望に繋がる前に諦めることを上手になっておかないと、生きていけなくなっちゃうと思うんです。■あれこれ言ってくる外野には、心の底から幸せを祈るといなくなる――そういう諦め上手な性格はどんなふうに身についたんですか。壇蜜　昔は何でもかんでも掘り下げて考えるタイプだったんです。答えを探し続けて、わからないことは納得するまで人にも聞いて。だけど30歳を過ぎた頃、もういいやって思ったんですよね。突き詰めて、答えを知って、だからなに、って一句できちゃった。どうしてこんなことが起きるんだろうとか、あの人の言葉の真意はなんだったんだろうとか、聞くのも考えるのも疲れるだけだし、自分と関係ないことを考える時間ももったいないから、疑問に思ったというその事実だけ記録しておこう、それでいいや、って思うようになりました。――仕事でもプライベートでも、あれこれ言ってくる外野に対するわずらわしさも日記には書かれていますが、そういう人と相対したときはどうやり過ごすんですか。壇蜜　以前は、なんでそういうこと言うかなあって思ってたけど、今は、じゃあ抱きしめてやろうか、って思います。――斬新ですね（笑）。壇蜜　だって、恵まれている人は他人にとやかく口出ししたり、悪口言ったりしませんから。その人たちがお金をいっぱいもらえて、ほしいものを全部買えて、キャーキャー言われて、望むような幸せを手に入れられるといいなあって祈ります。そうしてニコニコしていると、みんな、本気で気持ち悪いものを見たって顔してどこかに行っちゃうんです。けっきょく、反応させたいんでしょうね。同じ土俵に立たせて同じようにやいのやいの言い合いたい。でもそれじゃ、私が疲れちゃいますから。――いい方法ですね。沸点が低くてすぐに怒っちゃうんで、ちょっと実践してみます。壇蜜　でも、沸点が低いほうが人としては正常な反応だと思いますよ。けっこう、いろんなものを失ってこうなってしまったので……。怒りの感情をちゃんと発散させられないぶん、抑圧されているのか、叫びながら目を覚ますことが時々あります。吐き出せていないものが、内向きの刃となって刺さっているんでしょうね、きっと。■品のいいだらしなさは、生活に宿る――夢はけっこう見るほうですか。壇蜜　見ますね。鰻のように穏やかに、まったく見ずに寝られるときもあるんですけど、見るときはクリアランスセールみたいに次から次へと。日記にも書いた、昔好きだった人のこととか、現実に即したものが多いんですが、夢でしか出会えない人もいます。――同じ夢をくりかえし見るということですか？壇蜜　そう。夢の中の学校で、私は鼓笛隊に入っているんです。同じメンバーでいつも練習していて、夢の中だけのルームメイトもいて……。自分が学生じゃなくなったあともずっと見ている夢なんですけど、時期によって少しずつチャプターが変わるんですよね。夢の中の私も少しずつ成長している。だいたい現実のより少し若くて、今は20代後半くらいかな。――記録して、小説にしたらおもしろそうですね。壇蜜　怖いので、あまり書き留めないようにしているんですよ。それにおもしろくないですよ。ルームメイトがなかなか帰ってこなくて、食堂に青汁を買いに行く夢とかだから。夢の中の私、なぜか青汁が大好きなんですよ。リッターで飲むくらい。だから食堂の人も、氷に差した瓶を常備しておいてくれる。――日記では頻繁に「異常な眠気」についても書かれていますが、こんなに眠くてもいいんだ、と思ったら少しホッとしました。睡眠時間が短くても仕事ができたり、いつもシャキッとしていたりできるのが“ちゃんとした人”のような気がしてしまうので。壇蜜　私も、読者にホッとしていただけたらいいなと思って書いています。自堕落で困ることは確かにいっぱいありますけど、みんながみんな、女性誌の提唱する素敵ライフばかり送っていたらつまらなくないですか。「干物女」とか「ずぼら女子」とか馬鹿にするけど、そこにある魅力を一度でもちゃんと見たことがあるのかい？　そんなに湿ってばっかじゃカビはえるぞ、って思っちゃう。――その、いい意味での自堕落さが、壇蜜さんの色気なんだなとも思いました。掃除をするときはちゃんとスリッパの裏から拭くなど、きちんと生活をしている感がありながら、精神的にはだらしない部分もあるという。壇蜜　掃除、めちゃくちゃちゃんとしますよ。両手にウェッティつけて四つん這いになって、猫が引くくらい部屋中を這いまわります。そのあとに、今度は同じように乾拭きもします。本当の自分はだらしないことを知っているからこそ、だらしなくないように見せるのが大事というか。行儀のいいだらしなさって、生活に宿ると思うんですよね。そのうえで「私はだらしないから」って言えるのが、いちばん強いんじゃないでしょうか。「私はだらしなくありません！」って頑として譲らない人のほうが、つらい気がします。■罪悪感を覚える自分は優しい、と発想を転換する。相手も自分も責めちゃだめ――すべてにおいて「ちゃんとしなきゃ」って思いすぎるのは、つらいですよね。壇蜜　先ほどの諦め上手の話に戻りますが、みんなで同じ100点満点を目指すのではなく、自分の中の70点満点でよしとしてあげられたらいいな、と。6点満点だっていいんですよ。自分の器を理解してあげるのが、いい諦めに繋がるんだと思います。少しずつ自分が変わっていければ、いつかとても楽になるかもしれないし。今の世の中、今すぐ問題解決しようと思いすぎているような気がしていて。明日相手が変わっていてくれないかなとか、自分の気持ちをわかってもらえるんじゃないかとか、ついつい幻を見ちゃうけど、何事もそう簡単に時短では解決しませんよね。――だからこそ時短で解決できることはしたほうがいいんだろうな、と思います。先日、共働きの主婦が料理にレトルトを使うことが手抜きに思えて罪悪感、という記事を見てとても驚いたんですが……。壇蜜　「できれば手作りで」って思うのは優しさの表れですよね。だから、罪悪感を覚えている自分は優しい人間なんだと、気持ちを変換したほうがいいと思います。「ほんとは手作りしてあげたいけどむずかしいから、完全食のレトルトを使ったほうが旦那のためになる。これは優しさだ」って。――そういうふうに、自分も相手も責めない発想に変換できたほうが平和ですね。壇蜜　まあ、共働きなのになんで女にばかり手作りを求めるんだ、って言い分もわからなくはないけれど、男の人なんてみんな、好きな人の作った出汁巻き卵を食べたいものじゃないですか。逆に男の人の文句で「なんでもいいというからラーメン屋に連れて行ったのに不機嫌になった」なんてのもありますけど、それはあなたに甘えてるからだよ？ って思います。猫にだって甘えられたら嬉しいじゃん、彼女に甘えられたら最高じゃん！　って。甘えてもらえない人として自分がセットアップされたら、それはそれで淋しくないですか。お互いに責めたらだめですよ。――壇蜜さんって、誰かと喧嘩することはあるんですか？壇蜜　付き合っている人とは、生涯で一度だけ。渋谷駅の雪崩のような人混みの中、階段で手を繋いでもらえなくて、押しつぶされて死ぬ！ って怒りました。それくらいかな。家事も、やり方が間違っていたら褒めながら直しますね（笑）。あざとい女子に騙されるなとかみんな言うけど、そう言われている女子はみんな幸せそうじゃないですか。引っかかっていたほうが楽しいし、引っかけたほうが楽しい。……と、そんなことを言うと怒られる。ただ、批判するのは簡単だけど、批判されている人たちの行動を見ることも大事かなと思います。――先ほどのずぼら女子の話と同じですね。そこにもまた違う魅力がある。壇蜜　立場チェンジ、って私は言うんですけど、たとえば何かの事件が起きたとき――殺人や強盗などの犯罪は別ですけど、不倫をした、誰かを裏切ったという問題が起きたとき、もし自分が批判される側の立場だったら、と考えるだけで見えてくるものもあって。なぜその問題が誘発されたのだろうと考えると、明日は我が身だなと思って責められなくなります。■生活にひと手間を加えるだけで、自分は簡単に変わっていける――本書ではっとしたのが〈「申し訳ありません」と頭を下げる準備はできている〉という文章で。壇蜜さんは、誰のせいにもしない、自己卑下をしすぎないギリギリのところで自分に責任を持つ方なんだな、と。壇蜜　私はただ「自分こんな奴なんですよ、てへ」って思っているだけですからね。「どうせ自分なんて」って言いすぎちゃう人は、たいてい「そんなことないよ」待ちをしていて、話す相手も疲れちゃう。人に気を遣わせないギリギリの自己評価は、いつでも誰でも身につけることができると思いますよ。――傲慢にならず、フラットに自分に自信を持つためにはどうしたらいいんでしょう。壇蜜　深爪しておくといいですよ。何かいいことがあったとき、わざと深爪をきゅって握ると、ああ調子に乗っちゃいけないなって思う。私自身、根本的には物理的な痛みでどうにかするしかないような人間なので、いつも靴擦れがあったらいいのにと思います。やったあ、褒められた、わーい、いったーい！っていう（笑）。そういうものがあると、世の中のバランスをゆるく見る力が備わると思うので。あとは有頂天になっちゃう日があったら、今から1時間だけは手放しで調子に乗ろう、って時間で区切る。そうすると、ちょっと気が楽になると思います。私はグロ画像を見ますけど。――グロ画像？壇蜜　蛇がウズラを丸呑みするやつとか、ウーパールーパーが次々とメダカを食べていくやつとか……。見ると調子に乗っててすみませんでした！ってなる。 ――荒療治ですね（笑）。そういえば蛇もウーパールーパーも飼ってらっしゃいますよね。壇蜜　ウーパールーパーは死なせちゃいましたけど（※本書参照）、蛇は健在です。いま飼ってるのは猫、蛇、鳥、ナマズ、あとはトカゲのサチコかな。手に負えないものをなんとかするというのも、修行になりますね。蛇なんて、どう考えてもコミュニケーションとれないじゃないですか。朝起きていなくなってたらどうしよう、っていう緊張感も、生活のバランスをとるのにいいかもしれない。生活にひと手間を加えると、けっこう簡単に自分を変えていけるよっていうのは私の言いたいことでもありますね。毎日がつまらないんだったら蛇を飼えばいい。そんな無責任なことを、って言われるかもしれないけど、まずはやってみてよと思います。――壇蜜さん自身、泳げないという個性は消すことにした、とプールに通う日々の描写が日記にありますね。壇蜜　自分のアイデンティティだと思っていたものが、そんなに固執するものでもないなと気づいたとき、わりとなんでもできるようになったんですよ。泳げてもいいし、動物をたくさん飼っていてもいいし、孤独じゃなくてもいい。自分が思っている自分を大事にしすぎると、こうしたほうがいいよと助言や忠告をくれる人に対しても攻撃的になってしまいますからね。――ちなみに2019年、新たに挑戦してみたいことはありますか。壇蜜　そうですね……人間ドックが再検査と言われているので、それをクリアしたいかな。あとは年を追うごとに、身体が無理しているところや意固地になっているところを見せやすくなってしまうので、気をつける。たとえば、白髪をマメに染める。差し歯なので、隙あらばインプラントもしたいですね……って、ガタがきている話ばっかり（笑）。――そういう率直なところが、この日記の魅力でもあると思います。壇蜜　隙が見えた瞬間、その人のことが好ましくなることはありますからね。それが私を居心地よくしようとしての言動だったりするとより救われたような気持ちになる。この本が読者にとって、そういうものであれば嬉しいですね。変わっていないようで変わっている私の日常に触れて、人間は日々変わっていけるんだと思ってもらったり、ずっと同じことをくり返しているように見える人には、変わらなくていいんだとホッとしてもらえたり。それぞれ好きなように読んで、いろんな感じ方をしてもらえたらと思います。あとは最後に伝えることがあるとしたら……古本屋に出すと印税が入ってこないということ。現場からは、以上です（笑）。"


_KUMAKAWATETSUYA_TEXT = "――『完璧という領域』はKバレエ カンパニーを創立されてから現在までの、熊川さんのバレエダンサー、芸術監督、経営者としての胸の内が細やかに語られる、読み応えのある内容です。21年ぶりの本作りはいかがでしたか。熊川哲也氏（以下、熊川）　若かりし頃は何冊か出させていただきましたが、長い間ライブ（舞台）以外で露出するのは踊っている映像くらいで、「活字で本を出す」ということを僕の中でまったく考えていませんでした。お話は何度かいただいていたのですが、本を作るのはまだ早いと思っていましたし、そのとき考えていることを膨らませて話すだけでは内容が薄くなってしまいますし。制作は1年ほど前からスタートして、忘れていることも多かったので、思い出しながらの作業でした。何回も書き直させてもらって制作チームには苦労をかけましたが、20年の軌跡を整理して、あらためて自分をほめたくなりました（笑）。――本を作ることになった一番のきっかけはなんだったのでしょう？熊川　僕のことを16歳の頃から撮影してくださっている、写真家の岡村啓嗣さんというキーパーソンがいらして、その岡村さんとの友好関係から道がひらけた感じです。21年前に出した自伝『メイド・イン・ロンドン』以降の蓄積を、Kバレエ カンパニー創立20周年の節目にまとめられたのはよかったと思います。――「天才・熊川哲也」の内面が、飾らずに語られていますね。熊川　天才という気はまったくなかったんです。ただ運動神経がよかっただけで（笑）。でもそんな自分が英国ロイヤル・バレエ団のプリンシパルになり、語り継ぐべきバレエ界の偉人たちと交流し、天皇皇后両陛下（現上皇ご夫妻）にご臨席いただくことになる（2014年Kバレエ公演『カルメン』）。そんな崇高な世界と関わっていることに対して、本来の自分との間にギャップが生まれていました。熊川　いつもイメージが先行してしまうので、つねに後追いでした。マーケットの中にいる「ダンサー熊川哲也」という芸術家に、個人の「熊川哲也」が追いつくのは大変で。自分の興味も、若い頃はまったく成熟していませんでしたし、若くして物欲のまま欲しいものも買えていると、ダンサーとして成長しないと思いつつ、ますます芸術論から離れていってしまう傾向がありました。そういうことは自然に追いついていくものと実感したのは、最近ですね。古典芸術の偉大さや先人へのリスペクトが胸に刻まれて、その時代に触れるための古書や骨董の蒐集が趣味になって。やっと、追いついたかなと思います。組織を立ち上げて会社を経営するようになってからは、グレーゾーンも必要だし、忖度も大事だし、そうして大人になってきた部分もありました。――本の中で、苦悩されていた時期のことなども隠さず明かされています。熊川　僕はずっと、意外と正直に生きてきているんです（笑）。20代の頃は、口が災いの元になったことも多くありました。正直者は馬鹿を見る、というのも経験しています。　Kバレエを立ち上げたときは、派手な活動に見えたり、自分の言動が大きなものだったりすると、出過ぎたものに蓋をするように、少し距離をおくというか、いわゆるアンチといわれる存在もいました。当時は見たい人が見るSNSではなく新聞に出て、みんなにさらけ出されてしまう時代でしたが、それでもずっと、自分に正直にやってきた。この本も、バレエのすばらしさだけでなく、苦悩や苦言、厳しかったことも、嘘偽りなく語りました――熊川さんの正直な言葉が、21年ぶりに本にまとまったのは意義深いことだと思います。熊川　僕が先人たちの本に学んできたように、次の世代に残すつもりで作りましたし、事実と時系列に間違いがないようにして、自分のディクショナリという位置づけの本にもしたいと考えていました。　言い回しなどは制作チームにも多少助言をもらいましたが、すべて自分の言葉です。完成までに、10回くらい読みました。普通ここまで読むだろうか？と思いながらも、最終的に（笑）。――10回……！　それはすごいですね。熊川　出し尽くしました（笑）。――近年、特に日本の男性バレエダンサーの層が厚くなったのは、確実に熊川さんの存在がありますよね。熊川　男性は親やお姉さんの影響でバレエを始める人が多いので、まずお母さま世代が僕のファンになってくれたことが大きいと思います。男の子が生まれて、DVDを何度も見せて……きっかけはそういう感じではないでしょうか。もうKバレエにも、ご両親が僕と同い年というダンサーがいます。2003年に若手ダンサーの育成を目的にKバレエスクールを設立して、生徒ともいろいろ関わっていますが、バレエをやっている子供たちは純粋で、悪い子はいません。接していると心が洗われる気がします。ただ、人間の育成は簡単ではないので、スクールの経営からは、僕も多くのことを学んでいます。――ダンサー、芸術監督、経営者の3つを並行して成功させ続けている例は、世界的に見ても熊川さんしかいないのではないでしょうか。『完璧という領域』ではすべての要素について、真摯に語られていますね。熊川　ダンサーとしてのキャリア、芸術監督として完璧を目指す姿勢、そして、経営者としてのビジネスの話も、その厳しさや駆け引きも含めて、詳しく書いています。Kバレエ カンパニーはバレエ団として日本で唯一の株式会社で、芸術を追求しながら、ビジネスとしても運営を成立させているんです。国からの助成金を受けずに、クオリティを保った内容の公演を年間50回以上コンスタントに続けるビジネスモデルを確立し、ダンサーやスタッフの生活を保証し、ダンサーがプロとして場数を経験できる環境を実現してきたことは、この20年で日本のバレエ界の旧態依然の環境が大きく変化するきっかけになっていると思います。Kバレエを立ち上げたとき、「プロのダンサーを育てたい」と語っていたのですが、ほかのバレエ団との切磋琢磨もあり、「生徒」ばかりだった日本に、「プロ」意識を持ったダンサーが増えたことは最大の変化だと感じています。――本のタイトルがまさに熊川さんを表していますね。熊川　タイトル選びは悩みました。僕が話した内容からピックアップして候補を出してもらい、これしかないとパシン！ と来たのが『完璧という領域』でした。もともとは、2017年に世界初演した完全オリジナル新作『クレオパトラ』の記者会見で語った言葉です。「完璧とはどういうものかを皆さんにお見せしたい」というのが『クレオパトラ』への僕の意気込みだった。完璧なんてものはないとみんな言うけれど、いや自分の中にはあるんだと。いくら言葉で宣伝しても、買っていただくことは簡単なことではありません。だから、興味がない人は興味がなくてもいい。ただ、このタイトルが響く人には、ぜひ中身を読んでほしいと思います。――「完璧という領域」は、すべてに通じるものの考え方ですよね。響く人には、しっかりと響くと思います。熊川　この本を出したことで、それは僕にとって非常にハードルが高い、今後の生活のテーマにもなりました。ポリシーとしてその思いはずっとあったけれど、言葉としては『クレオパトラ』の制作から出てきたものが、人生や熊川哲也の新しいテーマになってしまった。これからはもうすべてにおいて完璧を目指さなくてはいけなくなりました（笑）。でも楽しみです。うん、非常に楽しみですね。――今は秋に控えているKバレエの2つの新作公演の準備中ですよね。若手ながら世界的指揮者であるバッティストーニと共演する『カルミナ・ブラーナ』と、プッチーニの名作オペラ『蝶々夫人』を原案とした『マダム・バタフライ』。どちらも大作です。オリジナルの全幕新作バレエを作り続けていらっしゃることも、日本ではめずらしいことです。熊川　新作を作り、レパートリーを蓄えていくことは、バレエ団の財産です。そして、なにもないところから作品の創造をすることは100％自分の愛する世界を作り上げることでもあります。大がかりな作品が2本並行していますが、完成まで死力を尽くすだけです。"

_YAZAWAEIKICHI_TEXT = "－－09年のアルバム『ROCK'N'ROLL』から、10年の『TWIST』、そして今作『Last Song』と、僕は勝手に三部作と捉えているのですが、やっぱり今作のタイトルには驚きました。矢沢永吉：もう40周年ですからね。武道館だって117回、現役最多で走ってる。アルバムだってどれくらい出しただろうっていうくらい、いっぱい出しましたよ。早くから海の向こうへ行って、世界的な連中とも色んなことをやりました。その走りと言っても過言ではないくらい色々とやってきたでしょ？それにぼんぼんレコードを出せばいいってもんではない時代になってきた。それらが全部ひとつになってきた時に、けっこう良い意味で肩の力が抜けてきたんですよ。それに元々、11番目のバラードに『LAST SONG』っていうタイトルがありましたからね。それでアルバムタイトルどうしようか？ って思った時に、「これ最高じゃない！ LAST SONG、やっちゃおう！」。そのくらい軽い感じでポンッとタイトルにしちゃいました。－－とはいえ意味深なタイトルではありますよね。矢沢永吉：もうひとつは事実、「これが最後になるなら、最後になってもいいんじゃない？」ぐらいの気持ちが無かった訳でもない。スタジオワーク、疲れるし（笑）。本当に。だってボクのやり方というのは『ROCK'N'ROLL』から既に始まっていたことですけど、作るのは1か月あるかないかで出来てるんです、アルバムの録りは。でも、後3か月くらいずっと聴いてるのね。聴いて直して聴いて直して、イジってイジってイジって……。聴くことに飽きるくらい聴いてる。そういうことをひっくるめて、白盤（サンプル盤）、いつ頃にもらいました？－－1か月前くらいですね。矢沢永吉：1か月前と今は全然音が違いますよ。もっとストーンッとキます。今の最新のヤツを聴いたら、「こんなに直球でくるワケ？」って。もっと分かりやすい！ もっと聴きやすい！ もっとストーンッと曲に入れる。矢沢永吉：それでさっきの話に戻りますけど、アルバム制作、たぶんボクは止めないだろうね。ボクは貪欲だから、また1年くらい時間が経ったら、「さーてそろそろ作ろうかなー」って思うんじゃないですか？ ステージと一緒ですよ。武道館の最終日になったら、「もうやらねえぞライブは！」って言ってるんですよ。ファイナルの時、アンコールが「ワーーーーーー！」と終わって「サンキュー！」、楽屋に帰ってシャワー浴びて、好きな酒グワァーーーーって、その夜はドライマティーニ呑んでベロンベロンになって、どうやってベッドに入ったのか覚えてない（笑）。それで年が明けてからは、もう丸っきり音楽家じゃないからね。ただの呑んべぇのオッサンで1月が過ぎて、2月3月4月になってくると……、もうライブがしたいんだよ！ そして、またシーズンがきてガーンとやっちゃう。それを繰り返して40年になるんです。でもね！ ひとつだけ違うのは、今までこんな気持ちにはならなかった……、『ROCK'N'ROLL』の後も『TWIST』の後も。こういう心境になったのは何故かと思ったら、……もう40年も経ち、「我、ロック人生、悔い無し」みたいな所もあるんじゃないですか？－－なるほど。矢沢永吉：俺は音楽を、ステージを止めるか？ 40年もやればそんな自問自答もするじゃないですか。でも、たぶん止めない。何故止めないか。ミック・ジャガーも含めた世界の連中たちが止めないように、止めないだろうね。……たぶんね、止めれない。だって、ライブやってないとボクらって何処か不完全な所があるよね。ライブやってないとダメになっちゃいそうだもん。ステージをやるって目標ができれば、やっぱり身体を鍛えなきゃいけないし、自ずからボイストレーニングをやるし、食べるものも意識する。ブルース・スプリングスティーンもまた大々的にツアーをやってるみたいだけど、成功はとっくの昔にしてるじゃない？ だからそういうのではやってないよね。死ぬ訳にはいかないからやるんじゃない？ ボクもこれくらいの歳になって、やっと「分かるよな～」って所にきてますね。そのうち「もう無理だ！」という時がくるんだろうけど、それまでは。その歳、その歳に合うようなスタイルを取り入れながら、やり続けるんだろうなって思いますね。"

_JOHNNYS_TEXT = "ジャニーズ事務所の創業者、ジャニー喜多川さんが7月9日、くも膜下出血で死去した。87歳だった。筆者は朝日新聞で演劇記者をしていた時代に、一度だけ直接インタビューする機会に恵まれた。取材したのは、2011年9月。「最も多くのナンバーワン・シングルをプロデュースした」「最も多くのコンサートをプロデュースした」として、ギネス・ワールド・レコーズに認定された時のことだ。一代にして「ジャニーズ帝国」を築き上げた芸能界の立志伝中の人物だけに緊張したが、帝国劇場の貴賓室に姿を現したジャニーさんは、好々爺然として物腰柔らかだったppp。【BuzzFeed Japan / 神庭亮介】ジャニー喜多川さんが生前に語った言葉「SMAPの中居くんは…」ミュージカルの本場、ニューヨークのブロードウェイ「ブロードウェイに負けたくない」2時間に及んだ取材のうち、多くが割かれたのが演劇を中心とするショービジネスについてだった。「アメリカのブロードウェイなんかに負けたくない」と繰り返し、舞台へかける思いを饒舌に語った。ジャニーズの舞台は本物の水を使ったり、俳優が自在に宙を舞ったりとラスベガス風のダイナミックな演出で知られる。「客席がいかに楽しんでいるかをまず見る。客席半分とステージ半分。ステージより客席の方が大切なわけですよ」「たとえば『滝沢歌舞伎』だったら、ご年配のお客さんが身を乗り出して見ていたりする。共鳴がなかったら、お客さんはついてきません」滅多にインタビューを受けず、表舞台に出ることを嫌ったジャニーさん。テレビ担当や音楽担当ではなく、演劇記者の取材を受けたのは、「舞台人」「演劇人」として正当に評価されることを望んでいたからかもしれない。美空ひばりの通訳を任され…父親は真言宗米国別院の僧侶。米ロサンゼルスで育ち、幼いころからミュージカルやショーを浴びるように見てきた。10代のころ、訪米した服部良一や美空ひばりらの通訳を任された。ブロマイド写真をつくると非常によく売れ、収益はすべてタレント本人に渡した。子どもながらに、大人たちから信頼されることに喜びを感じたという。そんな体験が、芸能界を目指す原点となった。"

_HAYABUSA_TEXT = "津田さんは成功の背景について、「チームワーク以外のなにものでもない。メンバー一人一人が大切な役割を全うした。度を超えたともいえる自己批判能力を発揮し、意地悪な想定を積み重ね、実現を引き寄せた。その結果、本番では本当に何もなく、心配がうそのようにうまくいった」と分析した。はやぶさ2がリュウグウへ着陸後に上昇しながら撮影した画像も公開された。はやぶさ2の下に大量のリュウグウの破片が舞う様子が写っていた。はやぶさ2の科学分析のとりまとめを担当する渡辺誠一郎・名古屋大教授は「目標としていた場所と1メートル前後の誤差で、かなりの高い精度で着陸できたのではないか」と説明した。さらに、渡辺さんは、画像に写っていた破片について「1回目の着陸でも破片が多く写っていたが、少し違って見える。1回目よりも明るく、細かいような印象だ。上空からの観測では、リュウグウはどこも一様な性質なのではないかと考えられていたが、このような小さな天体でもバラエティーに富んでいることが分かった。これこそ着陸を2回実施した意味だと思う」と話した。着陸した瞬間に採取装置先端を撮影した画像にも、多くの破片が飛び散っている様子が写っており、「これも1回目よりも多く、興味深い」（渡辺さん）という。津田さんは「はやぶさ2は、私たちにとっては管制室のメンバーの一員。本当によくやったと言いたい。リュウグウにも『牙をむいた』などと言ったが、試料を手渡してくれた。せっかく渡してくれたので大事に扱い、大事に分析したい。リュウグウにはあと半年ほど滞在するので、残りの時間を一日たりとも無駄にしないように運用していく」と話した。JAXAによると、はやぶさ2は正常に飛行しており、既に試料が入った容器のふたを閉める作業を実施したという。はやぶさ2は2020年冬に地球へ帰還する。"

_ANDROID_TEXT = "Android：手書きメモアプリが使えないのは過去の話になったかも。「手書きメモアプリ」と聞くだけで、筆者は敬遠するところがありました。今までいくつかのアプリを試してきて、うまく文字が書けたり、正しく反映されたためしがなかったのです。大人しくキーボードから入力するメモが一番だ、と。ですが、今回紹介する『DioNote』は、手書き反映の機敏さといい、認識力の高さといい、かなりの実力を持っていて、久々に「いいね！」と言いたくなるアプリでした。加えて、画像の挿入や文字入力、メモのショートカットをホームに置けるなど、細かな機能も実装されており、あらゆる点からなかなか使える仕上がりとなっています。早速、トップ画面右上のプラスマークからメモを作ってみます。ノートのようなデザインです。画面下部の領域に文字を手書きで入力していきます。一文字書いてみると、反応の正確さにビックリします。すぐさま一文字書いたことが認識され、新たな文字、さらに新たな文字...と、そのテンポの良さも素晴らしい。ちなみに、一文字ずつだけでなく、横に連続で書いていくことも可能です。画面右上のメニューから「キャンパス作成」をタップすると、真っさらな自由帳のような画面になります。ここでは画像の貼り付けも自由にでき、より気ままなメモを作成できます"

_ABESHINZO_TEXT = "企業業績が上向き、景気拡大局面が続いています。ただ日本発のイノベーション（技術革新）の停滞や人手不足など成長阻害要因も顕在化しています。6月にまとめる新成長戦略ではどのような政策を柱に据えますか。安倍首相：働きたい人が働けるという状況を作っていく。雇用を作り、収入が増える環境を作っていく。それが政府に課せられた使命だと思っています。この2年間で正規雇用が約80万人増え、すべての都道府県で有効求人倍率が1倍を超えました。労働市場がタイトになり、今年3月の完全失業率は2.8％。需給を反映し、賃金がこれから上がりやすくなる状況になってきたと言えます。「ソサエティー5.0」の実現へ一方で、人手不足は経済成長の足かせになりつつあります。そこで、AI（人工知能）やあらゆるモノがネットにつながるIoT、ビッグデータを活用して少子高齢化を乗り越える構想『ソサエティー5.0』を実現していきたいと考えています。例えば、医療や介護でデータを活用して、予防や健康管理に軸足を移していきたい。またオンライン診療などの遠隔医療について、2018年度の診療報酬改定でしっかり評価していく考えです。人手不足の解消につながる介護ロボットや見守りセンサーの導入も介護報酬や人員配置基準で後押ししていくつもりです。イノベーションに力を入れ、AIなどの活用を進めていく中で生産性を上げていきます。それによって人手不足を上回る成長を実現していきたい。例えば自動走行については17年度から公道での実証を本格化します。トラックの無人隊列走行は20年代前半の事業化を目標にし、人手不足による物流危機の克服を目指します。憲法改正に向け20年という施行目標や9条の1項、2項を維持した上で自衛隊に関する規定を加える方針を表明されました。この時期に提案した狙いを説明してください。安倍首相：憲法の施行から70年になりますが、この間に世界の情勢も人々の暮らしも社会のあり方も大きく変わりました。国民主権、基本的人権の尊重、平和主義は普遍的なもので、これを変えることはない。ただ憲法は国の未来や理想の姿を語るものであり、我が国でも必要な改正を行うことは当然のことと考えています。"


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
    test_text = _YAZAWAEIKICHI_TEXT
    sv = SemanticVolume()
    sv.execute(test_text, 300)

    print('################ original text ################')
    print(test_text)
    print('################ summarize ################')
    for s in sv.summarized_sentence:
        print(s)
    
if __name__ == '__main__':
    main()




