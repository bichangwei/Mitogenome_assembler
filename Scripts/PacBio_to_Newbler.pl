#!/usr/bin/perl
#---------------------------------------------------------------------#
# @Author: Changwei Bi
# @E-mail: bichwei@163.com
# @Function: Convert long reads into a new file for Newbler assembly (<30k)
# @File: PacBio_to_Newbler.pl
#---------------------------------------------------------------------#
use strict;
use warnings;
use Getopt::Long;

my $usage = "
Usage: perl $0 -i <in.input file> -o <out.output file> -b <break number>\n

";

my ($in,$out,$help);
my $break = 20000;

GetOptions (
	"in=s"     => \$in,     # string
        "out=s"    => \$out,    # string
	"break=i"      => \$break,		# int
	"help"	   => \$help);		# flag
die "$usage\n" if ($help || !$in || !$out);

open IN,"<$in" or die "$!";
open OUT,">$out" or die "$!";

my $name = 1;
my $seq_count = 0;
while(<IN>){
        chomp;
        if(/^>/){
		$seq_count++;
                next;
        }elsif(/^[ATCGN]/){
                my $len = length $_;
                if($len < 30000){
                        print OUT ">$name\n$_\n"; 
			$name++;
                }elsif($len >= 30000){
                        # Braek the reads (>30k) into more short reads (<20k) 
			my $num = int ($len / $break);
                        for my $i (0 .. $num){
                                my $data = substr($_,$i*$break,$break);
                                print OUT ">$name\n$data\n";
                                $name++;
                        }
                }
	}
}
print "The raw sequence number is: $seq_count\n";
print "The processed sequence number is:",$name-1,"\n";
close IN;
close OUT;
