#!/usr/bin/perl

# precision, recall, F-measureを計算
# 入力はスペースで区切られた記号列
# 1個目がシステム出力、2個目がテストセット
# (記号は一定のフォーマットに従っていれば何でもあり)
# 入出力の行数をそろえること

use Env;
use File::Basename;

$FILE1 = shift; # tagger
$FILE2 = shift; # test

open(FILE1, $FILE1) || die;
@file1 = <FILE1>;

open(FILE2, $FILE2) || die;
@file2 = <FILE2>;

if ($#file1 != $#file2) {
    printf "file1 %d lines, file2 %d lines.\n", scalar(@file1), scalar(@file2);
    die;
}


$suc = 0;                                         # 完全マッチした文数
$nm1 = 0;                                         # FILE1 のユニット数
$nm2 = 0;                                         # FILE2 のユニット数
$nmm = 0;                                         # マッチしたユニット数

for ($i = 0; $i <= $#file1; $i++) {
    chomp($file1[$i]);
    chomp($file2[$i]);
    @ws1 = split(/ /, $file1[$i]);
    @ws2 = split(/ /, $file2[$i]);
    $wlcs = &WLCS(\@ws1, \@ws2);
    $nm1 += scalar(@ws1);
    $nm2 += scalar(@ws2);
    $nmm += $wlcs;
    if (scalar(@ws2) == $wlcs){
        $suc++;
    }else{
#         print $i, "\n";
#         print "@ws1\n";
#         print "@ws2\n\n";
    }

}

# $FILE1 = basename($FILE1);
# $FILE2 = basename($FILE2);
printf("%d/%d = %5.2f%%\n", $nmm, $nm1, 100*$nmm/$nm1);
#printf("           Recall = %d/%d = %5.2f%%\n", $nmm, $nm2, 100*$nmm/$nm2);
#printf("        F-measure = %5.2f%%\n", 100 * 2 * $nmm/($nm1+$nm2));
#printf("Sentence Accuracy = %d/%d = %4.1f%%\n", $suc, $i, 100*$suc/$i);

close(FILE1);
close(FILE2);

sub WLCS{
    ($ws1, $ws2) = @_;

    ($len1, $len2) = (scalar(@$ws1), scalar(@$ws2));

    @DP = ([(0) x $len2+1]) x $len1+1;

    for ($pos1 = 1; $pos1 <= $len1; $pos1++){
        for ($pos2 = 1; $pos2 <= $len2; $pos2++){
            if ($ws1->[$pos1-1] eq $ws2->[$pos2-1]){
                $DP[$pos1][$pos2] = $DP[$pos1-1][$pos2-1]+1;
            }else{
                $DP[$pos1][$pos2] = &max($DP[$pos1-1][$pos2],  $DP[$pos1][$pos2-1]);
            }
        }
	my $hoge;
    }

    return($DP[$len1][$len2]);
}


sub min{
    my($min) = shift(@_);

    foreach (@_){
        ($_ < $min) && ($min = $_);
    }

    return($min);
}

sub max{
    my($max) = shift(@_);

    foreach (@_){
        ($_ > $max) && ($max = $_);
    }
    
    return($max);
}
