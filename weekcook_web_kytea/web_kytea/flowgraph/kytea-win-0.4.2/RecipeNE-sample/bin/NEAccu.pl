#! /usr/bin/perl

# タグの推定精度を計算
# タグが一つだけ推定されている場合．

# todo: for latex-tabular

$ansfile = $ARGV[0];
$rsltfile = $ARGV[1];

open AFILE, $ansfile;
open RFILE, $rsltfile;

my @afile = <AFILE>;
my @rfile = <RFILE>;

printf("#tag\t#ans\t#rslt\t#true\tprecision\trecall\tF-measure\n");

# for recipe: 8
my @TYPE = qw( Ac Af F Sf St Q D T ); 

# # for shogi: 23
# my @TYPE = qw( Hu Tu Po Pi Ps Mc Pa Pq Re Ph Ai St Ca Ce Me Mn Ee Ev Ti Ac Ap Ao Ot );

# 指定したタグ以外は全てO扱い
my @tagB = ();
my @tagI = ();

for my $i (0..$#TYPE) {
    push(@tagB, "$TYPE[$i]-B");
    push(@tagI, "$TYPE[$i]-I");
}

# @tagB = ("Ac-B", "Af-B", "F-B", "Sf-B", "St-B", "Q-B", "D-B", "T-B");
# @tagI = ("Ac-I", "Af-I", "F-I", "Sf-I", "St-I", "Q-I", "D-I", "T-I");

for my $i (0..$#tagB) {    
    my $NEtag = $tagB[$i];
    $NEtag =~ s/-.$//;
    &calctagA([$tagB[$i]], [$tagI[$i]], $NEtag);
}
print "--\n";

&calctagA(\@tagB, \@tagI, "ALL");

sub calctagA {
    my ($tagb, $tagi, $prNEtag) = @_;

$anstotalwordnum = 0;
$rslttotalwordnum = 0;
$anstotaltruenum = 0;
$rslttotaltruenum = 0;

$anstotalnum = 0;
$rslttotalnum = 0;

$ansBtagn = 0;
# 正解タグを獲得
for my $j (0..$#afile){
	$line = $afile[$j];
	chomp($line);
	@bufs = split(/ /, $line);
	$wordn = 0;
	foreach $buf (@bufs){
		@bufs2 = split(/\//, $buf);
		$wordcont[$wordn] = $bufs2[0];
		# Bのタグがついている単語数をカウント
		$anstag[$wordn] = $bufs2[1];
		if(grep(/$anstag[$ii]/, @$tagb)){
#		if(grep(/$anstag[$ii]/, ($tagB[$i]))){
			$ansBtagn++;
		}
		$wordn++;
	}

# kyteaによるタグ推定結果を獲得
	$line = $rfile[$j];
	chomp($line);
	@bufs = split(/ /, $line);
	$wordn2 = 0;
	foreach $buf (@bufs){
		@bufs2 = split(/\//, $buf);
		$wordcont2[$wordn2] = $bufs2[0];
		$rslttag[$wordn2] = $bufs2[1];
		# Bのタグがついている単語数をカウント
		if(grep(/$rslttag[$ii]/, @$tagb)){
#		if(grep(/$rslttag[$ii]/, ($tagB[$i]))){
			$rslttagn++;
		}
		$wordn2++;
	}
	
#	printf("wordn: $wordn  wordn2: $wordn2\n");
	
	for($ii=0; $ii<$wordn; $ii++){
		if(grep(/$anstag[$ii]/, @$tagb)){
#		if(grep(/$anstag[$ii]/, ($tagB[$i]))){
#			print "ans  [$ii] $wordcont[$ii]\t";
			$anstotalnum++;
			if($anstag[$ii] ne $rslttag[$ii]){
#				printf "$anstag[$ii] ! $rslttag[$ii]\n";
				next;
			}else{
				while(grep(/anstag[$ii+1]/, @$tagi)){
#				while(grep(/anstag[$ii+1]/, ($tagI[$i]))){
					$ii++;
					if($anstag[$ii] ne $rslttag[$ii]){
#						printf "$anstag[$ii] ! $rslttag[$ii]\n";
						next;
					}
				}
#				printf "$anstag[$ii] = $rslttag[$ii]\n";
				$anstotaltruenum++;
			}
		}
	}
#	printf "$wordn $anstotalnum $anstotaltruenum\n";
	
	for($ii=0; $ii<$wordn; $ii++){
		if(grep(/$rslttag[$ii]/, @$tagb)){
#		if(grep(/$rslttag[$ii]/, ($tagB[$i]))){
#			print "rslt [$ii] $wordcont[$ii]\t";
			$rslttotalnum++;
			if($anstag[$ii] ne $rslttag[$ii]){
#				printf "$anstag[$ii] ! $rslttag[$ii]\n";
				next;
			}else{
				while(grep(/rslttag[$ii+1]/, @$tagi)){
#				while(grep(/rslttag[$ii+1]/, ($tagI[$i]))){
					$ii++;
					if($rslttag[$ii] ne $rslttag[$ii]){
#						printf "$anstag[$ii] ! $rslttag[$ii]\n";
					    next;
					}
				}
				$rslttotaltruenum++;
			}
#			printf "$anstag[$ii] = $rslttag[$ii]\n";
		}
	}
#	printf "$wordn $rslttotalnum $rslttotaltruenum\n";
		
#	printf("-------------\n");

}
close AFILE;
close RFILE;

    if ($rslttotalnum > 0 && $anstotalnum > 0) {
	$precision = $anstotaltruenum/$rslttotalnum;
	$recall = $anstotaltruenum/$anstotalnum;
	if ($precision == 0 && $recall == 0) {
	    printf("%s\t%d\t%d\t%d\t%.2f\%\t\t%.2f\%\tNA\n", $prNEtag, $anstotalnum, $rslttotalnum, $anstotaltruenum,
		   $precision*100, $recall*100);
	    return 0;
	}
	$Fmeasure = 2*$precision*$recall/($precision + $recall);
	printf("%s\t%d\t%d\t%d\t%.2f\%\t\t%.2f\%\t%.04f\n", $prNEtag, $anstotalnum, $rslttotalnum, $anstotaltruenum,
	   $precision*100, $recall*100, $Fmeasure);
    }
    elsif ($rslttotalnum > 0) {
	$precision = $anstotaltruenum/$rslttotalnum;
	printf("%s\t%d\t%d\t%d\t%.2f\%\t\tNA\tNA\n", $prNEtag, $anstotalnum, $rslttotalnum, $anstotaltruenum,
	   $precision*100);
    }
    elsif ($anstotalnum > 0) {
	$recall = $anstotaltruenum/$anstotalnum;
	printf("%s\t%d\t%d\t%d\tNA\t\t%.2f\%\tNA\n", $prNEtag, $anstotalnum, $rslttotalnum, $anstotaltruenum,
	   $recall*100);
    }
    else {
	printf("%s\t%d\t%d\t%d\tNA\t\tNA\tNA\n", $prNEtag, $anstotalnum, $rslttotalnum, $anstotaltruenum);
    }
    return 0;
}
