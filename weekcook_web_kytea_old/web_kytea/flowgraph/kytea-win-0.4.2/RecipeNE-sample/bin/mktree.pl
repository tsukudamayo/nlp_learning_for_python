
$basefileid = shift;

while (<>) {
    chomp;
    @tmp = split(/ /, $_);
#    print "ID=$fileid", "_$.\n";
    $fileid = $.;
    if ($basefileid) {
	print "ID=$basefileid-$.\n";
    }
    else {
	print "ID=$.\n";
    }
    for my $i (0..$#tmp) {
	($word, $tag) = split(/\//, $tmp[$i]);
	if ($i == $#tmp) {
	    printf("%03d -01 %s %s %s\n", $i+1, $word, $tag);
	}
	else {
	    printf("%03d %03d %s %s %s\n", $i+1, $i+2, $word, $tag);
	}
    }
    print "\n";
}
