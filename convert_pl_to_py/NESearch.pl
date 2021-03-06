#! /usr/bin/perl

# タグの推定結果を計算する

# 入力: kytea -out confの結果
# 出力: BIOタグ推定コーパス

# BIO形式は tag-B,tag-I,O

$rsltfile = $ARGV[0];
$rsltfile2 = $ARGV[1];

# for recipe: 8
my @TYPE = qw( Ac Af F Sf St Q D T ); 

# # for shogi: 23
# my @TYPE = qw( Hu Tu Po Pi Ps Mc Pa Pq Re Ph Ai St Ca Ce Me Mn Ee Ev Ti Ac Ap Ao Ot );

# Other tag: 1
my $OTYPE = "O";

my @tagkinds = ();
my @head_tag = ();
@connect_matrix = ();

for my $i (0..$#TYPE) {
    push(@tagkinds, "$TYPE[$i]-B");
    push(@head_tag, "1");
    push(@tagkinds, "$TYPE[$i]-I");
    push(@head_tag, "0");
}

push(@tagkinds, $OTYPE);
push(@head_tag, "1");

my $size = scalar(@tagkinds);

# 接続可能マトリックス: 
# B,O -> あらゆるタグから接続可, I -> 同じ種類のタグ以外からは接続不可
for my $i (0..$#tagkinds) {
    printf("i %s\n", $i);
    my @l;
    if ($tagkinds[$i] =~ /^(.+?)-I$/) {
    printf("tagkinds %s\n", $tagkinds[$i]);
	$tag = $1; # $0はNESearch.plになる $1はマッチしたタグ名
	for my $j (0..$#tagkinds) {
        printf("j %s\n", $tagkinds[$j]);
	    if ($tagkinds[$j] =~ /$tag/) {
		push(@l, "1");
	    }
	    else {
		push(@l, "0");
	    }
	}
    }
    else {
	@l = ("1") x scalar(@tagkinds);
    }
    push(@connect_matrix, \@l);
    printf("llllll %s\n", @l);
}

#printf("connect_matrix %s", @connect_matrix)

#@org_tagkinds = ("Ac-B", "Ac-I", "Af-B", "Af-I", "F-B", "F-I", "Sf-B", "Sf-I", "St-B", "St-I", "Q-B", "Q-I", "D-B", "D-I", "T-B", "T-I", "O");
#                                         文頭に来ることのできるタグ
#             AC-B, AC-I, AF-B, AF-I, F-B, F-I,Sf-B,Sf-I,St-B,St-I,Q-B, Q-I, D-B, D-I, T-B, T-I, O
#@org_head_tag = (    1,    0,    1,    0,   1,   0,   1,   0,   1,   0,  1,   0,   1,   0,   1,   0, 1);

# #                                         接続可能マトリックス
# #                    Ac-B, Ac-I, Af-B, Af-I, F-B, F-I,Sf-B,Sf-I,St-B,St-I, Q-B, Q-I, D-B, D-I, T-B, T-I, O
# @org_connect_matrix = ([    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # Ac-B
#                    [    1,    1,    0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 0 ], # Ac-I
#                    [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # Af-B
#                    [    0,    0,    1,    1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 0 ], # Af-I
#                    [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # F-B
#                    [    0,    0,    0,    0,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 0 ], # F-I
#                    [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # Sf-B
#                    [    0,    0,    0,    0,   0,   0,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0, 0 ], # Sf-I
#                    [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # St-B
#                    [    0,    0,    0,    0,   0,   0,   0,   0,   1,   1,   0,   0,   0,   0,   0,   0, 0 ], # St-I
#                    [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # Q-B
#                    [    0,    0,    0,    0,   0,   0,   0,   0,   0,   0,   1,   1,   0,   0,   0,   0, 0 ], # Q-I
#                    [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # D-B
#                    [    0,    0,    0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   0,   0, 0 ], # D-I
#                    [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # T-B
#                    [    0,    0,    0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1, 0 ], # T-I
#                    [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ]);# O

open RFILE, $rsltfile;  # kyteaによるタグ推定確率
open RFILE2, ">$rsltfile2"; # このプログラムによるタグ推定結果

# $totalwordnum = 0;
# $totaltruenum = 0;

