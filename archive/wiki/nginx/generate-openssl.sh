#!/bin/bash
#
# Generate openssl files for HTTPS

if [ -e localhost.key ]|| [ -e localhost.crt ]
then
   echo "localhost.key and localhost.crt already exist..."
else
   echo "generating new openssl files..."
   openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout localhost.key -out localhost.crt -config openssl_self_signed_cert.conf
fi

