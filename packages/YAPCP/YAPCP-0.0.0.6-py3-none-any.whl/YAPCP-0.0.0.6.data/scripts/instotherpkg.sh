#!/bin/bash

if [ ! -d $HOME/bin ];
then
    # create bin directory and get repo
    mkdir -p $HOME/bin
fi

# clean, download, and unzip latest platform tools, repo
rm -rf $HOME/bin/platform-tools-latest-linux.zip
rm -rf $HOME/bin/platform-tools-latest-linux*.zip
rm -rf $HOME/bin/platform-tools
aria2c https://dl.google.com/android/repository/platform-tools-latest-linux.zip -d $HOME/bin -o platform-tools-latest-linux.zip
unzip $HOME/bin/platform-tools-latest-linux.zip -d $HOME/bin
rm -rf $HOME/bin/platform-tools-latest-linux.zip
rm -rf $HOME/bin/platform-tools-latest-linux*.zip

rm -rf $HOME/bin/repo
aria2c https://storage.googleapis.com/git-repo-downloads/repo -d $HOME/bin
chmod a+x $HOME/bin/repo
