#!/usr/bin/expect

expect -c "
spawn scp -r $1 root@192.168.0.210:/opt/app/sftp/

expect \"password:\"
send \"51xf@password123\r\"
expect eof
"