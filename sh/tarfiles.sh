#!/bin/bash
# Creates a tarball of the bacukp files
directory="endgame"

# Source code files

srcdir="../src"
plotdir="../plot"
shdir='../sh'
files="$srcdir $plotdir $shdir ../dirs.sh ../Makefile"

# Output name
output=$directory".tar.bz2"

# Creates the tarball
tar cjfv $output $files

echo "File " $output " ready!"
echo
