/* California Population Projections contains gender population by county. 
	Create a search that will return a list of 
	the male population 
	and female population 
	for each county 
	for the year 2014.
*/

select
   `County Name` as "Year: 2014",
   sum(secondTable.population) as 'Male',
   Female_Pop as 'Female'
from ( select
      `County Name` as Female_Cty,
			sum(population) as Female_Pop
			from secondTable
			where Year = 2014 and gender = 'Female'
            group by `County Name`
			)
inner join  secondTable
      on Female_Cty = secondTable.`County Name`
 where Year = 2014 and gender = 'Male'
group by `County Name`
order by `County Name`
