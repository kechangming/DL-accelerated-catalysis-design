#! /bin/bash

first=$1
second=$2

for temperature in 473 523 573 623 673 723 773 823 873
do
	prefactor=`nonactive_prefactor $first $second $temperature 10.0|tail -1`
printf "%d %1.5e \n" $temperature $prefactor
done
