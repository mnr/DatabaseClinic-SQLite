/* California Population Projections contains gender population by county. 
	Create a search that will return a list of 
	the male population 
	and female population 
	for each county 
	for the year 2014.
*/
select
   county_name as "Year.2014",
   sum(populationProjection.population) as 'Male',
   Fem_Pop as 'Female'
from ( select
      county_name as Fem_Cty,
			sum(population) as Fem_Pop
			from populationProjection
			where Year = "01/01/2014 12:00:00 AM"
            and gender = 'Female'
            group by county_name
			)
inner join  populationProjection
on Fem_Cty = populationProjection.county_name
where Year = "01/01/2014 12:00:00 AM"
and gender = 'Male'
group by county_name
order by county_name
