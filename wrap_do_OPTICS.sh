#!/bin/bash

for hari in {1..31}
do
	for jam in {0..23}
	do
		echo ./do_OPTICS.py 2019 6 $hari $jam 0 CGPositive 0
		./do_OPTICS.py 2019 6 $hari $jam 0 CGPositive 0
		
		echo ./do_OPTICS.py 2019 6 $hari $jam 0 CGNegative 1
		./do_OPTICS.py 2019 6 $hari $jam 0 CGNegative 1

		echo ./do_OPTICS.py 2019 6 $hari $jam 15 CGPositive 0
		./do_OPTICS.py 2019 6 $hari $jam 15 CGPositive 0
		
		echo ./do_OPTICS.py 2019 6 $hari $jam 15 CGNegative 1
		./do_OPTICS.py 2019 6 $hari $jam 15 CGNegative 1
		
		echo ./do_OPTICS.py 2019 6 $hari $jam 30 CGPositive 0
		./do_OPTICS.py 2019 6 $hari $jam 30 CGPositive 0
		
		echo ./do_OPTICS.py 2019 6 $hari $jam 30 CGNegative 1
		./do_OPTICS.py 2019 6 $hari $jam 30 CGNegative 1
		
		echo ./do_OPTICS.py 2019 6 $hari $jam 45 CGPositive 0
		./do_OPTICS.py 2019 6 $hari $jam 45 CGPositive 0
		
		echo ./do_OPTICS.py 2019 6 $hari $jam 45 CGNegative 1
		./do_OPTICS.py 2019 6 $hari $jam 45 CGNegative 1
		
		echo ./do_OPTICS.py 2019 6 $hari $jam 0 2
		./do_OPTICS.py 2019 6 $hari $jam 0 2
		
		echo ./do_OPTICS.py 2019 6 $hari $jam 15 2
		./do_OPTICS.py 2019 6 $hari $jam 15 2
		
		echo ./do_OPTICS.py 2019 6 $hari $jam 30 2
		./do_OPTICS.py 2019 6 $hari $jam 30 2
		
		echo ./do_OPTICS.py 2019 6 $hari $jam 45 2
		./do_OPTICS.py 2019 6 $hari $jam 45 2
	done
done
