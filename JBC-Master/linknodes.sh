#!/bin/bash

port=$1

if [ -z "$port" ] #if port isn't assigned
then
    echo Need to specify port number
    exit 1
fi

FILES=(block.py chain.py config.py mine.py node.py sync.py utils.py genesis.py)

mkdir jbc$port
for file in "${FILES[@]}"
do
    echo Syncing $file
    ln jbc/$file jbc$port/$file
done

echo Synced new jbc folder for port $port

exit 1