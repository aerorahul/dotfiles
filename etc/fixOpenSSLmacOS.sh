#!/bin/bash

#echo 'update brew'
#
#brew update
#
#echo 'upgrade brew'
#
#brew upgrade
#
#echo 'brew install openssl'
#
#brew install openssl@1.1

version=$(brew list --formula openssl@1.1 --versions | cut -d " " -f2)

if [ -f /usr/local/lib/libssl.dylib ]; then
    echo 'backing up existing libssl.dylib'
    mv /usr/local/lib/libssl.dylib /usr/local/lib/libssl_bak.dylib
fi

if [ -f /usr/local/lib/libcrypto.dylib ]; then
    echo 'backing up existing libcrypto.dylib'
    mv /usr/local/lib/libcrypto.dylib /usr/local/lib/libcrypto_bak.dylib
fi

# Leaving some commands to check directory contents
# ls -al /usr/local/Cellar/openssl@1.1/$version/lib
# ls -al /usr/local/lib/libssl* && ls -al /usr/local/lib/libcrypto*

echo 'add symlink to missing openssl libs'

if [ -f /usr/local/Cellar/openssl@1.1/$version/lib/libssl.1.1.dylib ]; then
    sudo ln -s /usr/local/Cellar/openssl@1.1/$version/lib/libssl.1.1.dylib /usr/local/lib/libssl.dylib
fi

if [ -f /usr/local/Cellar/openssl@1.1/$version/lib/libcrypto.1.1.dylib ]; then
    sudo ln -s /usr/local/Cellar/openssl@1.1/$version/lib/libcrypto.1.1.dylib /usr/local/lib/libcrypto.dylib
fi

echo 'add symlink to missing openssl pkgconfig files'

if [ -f /usr/local/Cellar/openssl@1.1/$version/lib/pkgconfig/openssl.pc ]; then
    sudo ln -s /usr/local/Cellar/openssl@1.1/$version/lib/pkgconfig/openssl.pc /usr/local/lib/pkgconfig/openssl.pc
fi

if [ -f /usr/local/Cellar/openssl@1.1/$version/lib/pkgconfig/libssl.pc ]; then
    sudo ln -s /usr/local/Cellar/openssl@1.1/$version/lib/pkgconfig/libssl.pc /usr/local/lib/pkgconfig/libssl.pc
fi

if [ -f /usr/local/Cellar/openssl@1.1/$version/lib/pkgconfig/libcrypto.pc ]; then
    sudo ln -s /usr/local/Cellar/openssl@1.1/$version/lib/pkgconfig/libcrypto.pc /usr/local/lib/pkgconfig/libcrypto.pc
fi
