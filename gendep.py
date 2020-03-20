#!/usr/bin/python3

import requests
import argparse

baseLink = "http://distro.ibiblio.org/tinycorelinux/11.x/x86/tcz/"
reverseBuff = b''
reversePrint = False

def getDeps(packName):
	rcontent = requests.get(baseLink + packName)
	if rcontent.status_code != 200:
		return 1
	return rcontent.content

def printDeps(packName, level):
	global reverseBuff
	packName += ".dep"
	deps = getDeps(packName)
	if deps != 1:
		deps = deps.decode().split('\n')
		deps.remove('')
		for x in deps:
			if level == 0:
				if reversePrint:
					reverseBuff = x.encode('utf-8') + b'\n' + reverseBuff
				else:
					print(x)
				printDeps(x, 0)
			if level > 0:
				out = "│" * level
				out += "└── " + x
				print(out)
				printDeps(x, level+1)
	return

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate full dependency list (tree) for given package.')
	parser.add_argument('-t', '--tree', action='store_true', help="Generate human readable tree.")
	parser.add_argument('-r', '--reverse', action='store_true', help="Reverse list print, for OS loading reasons. Not to use with -t. Takes more timeto build list.")
	parser.add_argument('packagename', help="Name of package")
	args = parser.parse_args()
   
	if args.tree and args.reverse:
		print("Well, no.")
		exit(1)

	if args.packagename[-4:] != ".tcz":
		args.packagename += ".tcz"

	if requests.get(baseLink + args.packagename).status_code != 200:
		print(f"Error: package {args.packagename} not found!")
		exit(1)
	
	if args.reverse:
		reversePrint = True

	if args.tree:
		print(args.packagename)
		printDeps(args.packagename, 1)
	else:
		if not reversePrint:
			print(args.packagename)
		printDeps(args.packagename, 0)

	if reversePrint:
		print(reverseBuff.decode()[:-1])
		print(args.packagename)
