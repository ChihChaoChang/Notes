#!/bin/bash

  ########################################################
   #
   #  jlk1.sh john herraghty 2016-04-11
   #  1:  do DNS lookup from a list of servers,
   #  :  
  #  2:  Echo results to a log file.
   #
   #########################################################


dnsvar=‘’
ipvar=‘’
pingvar=‘’
sshvar=‘’
#    Input file goes here.
filename=‘list1.txt’

# Output file goes here.
outfile=‘outfile.csv’

hostname=‘’
filelines=`cat $filename`

echo Start
for line in $filelines ; do
#ipvar=“$(getent hosts $line | awk ‘{print $1}‘)”

if [ -z $ipvar ] ; then
    ipvar=$(nslookup $line 10.218.28.10 | grep name | awk ‘{print $4}‘)
        if [ -z $ipvar ] ; then  dnsfound=“DNS-No”; else dnsfound=“DNS-Yes”; fi
    else
    dnsfound=“DNS-Yes”
fi

if [ -z $ipvar ] ; then
    ipvar=$(nslookup $line 10.217.3.22 | grep name | awk ‘{print $4}‘)
        if [ -z $ipvar ] ; then  dnsfound=“DNS-No”; else dnsfound=“DNS-Yes”; fi
    else
    dnsfound=“DNS-Yes”
fi

if [ -z $ipvar ] ; then
    ipvar=$(nslookup $line 10.217.2.14 | grep name | awk ‘{print $4}‘)
        if [ -z $ipvar ] ; then  dnsfound=“DNS-No”; else dnsfound=“DNS-Yes”; fi
    else
    dnsfound=“DNS-Yes”
fi

##   Begin SNMP hostname check.
### If everything fails, do an snmp check on hostname.  
### Only specified servers should be able to query using snmp, so pay attnetion if you use this option. 

if [ -z $ipvar ] ; then
       ipvar=$(snmpget -v2c -r1 -t1 -cRO-STRING-GOES-HERE -mALL $line sysName.0 | awk ‘{print $4}‘)
           if [ -z $ipvar ] ; then  dnsfound=“DNS-No”; else dnsfound=“DNS-Yes”; fi
    else
    dnsfound=“DNS-Yes”
fi
###  End SNMP hostname check.


               echo $line “,” $ipvar  >> jout1.csv
                echo $line “,” $ipvar
ipvar=‘’
done
