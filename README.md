# Environment Model Generation
## Data Analyzer csv file format
### Each row represents a single day.
	1. 1st column shows which day it is.
	  1.1. t is totally same with ‘WEEKDAY’ function with return type ‘1’ in Microsoft Excel.
	  1.2. It is 1(Monday) to 7(Sunday)
	2. 2nd to 25th column shows traffic data.
	  2.1. 2nd column is for 0:00 to 1:00 and 25th column is for 23:00 to 24:00.
	  2.2. Each number should be written as common Arabic numbers.
	  2.3. You can add comma for large numbers. (Don’t include period instead of comma)
