/* California Population Projections contains gender population by county. 
	Create a search that will return a list of 
	the male population 
	and female population 
	for each county 
	for the year 2014.
*/


select 
   `County Name`, 
   gender, 
   sum(population)
from secondTable
where Year = 2014
group by  `County Name`, gender
order by  `County Name`, gender