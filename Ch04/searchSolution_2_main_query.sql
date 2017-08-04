/* This is the main query for the search solution 
*/

select
   `County Name` as "Year: 2014",
   sum(secondTable.population) as 'Male'
from secondTable
where Year = 2014 and gender = 'Male'
group by `County Name`
order by `County Name`
