#!/usr/bin/perl
############################################
#filename: http_log_monitor.pl
############################################
#description: checks outside website for 500 http errors. send email to any issues.
#kind of a canary in the coal mine
#author - Teddy Knab

use Sys::Hostname;    #for host lookups
use Net::SMTP;        #for email

############################################
#cronjob run at 59 every hour.
############################################

############################################
#globals for UScourts
############################################
#my $mailhost='cmecf.uscmail.dcn'; #inside ecf servers
my $mailhost     = 'smtp.uscourts.gov';             #outside      #change this
my $from_address = "myemail\@mycourt.uscourts.gov";    #change this the sending address
my $to_address   = "myemail\@mycourt.uscourts.gov";    #chage this to your email address

sub run_command_and_return_results {

#description takes input in the form of a command and returns the results in an array
    my $command = shift;
    my @results;
    my @return_raw;
    my $count = 0;

    open( CMD, "$command|" );
    @results = <CMD>;
    close CMD;

    foreach my $line (@results) {
        chomp $line;

        #print "run_command_and_return_results $line\n";
        $count = $count + 1;
        push( @return_raw, $line );
    }
    print "**** We got \'$count\' raw lines\n";
    return @return_raw;
}

sub my_date {
    my $date2;

    my @months  = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
    my @numdays = qw( 00 01 02 03 04 05 06 07 08 09);

    my ( $sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst ) =
      localtime();
    my $my1 = $year + 1900;    #get real georgian calendar year
    if ( $mday < 10 ) {
        $date2 = "$numdays[$mday]/$months[$mon]/$my1:$hour";
        print "$date2\n";
    }
    else {
        $date2 = "$mday/$months[$mon]/$my1:$hour";
        print "$date2\n";
    }
    return $date2;
}

sub check_logs_for_web_errors {
    my @log_check =
      run_command_and_return_results("sudo cat /var/log/httpd/live.access.log");
    my @report;
    my $count    = 0;
    my $count500 = 0;
    my $count501 = 0;
    my $count502 = 0;
    my $count503 = 0;
    my $count504 = 0;
    my $count505 = 0;

    my $d1 = my_date();

    foreach my $line (@log_check) {
        chomp $line;

        if ( $line =~ /HTTP\/1\.[1|0]\" 500/ && $line =~ /$d1/ ) {
            print "debug internal service error: $line\n";
            push( @report, "HTTP ERROR: $line - internal server error WARN" );
            $count500 = $count500 + 1;
        }
        elsif ( $line =~ /HTTP\/1\.[1|0]\" 501/ && $line =~ /$d1/ ) {
            print "debug internal service error: $line\n";
            push( @report, "HTTP ERROR: $line - not implemented WARN " );
            $count501 = $count501 + 1;
        }
        elsif ( $line =~ /HTTP\/1\.[1|0]\" 502/ && $line =~ /$d1/ ) {
            push( @report, "HTTP ERROR: $line - bad gateway WARN " );
            $count502 = $count502 + 1;
        }
        elsif ( $line =~ /HTTP\/1\.[1|0]\" 503/ && $line =~ /$d1/ ) {
            push( @report, "HTTP ERROR: $line - service unavailable WARN" );
            $count503 = $count503 + 1;
        }
        elsif ( $line =~ /HTTP\/1\.[1|0]\" 504/ && $line =~ /$d1/ ) {
            push( @report, "HTTP ERROR: $line - Gateway Timeout WARN" );
            $count504 = $count504 + 1;
        }
        elsif ( $line =~ /HTTP\/1\.[1|0]\" 505/ && $line =~ /$d1/ ) {
            push( @report,
                "HTTP ERROR: $line - HTTP Version Not Supported WARN" );
            $count505 = $count505 + 1;
        }
        else {
            #do nothing
        }
        $count = $count + 1;
    }
    print "debug check processed $count lines\n";
    print "internal server errors $count500\n";
    print "501 not implemented $count501\n";
    print "502 bad gateway $count502\n";
    print "503 service unavailable $count503\n";
    print "504 Gateway Timeout $count504\n";
    print "505 - HTTP Version Not supported $count505\n";
    return @report;

}

sub email_report {
    my ( $mailhost, $from, $to, $warn_count, @report ) = @_;
    my $host = hostname() or die "unable to get hostname\n";    #my hostname
    print "debug email_report got $warn_count\n";

    my $smtp = Net::SMTP->new($mailhost);

    $smtp->mail( $ENV{USER} );
    $smtp->to($to);

    $smtp->data();
    $smtp->datasend("To: $to\n");
    $smtp->datasend("From: $from\n");
    $smtp->datasend("Subject:$host - OUTSIDE WEB REPORT warn: $warn_count\n");
    $smtp->datasend("\n");
    $smtp->datasend("******** START  OUTSIDE WEB REPORT ***********\n");

    foreach my $line (@report) {
        chomp $line;
        print "debug: email_report $line\n";
        $smtp->datasend("$line\n");
    }

    $smtp->datasend("******** END  OUTSIDE WEB REPORT ***********\n");

    $smtp->dataend();
    $smtp->quit;

}

sub count_warnings {
    my @report = @_;
    my $count  = 0;
    foreach my $line (@report) {
        if ( $line =~ /WARN/ ) {
            $count = $count + 1;
        }
    }
    print "debug: count_warnings $count\n";
    return $count;
}

my @report;
@report = check_logs_for_web_errors();
my $warn_count = 0;
$warn_count = count_warnings(@report);
if ( $warn_count >= 1 ) {
    email_report( $mailhost, $from_address, $to_address, $warn_count, @report );
    print "email sent\n";
}
else {
    print "no email\n";
}

