#!/bin/sh

if [ -z "$1" ]; then
	sed 's/^/.\/gendep.py -r /' | sh | awk '!seen[$0]++'
else
	sed 's/^/.\/gendep.py -r /' ${1} | sh | awk '!seen[$0]++'
fi
