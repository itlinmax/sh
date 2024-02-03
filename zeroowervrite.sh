#!/bin/bash

owerwrite_count=3
FILE="$1"
echo "----------------------------------------------------"
echo "file is: $FILE"
BLOCKS_NUMBER=$(stat --format=%b $FILE)
echo "blocks numbet of $FILE: $BLOCKS_NUMBER"
BLOCK_SIZE=$(stat --format=%B $FILE)
echo "block size of $FILE: $BLOCK_SIZE bytes"
echo "owerwriting $FILE by zerous"
while [ $owerwrite_count -ne 0 ]
do
    dd if=/dev/zero of=$FILE bs=$BLOCK_SIZE count=$BLOCKS_NUMBER conv=notrunc
    owerwrite_count=$(( $owerwrite_count - 1 ))
done
echo "DONE"
echo "----------------------------------------------------"
