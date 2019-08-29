#!/bin/sh

#HOST=115.124.16.69
#USERNAME=loanplat
#PASSWORD=123456
HOST=192.168.10.207
USERNAME=kaka
PASSWORD=kaka@sftp123
ls_date=`date +%Y%m%d`

lftp -u $USERNAME,$PASSWORD sftp://$HOST << EOF
    mkdir /download/contract/apply/${ls_date}/
    cd /download/contract/apply/${ls_date}/
    mput /opt/app/sftp/$1A.zip
    mput /opt/app/sftp/$1A.zip.txt
    cd
    mkdir /download/contract/credit_authz/${ls_date}/
    cd /download/contract/credit_authz/${ls_date}/
    mput /opt/app/sftp/$1A.zip
    mput /opt/app/sftp/$1A.zip.txt
    cd
    mkdir /download/contract/loan_authz/${ls_date}/
    cd /download/contract/loan_authz/${ls_date}/
    mput /opt/app/sftp/$1A.zip
    mput /opt/app/sftp/$1A.zip.txt
    cd
    mkdir /download/contract/loan/${ls_date}/
    cd /download/contract/loan/${ls_date}/
    mput /opt/app/sftp/$1A.zip
    mput /opt/app/sftp/$1A.zip.txt
    bye
EOF

rm -rf /opt/app/sftp/$1A.zip
rm -rf /opt/app/sftp/$1A.zip.txt
