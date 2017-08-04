-- A version of the search solution using views instead of subqueries
-- be sure to run searchSolution_views_part_1.sql before running this

select
   `County Name` as "Year: 2014",
   sum(secondTable.population) as 'Male',
   Female_Pop as 'Female'
from female_population_view
inner join  secondTable
      on Female_Cty = secondTable.`County Name`
 where Year = 2014 and gender = 'Male'
group by `County Name`
order by `County Name`
