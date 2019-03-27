
use strict;
use Getopt::Long;

my %opts = ();
GetOptions(\%opts, 'fields=s', 'delimiter=s', 'unitdelimiter=s', 'help');

if ($opts{help}) {
    warn "Usage:\n\n";
    warn "  -f, -fields=LIST                       n\n";
    warn "                                       n-m\n";
    warn "                                 n,m,l,...\n";
    warn "                            (default: \"1\")\n";
    warn "  -d, -delimiter=DELIM      (default: \" \")\n";
    warn "  -u, -unitdelimiter=DELIM  (default: \"/\")\n";
    exit();
}

$opts{delimiter} = " " unless ($opts{delimiter});
$opts{unitdelimiter} = "/" unless ($opts{unitdelimiter});

my @flds;
if ($opts{fields}) {
    if ($opts{fields} =~ /^([0-9]+)-([0-9]+)$/) {
	@flds = ($1..$2);
    }
    elsif ($opts{fields} =~ / /) {
	@flds = split(/ /, $opts{fields});
    }
    elsif ($opts{fields} =~ /,/) {
	@flds = split(/,/, $opts{fields});
    }
    elsif ($opts{fields} =~ /^[0-9]+$/) {
	@flds = ($opts{fields});
    }
    else {
	die "invalid number\n";
    }
}
else {
    @flds = ("1");
}

$/ = "\n\n";
while (<>) {
    chomp;
    my @units = split(/\n/, $_);

    my $ID = shift(@units);

    my @out;
    foreach my $u (@units) {
	$u =~ s/ +$//;
	my ($pid, $cid, @rest) = split(/ +/, $u);
	my @ostr;
	foreach my $fi (@flds) {
	    die "$_\n@rest @flds: $fi\n invalid number\n" if ($fi !~ /^[0-9]+$/);
	    die "$_\n@rest @flds: $fi $#rest\n invalid number\n" if ($fi < 0 || $fi-1 > $#rest);
	    push(@ostr, $rest[$fi-1]);
	}
	my $ostr = join($opts{unitdelimiter}, @ostr);
	push(@out, $ostr);
    }
    print join(($opts{delimiter}), @out), "\n";
}
