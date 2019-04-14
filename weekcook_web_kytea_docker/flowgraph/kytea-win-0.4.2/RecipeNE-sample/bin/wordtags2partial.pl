
use encoding "utf-8";
use strict;

# 入力: ホット/F-B ケーキ/F-I を/O しっかり/O ...
# 出力: ホ-ッ-ト|ケ-ー-キ|を し っ か り ...
# BIOタグの付与された単語列のみに単語境界情報を付与

my @TAGS = (
    "Ac-B", "Ac-I",
    "Af-B", "Af-I",
    "F-B", "F-I",
    "Sf-B", "Sf-I",
    "St-B", "St-I",
    "Q-B", "Q-I",
    "D-B", "D-I",
    "T-B", "T-I"
);

my $TAGS = join("|", @TAGS);

while (<>) {
    chomp;
    my @units = split(/ /, $_);

    my $outstr;

    for my $i (0..$#units) {
	my ($word, $tag) = split(/\//, $units[$i]);
	my @word = split(//, $word);

	if ($tag =~ /($TAGS)/) {
	    $outstr .= "|" unless ($i == 0);
	    $outstr .= join("-", @word);
	    $outstr .= "|" unless ($i == $#units);
	}
	else {
	    $outstr .= " " unless ($i == 0);
	    $outstr .= join(" ", @word);
	    $outstr .= " " unless ($i == $#units);
	}
    }
    $outstr =~ s/\|\|/\|/g;
    $outstr =~ s/  / /g;
    $outstr =~ s/\| /\|/g;
    $outstr =~ s/ \|/\|/g;
    print "$outstr\n";
}
