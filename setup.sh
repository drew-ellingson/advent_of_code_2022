# example usage: sh setup.sh 01

# get cookie by:
#   1. visiting adventofcode.com
#   2. logging in
#   3. opening developer tools and navigating to application -> cookies
#   4. copying the value of the session cookie into a file named 'session_cookie'  in the same folder as this script

cookie=`cat session_cookie`

mkdir day_$1
cd day_$1

touch input.txt 
touch input2.txt # to be used for the sample input as given in the desc
touch readme.md

echo "with open('input2.txt') as my_file: 
    input = my_file.read()""" > soln.py

code -r readme.md
code -r soln.py

day_sans_padding=$(echo $1 | sed 's/^0*//') # remove leading zeroes for use in curl

curl --cookie "session="$cookie https://adventofcode.com/2022/day/$day_sans_padding/input > input.txt
