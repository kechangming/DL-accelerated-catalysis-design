#! /bin/bash

first=$1
second=$2

for temperature in 673 723 773 823 873 923 973
do
	prefactor=`prefactor $first $second $temperature 10.0|tail -1`
printf "%d %1.5e \n" $temperature $prefactor
done
