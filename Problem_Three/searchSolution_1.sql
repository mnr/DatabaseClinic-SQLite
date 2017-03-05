/* California Population Projections contains gender population by county. 
	Create a search that will return a list of 
	the male population 
	and female population 
	for each county 
	for the year 2014.
*/


select 
   county_name, 
   gender, 
   sum(population)
from populationProjection
where Year = "01/01/2014 12:00:00 AM"
group by county_name, gender
order by county_name, gender