while(<RFILE>){
################# kyteaによるタグ推定結果を獲得 #######################
	$line = $_;
	chomp($line);
	@words = split(/ /, $line);
	$wordn = 0;
	foreach $word (@words){
        # printf("word %s\n", $word);
		@buf = split(/\//, $word);
		$wordcont[$wordn] = $buf[0];
		@bufs2 = split(/\&/, $buf[1]);
        printf("wordn %s\n", $wordn);
        printf("wordcont %s\n", $wordcont[$wordn]);
		$tagn = 0;
		foreach $buf2 (@bufs2){
            # printf("buf2 %s\n", $buf2);
			$tags[$wordn][$tagn] = $buf2;
			$tagn++;
		}
		$wordn++;
	}
	
	<RFILE>;
	
	$line = <RFILE>;
	chomp($line);
	@bufs = split(/ /, $line);
	$wordn2 = 0;
	foreach $buf (@bufs){
        # printf("buf %s\n", $buf);
		@probs = split(/\&/, $buf);
		$probn = 0;
		foreach $prob (@probs){
            # printf("prob %s\n", $prob);
            printf("wordn2 %s\n", $wordn2);
            # printf("probn %s\n", $probn);
			$rsltprob[$wordn2]{$tags[$wordn2][$probn]} = $prob;
			printf("$probn %s %s %.2f\n", $tags[$wordn2][$probn], $wordcont[$wordn2], $rsltprob[$wordn2]{$tags[$wordn2][$probn]});
			$probn++;
		}
		$wordn2++;
	}
	<RFILE>;

################# Viterbi algorithmによる最適解の決定 #######################
	@prob = 0;
	
	for($jj=0; $jj<$size; $jj++){
        printf("jj %s\n", $jj);
		$edge[0][$jj] = 0;
		$prob[0][$jj] = $head_tag[$jj]*$rsltprob[0]{$tagkinds[$jj]};
        # printf("prob[0][jj] %s\n", $prob[0][$jj]);
		printf("$tagkinds[$jj] $head_tag[$jj] $rsltprob[0]{$tagkinds[$jj]} $prob[0][$jj]\n");
	}

	for($ii=1; $ii<$wordn; $ii++){ # 現在注目している単語
		for($jj=0; $jj<$size; $jj++){ # 現在注目している単語がもしこのタグだったら
            # printf("ii %s\n", $ii);
            # printf("jj %s\n", $jj);
			# $tagkinds[$jj]: 現在の単語のタグ
			# $rsltprob[$ii]{$tagkinds[$jj]}: 現在の単語がこのタグである確率
			$edge[$ii][$jj] = 0;
			$prob[$ii][$jj] = 0;
			for($kk=0; $kk<$size; $kk++){ # 1つ前の単語のタグがもしこのタグだったら
				# $tagkinds[$kk]: 1つ前の単語のタグ
				# $prob[$ii-1][$kk]: 1つ前の単語がこのタグである確率
				
				# 現在のタグのコスト
                # printf("kk %s\n", $kk);
				$tmpprob[$kk] = $prob[$ii-1][$kk] # 1つ前のタグが$kkだった確率
								* $connect_matrix[$jj][$kk] # 1つ前のタグと現在のタグがつながる確率
								* $rsltprob[$ii]{$tagkinds[$jj]}; # 現在のタグが子のタグである確率
                # printf("cost\n");
				# printf("$prob[$ii-1][$kk]/$connect_matrix[$jj][$kk]/$rsltprob[$ii]{$tagkinds[$jj]}/$tmpprob[$kk]\n");
                #printf("prob[ii][jj] %s\n", $prob[$ii][$jj]);
                printf("tmpprob[kk] %s\n", $tmpprob[$kk]);
				if ($prob[$ii][$jj] < $tmpprob[$kk]){
					$edge[$ii][$jj] = $kk;
					$prob[$ii][$jj] = $tmpprob[$kk];
				}
			}
		}
	}
	
	# 最後のノードで確率最大のタグを選択
	$maxprob = 0;
	$finaltag = 0;
	for($jj=0; $jj<$size; $jj++){
		if($maxprob < $prob[$wordn-1][$jj]){
			$maxprob = $prob[$wordn-1][$jj];
			$finaltag = $jj;
		}
	}

	# 後ろからバックトレース
#	printf("$wordcont[$wordn-1]: $tagkinds[$finaltag]->$tagkinds[$edge[$wodn-1][$finaltag]]\n");
	$rslttag[$wordn-1] = $finaltag;
	for($ii=$wordn-2; $ii>=0; $ii--){
		$rslttag[$ii] = $edge[$ii+1][$rslttag[$ii+1]];
	}

	# 結果の出力
	for($ii=0; $ii<$wordn; $ii++){
		printf(RFILE2 "%s/%s ", $wordcont[$ii], $tagkinds[$rslttag[$ii]]);
	}
	printf(RFILE2 "\n");
}
close RFILE;
close RFILE2;

