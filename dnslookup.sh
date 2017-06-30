#!/bin/bash

ipvar=''


servers=( 
10.80.13.42
10.80.13.43
10.80.13.44
10.80.13.45
10.80.13.46
10.80.19.41
10.81.34.22
10.110.12.37
10.110.12.38
10.110.12.39
)

for line in "${servers[@]}"; do
#those are 3 different dns servers we have.  
#reverse lookup (ip to name) isn't recursive, unlike forward lookup so force them traverse the dns servers looking for a match
      if [ -z $ipvar ]
      then
          ipvar=$(nslookup $line 10.218.28.10 | grep name | awk '{print $4}') 
      fi
      if [ -z $ipvar ]
      then
          ipvar=$(nslookup $line 10.217.3.22 | grep name | awk '{print $4}') 
      fi
      if [ -z $ipvar ]
      then
          ipvar=$(nslookup $line 10.217.2.14 | grep name | awk '{print $4}') 
      fi
      
##   Begin SNMP hostname check.
### If everything fails, do an snmp check on hostname.  
### Only specified servers should be able to query using snmp, so pay attnetion if you use this option. 

      if [ -z $ipvar ] ; then
          ipvar=$(snmpget -v2c -r1 -t1 -cRO-STRING-GOES-HERE -mALL $line sysName.0 | awk '{print $4}')        
      fi

echo Start
echo $line , $ipvar  >> jout1.csv
echo $line , $ipvar
ipvar=''
done
