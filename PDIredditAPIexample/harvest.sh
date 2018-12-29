#!/bin/bash
for i in `seq 1 100`;
do
	sh ./pan.sh -file='APIgetData.ktr'
	sleep 5; 
done    

