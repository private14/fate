#!/bin/sh

#HOST=115.124.16.69
#USERNAME=loanplat
#PASSWORD=123456

ls_date=`date +%Y%m%d`

lftp -u $USERNAME,$PASSWORD sftp://$HOST << EOF
    mkdir /download/contract/idcard/${ls_date}/
    cd /download/contract/idcard/${ls_date}/
    mput /opt/app/sftp/$1A.zip
    mput /opt/app/sftp/$1A.zip.txt

    bye
EOF

rm -rf /opt/app/sftp/$1A.zip
rm -rf /opt/app/sftp/$1A.zip.txt