#! /usr/bin/perl

# タグの推定結果を計算する

$rsltfile = $ARGV[0];
$rsltfile2 = $ARGV[1];

@tagkinds = ("Ac-B", "Ac-I", "Af-B", "Af-I", "F-B", "F-I", "Sf-B", "Sf-I", "St-B", "St-I", "Q-B", "Q-I", "D-B", "D-I", "T-B", "T-I", "O");

#                                         文頭に来ることのできるタグ
#             AC-B, AC-I, AF-B, AF-I, F-B, F-I,Sf-B,Sf-I,St-B,St-I,Q-B, Q-I, D-B, D-I, T-B, T-I, O
@head_tag = (    1,    0,    1,    0,   1,   0,   1,   0,   1,   0,  1,   0,   1,   0,   1,   0, 1);

#                                         接続可能マトリックス
#                    Ac-B, Ac-I, Af-B, Af-I, F-B, F-I,Sf-B,Sf-I,St-B,St-I, Q-B, Q-I, D-B, D-I, T-B, T-I, O
@connect_matrix = ([    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # Ac-B
                   [    1,    1,    0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 0 ], # Ac-I
                   [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # Af-B
                   [    0,    0,    1,    1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 0 ], # Af-I
                   [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # F-B
                   [    0,    0,    0,    0,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 0 ], # F-I
                   [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # Sf-B
                   [    0,    0,    0,    0,   0,   0,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0, 0 ], # Sf-I
                   [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # St-B
                   [    0,    0,    0,    0,   0,   0,   0,   0,   1,   1,   0,   0,   0,   0,   0,   0, 0 ], # St-I
                   [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # Q-B
                   [    0,    0,    0,    0,   0,   0,   0,   0,   0,   0,   1,   1,   0,   0,   0,   0, 0 ], # Q-I
                   [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # D-B
                   [    0,    0,    0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   0,   0, 0 ], # D-I
                   [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ], # T-B
                   [    0,    0,    0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1, 0 ], # T-I
                   [    1,    1,    1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 1 ]);# O


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
		@buf = split(/\//, $word);
		$wordcont[$wordn] = $buf[0];
		@bufs2 = split(/\&/, $buf[1]);
		$tagn = 0;
		foreach $buf2 (@bufs2){
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
		@probs = split(/\&/, $buf);
		$probn = 0;
		foreach $prob (@probs){
			$rsltprob[$wordn2]{$tags[$wordn2][$probn]} = $prob;
#			printf("$probn %s %s %.2f\n", $tags[$wordn2][$probn], $wordcont[$wordn2], $rsltprob[$wordn2]{$tags[$wordn2][$probn]});
			$probn++;
		}
		$wordn2++;
	}
	<RFILE>;

################# Viterbi algorithmによる最適解の決定 #######################
	@prob = 0;
	
	for($jj=0; $jj<17; $jj++){
		$edge[0][$jj] = 0;
		$prob[0][$jj] = $head_tag[$jj]*$rsltprob[0]{$tagkinds[$jj]};
#		printf("$tagkinds[$jj] $head_tag[$jj] $rsltprob[0]{$tagkinds[$jj]} $prob[0][$jj]\n");
	}

	for($ii=1; $ii<$wordn; $ii++){ # 現在注目している単語
		for($jj=0; $jj<17; $jj++){ # 現在注目している単語がもしこのタグだったら
			# $tagkinds[$jj]: 現在の単語のタグ
			# $rsltprob[$ii]{$tagkinds[$jj]}: 現在の単語がこのタグである確率
			$edge[$ii][$jj] = 0;
			$prob[$ii][$jj] = 0;
			for($kk=0; $kk<17; $kk++){ # 1つ前の単語のタグがもしこのタグだったら
				# $tagkinds[$kk]: 1つ前の単語のタグ
				# $prob[$ii-1][$kk]: 1つ前の単語がこのタグである確率
				
				# 現在のタグのコスト
				$tmpprob[$kk] = $prob[$ii-1][$kk] # 1つ前のタグが$kkだった確率
								* $connect_matrix[$jj][$kk] # 1つ前のタグと現在のタグがつながる確率
								* $rsltprob[$ii]{$tagkinds[$jj]}; # 現在のタグが子のタグである確率
#				printf("$prob[$ii-1][$kk]/$connect_matrix[$jj][$kk]/$rsltprob[$ii]{$tagkinds[$jj]}/$tmpprob[$kk]\n");
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
	for($jj=0; $jj<17; $jj++){
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

