#!/bin/sh

#HOST=115.124.16.69
#USERNAME=loanplat
#PASSWORD=123456
HOST=172.16.2.3
USERNAME=kaka
PASSWORD=kaka@sftp123@2018
ls_date=`date +%Y%m%d`

lftp -u $USERNAME,$PASSWORD sftp://$HOST << EOF
    cd /download/contract/apply/
    mkdir ${ls_date}
    cd ${ls_date}
    mput /Users/wanyl/Desktop/wanyl/apiTest/resource_all/contract/$1A.zip
    mput /Users/wanyl/Desktop/wanyl/apiTest/resource_all/contract/$1A.zip.txt
    cd
    cd /download/contract/credit_authz/
    mkdir ${ls_date}
    cd ${ls_date}
    mput /Users/wanyl/Desktop/wanyl/apiTest/resource_all/contract/$1A.zip
    mput /Users/wanyl/Desktop/wanyl/apiTest/resource_all/contract/$1A.zip.txt
    cd /download/contract/loan/
    mkdir ${ls_date}
    cd ${ls_date}
    mput /Users/wanyl/Desktop/wanyl/apiTest/resource_all/contract/$1A.zip
    mput /Users/wanyl/Desktop/wanyl/apiTest/resource_all/contract/$1A.zip.txt
    cd /download/contract/loan_authz/
    mkdir ${ls_date}
    cd ${ls_date}
    mput /Users/wanyl/Desktop/wanyl/apiTest/resource_all/contract/$1A.zip
    mput /Users/wanyl/Desktop/wanyl/apiTest/resource_all/contract/$1A.zip.txt
    bye
EOF
